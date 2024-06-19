# [Jaynes Examples: Cross-Provider Computation at Scale](https://github.com/geyang/jaynes-starter-kit)

This repository is an up-to-date collection of minimal jaynes usage examples. You can mix and match configurations between these included usecases for your particular infrastructure. You can find the up-to-date copy of this guide here: https://github.com/geyang/jaynes-starter-kit

## To Get Started

First let's install Jaynes! This tutorial is written w.r.t version: [0.7.2](https://github.com/geyang/jaynes/releases/tag/0.7.2)

```bash
pip install jaynes
```

I would also recommend taking a look at [params-proto](https://github.com/geyang/params_proto), which is a pythonic  hyperparameter + argparsing library that makes parameter management declaritive and error-free. We use params-proto and its sweep utility, `params_proto.hyper` in our parameter sweep example. To install params-proto, run

```bash
pip install params-proto waterbear
```

## Table of Contents

For detailed documentation on each usecases, refer to the in-dept tutorial bellow. Each folder contains a complete example. To run, follow the instruction in the README.

```
01_ssh_docker_configuration
├── README.md
├── launch_entry.py
└── .jaynes.yml
```

- **SSH Launch Modes**
    0. [**SSH Reachable Workstations**](00_ssh_reachable_machine/README.md)
    1. [**SSH + Tmux | Persisting Your Runs**](00_ssh_tmux_reachable_machine/README.md)
    2. [**Switching Between Machines via SSH**](03_multiple_ssh_reacheable_machines/README.md)
    3. [**Using Docker Container**](01_ssh_docker_configuration/README.md)
- **Working with Diverse Compute Resources**
    4. [**Advanced Multi-mode Example**](05_muti-mode_advanced_config/README.md)
- **SLURM**
    4. [**Compute at Scale with SLRUM & Jaynes**](04_slurm_configuration/README.md)
    5. [**Guide for MIT Supercloud**](07_supercloud_setup/README.md)
    6. [**Using SBATCH Mode with SLUR**](09_sbatch_mode/README.md)
    7. [**Using `mpirun`**](08_using_mpirun/README.md)
- **AWS**
    8. [**SSH Docker Configuration**](01_ssh_docker_configuration/README.md)
    9. [**EC2 Docker Configuration**](02_ec2_docker_guide/README.md)
- **GCP**
    10. [**GCP Docker Example**](10_gcp_docker_example/README.md)
- **God Mode**
    11. [**Jaynes Manager Server**](06_jaynes_manager/README.md)


## Reporting Issues (on the [Jaynes Repo/issues](https://github.com/geyang/jaynes/issues))

Let's collect all issues on the [main `jaynes` repo's issue page](https://github.com/geyang/jaynes/issues), so that
people can search for things more easily!

## How to Debug

`Jaynes` offer a way to transparently debug the launch via `verbose` mode, where it prints out all of the local and remote script that it generates. To debug a launch script, set `verbose` to `true` either in the yaml file, or through the `jaynes.config` call. To debug in the remote host where you intend to run your job, you can often copy and paste the generated script
to see the error messages.

**Debugging Steps:**

1. **Turn on verbose mode**, by setting `verbose=True` in the jaynes call

  ```python
  #! launch_entry.py
  import jaynes
  
  jaynes.config(verbose=True)
  ```

  or 

  ```yaml
  #! .jaynes.yml
  verbose: true
  runner:
  - ....
  ```

2. **Launch**

  ```python
  #! launch_entry.py
  if __name__ == "__main__":
      jaynes.run(train_fn, *args, **kwargs)
   
  # if in SLURM or SSH mode:
  jaynes.listen()  # to listen to the stdout/stderr pipe-back
  ```

3. **Debug** Suppose you have an error message. You can copy and paste the script ran
   by `jaynes`, that is printed out in the console either locally or on the EC2 instance
   you just launched to debug the specifics of it.

4. **Share with Lab mates** When you are done, you can share this repo with others
   who use the same infrastructure, so that they can run their code there too.

## Call for Contributors

Machine Learning infrastructure is an evolving problem, and would take
the rest of the community to maintain, adopt and standardize.

Below are a few areas that current stands in need to contributions: (now mostly done)

- [**done**] - [**Documentation on Configuration Schema** issue #2](issues/2)
- [**done**] - [**GCE Support** issue #3](issues/3)
- [**done**] - [**Pure SSH Host Support** issue #4](issues/4)
- [**done**] - [**SLURM SBatch Support** issue #5](issues/5)
- [**SLURM Singularity Support** issue #6](issues/6)

