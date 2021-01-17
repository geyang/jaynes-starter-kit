# Example Projects for Jaynes

In this folder, we provide a collection of example configurations. Each example sits
within its own folder. To run, follow the instruction in the README in that example
project.

```
01_ssh_docker_configuration
├── README.md
├── launch_entry.py
└── jaynes.yml
```
## Table of Contents

For detailed documentation on each usecases, refer to the in-dept tutorial bellow: 

3. [**Multiple SSH Reacheable Machines**](03_multiple_ssh_reacheable_machines)
4. [**Compute at Scale with SLRUM & Jaynes**](04_slurm_configuration)
5. [**Advanced Multi-mode Example**](05_muti-mode_advanced_config)
4. [**SSH Docker Configuration**](01_ssh_docker_configuration)
5. [**EC2 Docker Configuration**](02_ec2_docker_configuration)

## Reporting Issues (on the [Jaynes Repo/issues](https://github.com/geyang/jaynes/issues))

Let's collect all issues on the [main `jaynes` repo's issue page](https://github.com/geyang/jaynes/issues), so that
people can search for things more easily!

## How to Debug

`Jaynes` offer a way to transparently debug the launch via `verbose` mode, where it prints out all of the local and remote script that it generates. To debug a launch script, set `verbose` to `true` either in the yaml file, or through the `jaynes.config` call. To debug in the remote host where you intend to run your job, you can often copy and paste the generated script
to see the error messages.

**Debugging Steps:**

1. **Turn on verbose mode**, by setting `verbose=True` in the jaynes call

  ```python
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
  jaynes.run(train_fn)
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

Below are a few areas that current stands in need to contributions:

- [**Documentation on Configuration Schema** issue #2](issues/2)
- [**GCE Support** issue #3](issues/3)
- [**Pure SSH Host Support** issue #4](issues/4)
- [**SLURM SBatch Support** issue #5](issues/5)
- [**SLURM Singularity Support** issue #6](issues/6)


