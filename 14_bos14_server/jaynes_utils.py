"""Common utilities for jaynes-based cluster dispatch.

Provides GPU/storage resource probing, resource-based filtering, and a
generic work-queue dispatcher.  Node discovery is handled by
``jaynes.discover_nodes()``.
"""

import os
import subprocess
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed

import jaynes
from jaynes.runners import Slurm

CTRL_NODE = "bos14-ctrl-000"


def check_node_reachable(node, timeout=20):
    """Quick SSH connectivity check. Returns (reachable, reason)."""
    try:
        r = subprocess.run(
            ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
             "-o", f"ConnectTimeout={timeout}", node, "hostname"],
            capture_output=True, text=True, timeout=timeout,
        )
        if r.returncode == 0:
            return True, None
        return False, (r.stderr.strip() or f"exit={r.returncode}")[:200]
    except subprocess.TimeoutExpired:
        return False, "timeout"


def repair_ctrl_connection(ctrl=CTRL_NODE, timeout=15):
    """SSH to the control node to warm up / repair the ProxyJump route.

    Returns True if the control node is reachable after the attempt.
    """
    try:
        r = subprocess.run(
            ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
             "-o", f"ConnectTimeout={timeout}", ctrl, "echo ok"],
            capture_output=True, text=True, timeout=timeout,
        )
        return r.returncode == 0
    except subprocess.TimeoutExpired:
        return False


# ── Resource Probing ────────────────────────────────────────────────────────


def probe_node_resources(node, timeout=10):
    """SSH into a node and query GPU status, GPU processes, and disk usage.

    Returns dict with keys: gpus, processes, storage, or error.
    """
    gpu_cmd = (
        "nvidia-smi --query-gpu=index,name,memory.free,memory.total,utilization.gpu"
        " --format=csv,noheader,nounits"
    )
    proc_cmd = (
        "nvidia-smi --query-compute-apps=pid,gpu_bus_id,used_gpu_memory,process_name"
        " --format=csv,noheader,nounits"
    )
    disk_cmd = "df -h / /home 2>/dev/null | tail -n +2"
    combined = f"{gpu_cmd} && echo '---SEPARATOR---' && {proc_cmd}; echo '---SEPARATOR---' && {disk_cmd}"

    try:
        r = subprocess.run(
            ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
             "-o", f"ConnectTimeout={timeout}", node, combined],
            capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"error": "SSH timeout"}

    if r.returncode != 0 and "no running" not in r.stderr.lower():
        return {"error": r.stderr.strip()[:200]}

    # nvidia-smi process query prints to stderr when empty, but stderr also
    # contains SSH host-key warnings that would corrupt parsing — filter those out.
    filtered_stderr = "\n".join(
        line for line in r.stderr.splitlines()
        if not line.startswith("Warning: Permanently added")
    )
    output = r.stdout + filtered_stderr
    parts = output.split("---SEPARATOR---")

    # Parse GPUs
    gpus = []
    if len(parts) >= 1:
        for line in parts[0].strip().splitlines():
            fields = [f.strip() for f in line.split(",")]
            if len(fields) >= 5:
                gpus.append({
                    "index": int(fields[0]),
                    "name": fields[1],
                    "mem_free_mb": int(fields[2]),
                    "mem_total_mb": int(fields[3]),
                    "util_pct": int(fields[4]),
                })

    # Parse processes
    processes = []
    if len(parts) >= 2:
        for line in parts[1].strip().splitlines():
            if not line.strip() or "no running" in line.lower():
                continue
            fields = [f.strip() for f in line.split(",")]
            if len(fields) >= 4:
                processes.append({
                    "pid": fields[0],
                    "gpu_bus_id": fields[1],
                    "used_mem_mb": fields[2],
                    "process": fields[3],
                })

    # Parse storage
    storage = []
    if len(parts) >= 3:
        for line in parts[2].strip().splitlines():
            fields = line.split()
            if len(fields) >= 5:
                try:
                    use_pct = int(fields[4].rstrip("%"))
                except ValueError:
                    continue
                storage.append({
                    "filesystem": fields[0],
                    "size": fields[1],
                    "used": fields[2],
                    "avail": fields[3],
                    "use_pct": use_pct,
                    "mount": fields[5] if len(fields) > 5 else "/",
                })

    return {"gpus": gpus, "processes": processes, "storage": storage}


def _fmt_mem_gb(mb):
    """Format MB as compact GB string."""
    gb = mb / 1024
    return f"{gb:.0f}G" if gb >= 1 else f"{mb}M"


