# Using Singularity on Supercloud

To use singularity, we overload the `bash` command in the `jaynes.runners.Slurm` mode, with a custom script:

**.jaynes.yml** config:

```yaml
runner: !runnes.Slurm
    shell: ./srun-singularity.sh $HOME/escher_shared/singularity/model-free_latest.sif
```

**./srun-singularity.sh** script:  Place this script inside the `launch.launch_dir` specified in our `jaynes.Launcher`. 

```bash
#!/bin/bash
singularity exec --nv $1 bash -c "$3"
```

## Pulling and Building Singularity Images from DockerHub

The NFS system on the supercloud has file-lock disabled for performance reasons. To avoid the file-lock error, we can set the `TMPDIR` environment variable to the local disc on the login node, so that the singularity build can happen without error.

**Important** We place the singularity images in side our shared directory: `$HOME/$escher_shared`, so that the team members do not need to re-pull and build their own images. 

```bash
mkdir -p /state/partition1/user/$USER
export TMPDIR=/state/partition1/user/$USER

mkdir -p $HOME/escher_shared/singularity
cd escher_shared/singularity
singularity pull --docker-login docker://improbableailab/model-free
```



