# BOS14 Server — Node Dispatch with Jaynes

Dispatch Python tasks across the BOS14 SLURM cluster using [jaynes](https://github.com/geyang/jaynes). This example discovers idle nodes, probes GPU/storage resources, filters by configurable thresholds, and runs a work-queue dispatcher that automatically assigns tasks to freed nodes.

### Prerequisites

- SSH access to the BOS14 cluster — you must be able to connect directly from your terminal:

  ```bash
  # Control node
  ssh bos14-ctrl-000

  # Compute nodes (node names like bos14-node-001, bos14-node-002, etc.)
  ssh bos14-node-001
  ```

### Installation

**use the `cambridge_server` branch.**
```bash
# Clone jaynes and switch to the correct branch
git clone https://github.com/geyang/jaynes.git
cd jaynes
git checkout cambridge_server
```

The `pyproject.toml` expects jaynes as a local editable install. Update the path in `[tool.uv.sources]` to point to your local jaynes checkout:

```toml
[tool.uv.sources]
jaynes = { path = "/path/to/your/jaynes", editable = true }
```

### Configuration

Edit `.jaynes.yml` to match your environment:


### Usage

```bash
uv run python test_node_dispatch_bos14.py
```