def print_node_resources(node, info):
    """Pretty-print probed resources for a node."""
    if "error" in info:
        print(f"  {node}: ERROR — {info['error']}")
        return

    procs = info.get("processes", [])
    gpus = info.get("gpus", [])
    pad = " " * len(node)

    for i, g in enumerate(gpus):
        short_name = (g["name"]
                      .replace("NVIDIA ", "")
                      .replace(" Workstation Edition", "")
                      .replace(" Laptop GPU", ""))
        proc_str = f"{len(procs)} proc" if procs else "idle"
        label = node if i == 0 else pad
        print(f"  {label}  GPU {g['index']}: {short_name}  "
              f"{_fmt_mem_gb(g['mem_free_mb'])}/{_fmt_mem_gb(g['mem_total_mb'])}  "
              f"util {g['util_pct']}%  {proc_str}")

    disks = info.get("storage", [])
    if disks:
        parts = [f"{s['mount']} {s['use_pct']}% ({s['avail']} free)" for s in disks]
        print(f"  {pad}  disk  {' | '.join(parts)}")


# ── Resource Filtering ──────────────────────────────────────────────────────


def filter_nodes_by_resources(nodes, resource_map, *,
                              min_free_gpu_mem_mb=0,
                              max_gpu_util_pct=100,
                              max_storage_pct=100):
    """Filter nodes based on GPU/storage thresholds.

    Returns (accepted, rejected_with_reason).
    """
    accepted = []
    rejected = []

    for node in nodes:
        info = resource_map.get(node)
        if not info or "error" in info:
            rejected.append((node, "probe failed"))
            continue

        # Check storage
        for s in info.get("storage", []):
            if s["use_pct"] > max_storage_pct:
                rejected.append((node, f"storage {s['mount']} at {s['use_pct']}% "
                                       f"> {max_storage_pct}%"))
                break
        else:
            # Check if at least one GPU passes thresholds
            gpus = info.get("gpus", [])
            if not gpus:
                rejected.append((node, "no GPUs found"))
                continue

            usable = [
                g for g in gpus
                if g["mem_free_mb"] >= min_free_gpu_mem_mb
                and g["util_pct"] <= max_gpu_util_pct
            ]
            if usable:
                accepted.append(node)
            else:
                rejected.append((node, f"0/{len(gpus)} GPUs pass thresholds "
                                       f"(need free>={min_free_gpu_mem_mb}MB, "
                                       f"util<={max_gpu_util_pct}%)"))

    return accepted, rejected


# ── High-level: discover + probe + filter ───────────────────────────────────


def _reset_jaynes():
    """Reset jaynes singleton state so the next config() call loads fresh."""
    from jaynes.jaynes import Jaynes
    Jaynes._raw_config = None
    Jaynes.launcher = None
    Jaynes.runner_config = None
    Jaynes.verbose = None
    Jaynes.mounts = []


