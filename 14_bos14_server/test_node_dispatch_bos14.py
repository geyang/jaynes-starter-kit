#!/usr/bin/env python3
"""Test dispatching tasks across bos14 cluster nodes with a work queue.

Discovers idle nodes from SLURM via bos14-ctrl-000, then uses jaynes
to serialize and dispatch Python functions across available nodes.
When a node finishes, it picks up the next task from the queue.

Usage:
    python test_node_dispatch_bos14.py
    python test_node_dispatch_bos14.py --config.num-tasks 10
    python test_node_dispatch_bos14.py --config.max-nodes 3
    python test_node_dispatch_bos14.py --config.min-free-gpu-mem-mb 4000
    python test_node_dispatch_bos14.py --config.max-gpu-util-pct 50
    python test_node_dispatch_bos14.py --config.max-storage-pct 90
"""

import os
import time
from datetime import datetime

import jaynes
from params_proto import proto

from jaynes_utils import get_available_nodes, dispatch

# ── Configuration ────────────────────────────────────────────────────────────

CTRL_NODE = "bos14-ctrl-000"


@proto.cli
class Config:
    num_tasks: int = 6
    max_nodes: int = 0  # 0 = use all available
    min_free_gpu_mem_mb: int = 30000  # discard GPU if free memory < this (0 = no filter)
    max_gpu_util_pct: int = 50  # discard GPU if utilization > this (100 = no filter)
    max_storage_pct: int = 100  # discard node if storage usage > this (100 = no filter)


# ── Test Function (serialized by jaynes and run on remote) ──────────────────


def test_task(task_id, sleep_time):
    """This function runs on the remote node via jaynes.entry."""
    import os
    import socket
    import time

    host = socket.gethostname()
    print(f"[{host}] Task {task_id} started, pid={os.getpid()}")
    time.sleep(sleep_time)
    print(f"[{host}] Task {task_id} done after {sleep_time}s")


# ── Main ─────────────────────────────────────────────────────────────────────


@proto.cli
def main():

    print(f"{'='*60}")
    print(f"Node Dispatch Test (bos14) — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    config_path = os.path.join(os.path.dirname(__file__), ".jaynes.yml")

    # 1–4. Initialize jaynes, then discover, probe, and filter nodes via bos14-ctrl-000
    jaynes.config(config_path=config_path)
    available = get_available_nodes(
        ctrl=CTRL_NODE,
        max_nodes=Config.max_nodes,
        min_free_gpu_mem_mb=Config.min_free_gpu_mem_mb,
        max_gpu_util_pct=Config.max_gpu_util_pct,
        max_storage_pct=Config.max_storage_pct,
    )
    if not available:
        return 1

    # 5. Build tasks
    tasks = []
    for i in range(Config.num_tasks):
        sleep_time = 3 + (i % 3) * 2  # 3s, 5s, 7s, ...
        tasks.append({"id": i, "sleep": sleep_time})

    task_summary = [(t["id"], f"{t['sleep']}s") for t in tasks]
    print(f"\nTasks: {task_summary}")
    total_work = sum(t["sleep"] for t in tasks)
    max_task = max(t["sleep"] for t in tasks)
    ideal_time = max(max_task, total_work / len(available))
    print(f"Total work: {total_work}s across {len(available)} nodes "
          f"(ideal: {ideal_time:.0f}s)\n")

    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    dispatch_tasks = [(t["id"], t) for t in tasks]

    t0 = time.time()
    results = dispatch(
        available, dispatch_tasks,
        lambda t: jaynes.run(test_task, t["id"], t["sleep"]),
        log_dir=log_dir,
        config_path=config_path,
    )
    wall_time = time.time() - t0

    # 7. Summary
    ok = sum(1 for r in results if r["exit"] == 0)
    print(f"\n{'='*60}")
    print(f"Done: {ok}/{len(results)} succeeded in {wall_time:.1f}s "
          f"(ideal: {ideal_time:.0f}s, overhead: {wall_time - ideal_time:.1f}s)")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
