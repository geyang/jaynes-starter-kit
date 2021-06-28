# Using `mpirun` on cluster

You can replace the `python -m jaynes.entry` entry point with `mpirun python -m jaynes.entry`.

```python
def mpi_import():
    print('now import MPI')
    from mpi4py import MPI
    from ml_logger import logger

    logger.print(MPI, "success!", color="green")


if __name__ == "__main__":
    import jaynes

    jaynes.config(runner=dict(entry_script="mpirun python -u -m jaynes.entry"))
    jaynes.run(mpi_import)
    jaynes.listen()
```

Using the following configuration:

```yaml
version: 0
run:
  mounts: []
  runner: !runners.Slurm
    envs: >-
      LC_CTYPE=en_US.UTF-8 LANG=en_US.UTF-8 LANGUAGE=en_US
    setup: |
      source /etc/profile.d/modules.sh
      module load anaconda/2021a
      module load mpi/openmpi-4.0
    mem: 1000
    n_cpu: 1
    n_gpu: volta:1
  launch: !ENV
    type: ssh
    ip: "{env.JYNS_SLURM_HOST}"
    username: "{env.JYNS_USERNAME}"
    pem: "{env.JYNS_SLURM_PEM}"
```

