# Setup Guide on Harvard FAC Canon Cluster

Summary:

- using singularity with our own docker images
- getting to work fast without setting up the environments

## Official Guides from FAS

- quick start guide: https://docs.rc.fas.harvard.edu/kb/quickstart-guide/#Familiarize_yourself_with_proper_decorum_on_the_cluster
- software modules: https://docs.rc.fas.harvard.edu/kb/quickstart-guide/#Software_Modules
- understanding the limitations and trade-offs of each storage options is key in HPC usage. See this guide for details: https://docs.rc.fas.harvard.edu/kb/quickstart-guide/#Determine_where_your_files_will_be_stored

## A Singularity-based Setup

The NFS file system on the Canon cluster is quite slow. To avoid a time-consuming setup, we opt to use singularity containers that are built-off docker container images as our standard dev environement.

The required readings on singularity is below:

- the FAS guide: https://docs.rc.fas.harvard.edu/kb/singularity-on-the-cluster/
- singularity quick start guide: https://sylabs.io/guides/3.0/user-guide/quick_start.html#shell
- how to specify custom location for the images: https://pawseysc.github.io/singularity-containers/12-singularity-intro/index.html

Singularity is only availabel on the worker nodes. This is likely because the admins do not want users to be building container images on the login nodes. To run singularity, first request a machine:

```bash
salloc -p test -c 1 -t 00-01:00 --mem=4000
```

**To pull from private docker accounts, use the `--docker-login` option**: 

```bash
singularity pull --docker-login docker://improbableailab/model-free
```

**Now to run a shell with this image:**

```bash
singularity exec model-free_latest.sif python -c "import torch; print(torch.cuda.is_available())"
```

This is going to print out `False` because the instance is not requested with GPU and singularity is missing the `--nv` option.

**GPU Singularity Example:**  First start a GPU instance

```bash
salloc -p gpu --gres=gpu:1 --mem 1000 -n 4 -t 600
```

**Now launch the singularity container with the gpu binding**. Note that the `--nv` flag is *critical* for accessing the GPU front within the container.

```bash
singularity exec --nv model-free_latest.sif python -c "import torch; print(torch.cuda.is_available())"
```

```stdout
>>> True
```



### Setting Up Singularity Images on Canon

To use singularity, we overload the `bash` command in the `jaynes.runners.Slurm` mode, with a custom script:

- To get your lab group:

    ```bash
    id -ng $USER
    ```

    This should output something ends with `xxxx_lab`.

- **.jaynes.yml** config:

    ```yaml
    runner: !runnes.Slurm
        shell: ./srun-singularity.sh /n/holyscratch01/<your-lab>/$USER/singularity/model-free_latest.sif
    ```

- **./srun-singularity.sh** script:  Place this script inside the `launch.launch_dir` specified in our `jaynes.Launcher`. 

    ```bash
    #!/bin/bash
    singularity exec --nv $1 bash -c "$3"
    ```

This should allow you to run singularity images with `srun`.



## Final Notes

Using singularity with docker containers greatly simplifies 