def get_available_nodes(ctrl=CTRL_NODE, *, max_nodes=0,
                        min_free_gpu_mem_mb=0, max_gpu_util_pct=100,
                        max_storage_pct=100):
    """Discover idle SLURM nodes, verify SSH, probe resources, and filter.

    Assumes ``jaynes.config(config_path=...)`` has already been called by
    the caller to set up the runner/launch config.

    Prints status at each step.  Returns the list of nodes that pass all
    checks, or an empty list if none qualify.
    """
    print(f"Querying SLURM on {ctrl}...")
    jaynes.config(launch=dict(ip=ctrl))
    idle_nodes, down_nodes = Slurm.discover_nodes()

    if not idle_nodes:
        print(f"  down({len(down_nodes)}): {', '.join(down_nodes)}")
        print("\nNo idle nodes.")
        return []

    # SSH reachability (ControlMaster reuse handled by ~/.ssh/config)
    available, unreachable = [], []
    unreachable_reasons = {}
    for node in idle_nodes:
        reachable, reason = check_node_reachable(node)
        if reachable:
            available.append(node)
        else:
            unreachable.append(node)
            unreachable_reasons[node] = reason

    print(f"  ready({len(available)}):  {', '.join(available)}")
    if unreachable:
        print(f"  unreachable({len(unreachable)}):")
        for node in unreachable:
            print(f"    {node}: {unreachable_reasons[node]}")
    if down_nodes:
        print(f"  down({len(down_nodes)}):  {', '.join(down_nodes)}")

    if not available:
        print("\nNo reachable nodes.")
        return []

    # Probe resources on all reachable nodes in parallel
    print(f"\nProbing resources on {len(available)} node(s)...")
    resource_map = {}
    with ThreadPoolExecutor(max_workers=len(available)) as pool:
        futures = {pool.submit(probe_node_resources, node): node for node in available}
        for future in as_completed(futures):
            resource_map[futures[future]] = future.result()
    for node in available:
        print_node_resources(node, resource_map[node])

    # Report GPU validity, grouped by failure reason
    gpu_valid, gpu_invalid = [], []
    invalid_groups = {}  # reason -> [node, ...]
    for node in available:
        info = resource_map.get(node, {})
        if "error" in info:
            reason = info["error"]
            gpu_invalid.append(node)
            invalid_groups.setdefault(reason, []).append(node)
        elif not info.get("gpus"):
            reason = "no GPUs found"
            gpu_invalid.append(node)
            invalid_groups.setdefault(reason, []).append(node)
        else:
            gpu_valid.append(node)

    print(f"\nNode health check:")
    print(f"  valid({len(gpu_valid)}):   {', '.join(gpu_valid) if gpu_valid else '(none)'}")
    if gpu_invalid:
        print(f"  invalid({len(gpu_invalid)}):")
        for reason, nodes in invalid_groups.items():
            print(f"    {reason} ({len(nodes)}): {', '.join(nodes)}")

    # Drop nodes without working GPUs
    if gpu_invalid:
        available = [n for n in available if n in gpu_valid]
        if not available:
            print("\nNo nodes with valid GPUs.")
            return []

    # Filter
    has_filter = (min_free_gpu_mem_mb > 0
                  or max_gpu_util_pct < 100
                  or max_storage_pct < 100)
    if has_filter:
        print(f"\nFiltering: free_gpu_mem>={min_free_gpu_mem_mb}MB, "
              f"gpu_util<={max_gpu_util_pct}%, "
              f"storage<={max_storage_pct}%")
        available, rejected = filter_nodes_by_resources(
            available, resource_map,
            min_free_gpu_mem_mb=min_free_gpu_mem_mb,
            max_gpu_util_pct=max_gpu_util_pct,
            max_storage_pct=max_storage_pct,
        )
        for node, reason in rejected:
            print(f"  SKIP {node}: {reason}")
        if not available:
            print("\nNo nodes pass resource filters.")
            return []
        print(f"  passed({len(available)}): {', '.join(available)}")

    # Apply max_nodes limit after filtering so we pick from qualifying nodes
    if max_nodes > 0 and len(available) > max_nodes:
        available = available[:max_nodes]
        print(f"  using({len(available)}): {', '.join(available)}")

    return available


# ── Generic Work Queue Dispatcher ───────────────────────────────────────────


def dispatch(nodes, tasks, launch_fn, *, log_dir, config_path=None,
             log_prefix="task", poll_interval=1.0):
    """Dispatch tasks to nodes via jaynes with a work queue.

    Args:
        nodes: list of node hostnames.
        tasks: list of ``(task_id, payload)`` tuples.
        launch_fn(payload): called after ``jaynes.config()`` targets the node.
            Must call ``jaynes.run(...)`` and return the Popen pipe.
        log_dir: directory for per-task log files.
        log_prefix: filename prefix (e.g. "task", "trial").
        poll_interval: seconds between poll cycles.

    Returns list of dicts with keys: task_id, node, exit, elapsed.
    """
    os.makedirs(log_dir, exist_ok=True)

    queue = deque(tasks)
    active = {}  # node -> (pipe, task_id, start_time, log_file)
    completed = []

    def _assign(node):
        if not queue:
            return False
        task_id, payload = queue.popleft()
        log_path = os.path.join(log_dir, f"{log_prefix}_{task_id:03d}_{node}.log")
        log_file = open(log_path, "w")

        jaynes.config(config_path=config_path,
                      launch=dict(ip=node, stdout=log_file, stderr=log_file))
        pipe = launch_fn(payload)

        active[node] = (pipe, task_id, time.time(), log_file)
        print(f"[DISPATCHED] {log_prefix} {task_id:>3} -> {node}  (log: {log_path})")
        return True

    # Seed initial tasks
    for node in nodes:
        _assign(node)

    # Poll loop
    try:
        while active:
            for node in list(active.keys()):
                pipe, task_id, t_start, log_file = active[node]
                if pipe.poll() is None:
                    continue

                log_file.close()
                elapsed = time.time() - t_start
                status = "OK" if pipe.returncode == 0 else f"FAIL(exit={pipe.returncode})"
                print(f"  [DONE] {log_prefix} {task_id:>3} on {node} [{status}] ({elapsed:.1f}s)")

                completed.append({
                    "task_id": task_id,
                    "node": node,
                    "exit": pipe.returncode,
                    "elapsed": elapsed,
                })
                del active[node]
                _assign(node)

            if active:
                time.sleep(poll_interval)
    except KeyboardInterrupt:
        print(f"\n\nInterrupted — terminating {len(active)} remote task(s)...")
        for node, (pipe, task_id, t_start, log_file) in active.items():
            pipe.terminate()
            pipe.wait()
            log_file.close()
            print(f"  killed {log_prefix} {task_id} on {node}")
        active.clear()

    return completed
