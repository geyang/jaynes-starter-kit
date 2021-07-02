# Launching on Remote Server via SSH with `Jaynes`

<a href="./figures/output.png" target="_blank"><img src="./figures/output.png" alt="single_launch" align="right" width="600px" style="top:20px"></a>

This folder contains a working example for launching jobs without docker on multiple remote work stations via ssh, with subscription to all of the tty pipe-backs.

result looks like figure to the right: 👉

## Getting Started

This example assumes that you can assess a remote Linux machine via a username and a password. 

**First, install miniconda, and python 3.7 (or below)**. The cloundpickle module supports python 3.7 and below, which is different from the latest miniconda distribution. So you can install using this url

```bash
curl -O https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.3-Linux-x86_64.sh
bash Miniconda3-py37_4.8.3-Linux-x86_64.sh
```

Follow the instruction, then verify that it as installed successfully via

```bash
conda env
>> *base     $HOME/your-username/miniconda3
```

**Second, install jaynes** and other dependencies you need for your project. This tutorial is written w.r.t version: [v0.7.2](https://github.com/geyang/jaynes/releases/tag/v0.7.2)

```bash
pip install jaynes==0.7.2
```

## Overview of This Example

This folder is structured as:

```bash
03_multiple_ssh_reacheable_machines
├── README.md
├── figures
├── launch_entry.py
└── multi_launch.py
```

Where the main file contains the following

```python
import jaynes

def train_fn():
    from time import sleep

    for i in range(10):
        print(f"step: {i}"); sleep(0.1)
    print('Finished!')

if __name__ == "__main__":
    jaynes.config(verbose=False)
    jaynes.run(train_fn)

    jaynes.listen(200)
```

### Mode 1: Plain Password

Set the following environment parameters in your `~/.bashrc` file:

```bash
export JYNS_USERNAME=/*your username*/
export JYNS_PASSWORD='/*your password*/'  # use '' if contain [!]
export JYNS_DIR=/*path to the NFS you have access to*/
```

### Mode 2: Private Key

If you access the machine using a privte key instead change the `.jaynes.yml` file by replacing the `host.password` field with `host.pem: /*path to your pem key*/;` instead.

```yaml
  vision01: &vision01
    ip: vision01
    username: "{env.JYNS_USERNAME}"
    # remove this line from the config file
    # password: "{env.JYNS_PASSWORD}"
    pem: ~/.ssh/your-public-key
    launch_dir: {env.JYNS_DIR}/jaynes-demo/{now:%Y-%m-%d}/{now:%H%M%S.%f}
```

## Managing Python Environments on Server

Setup a conda environment on the server, and then install jaynes in that python environment: we use `jaynes.entry` module to bootstrap the python runtime. In this example, we use the `base` environment that comes with each conda installation.

```bash
conda activate base
pip install jaynes
```

The launch `.jaynes.yml` file contains the following values for configuring the remote python runtime:

```yaml
setup: |
  . $HOME/lfgr.env
  conda activate base
envs: >-
  LANG=utf-8
  LC_CTYPE=en_US.UTF-8
  LD_LIBRARY_PATH=$HOME/.mujoco/mujoco200/bin:$LD_LIBREARY_PATH
  PYTHONPATH=`which python`:$PYTHONPATH
pypath: "{mounts[0].host_path}"
work_dir: "{mounts[0].host_path}"
```

## Overriding the Config File (and Launch Across Machines)

In the [./multi_launch.py](./multi_launch.py) script, we automatically distribute the launch across multiple machines. This script shows the pattern for overwriding the configuration file:

```python
#! ./multi_launch.py
import jaynes

from launch_entry import train_fn

if __name__ == "__main__":
    hosts = [
        'visiongpu001',
        'visiongpu002',
        'visiongpu003',
    ]

    for host in hosts:
        jaynes.config(verbose=False, launch=dict(ip=host))
        jaynes.run(train_fn)

    jaynes.listen(200)
```

You should see the output stream from all three machines combined in the stdout.

## On Running Tensorflow

In rare occations (for example at CSAIL), if you install tensorflow via `pip` sometimes it gives `Illegal Instructions` fault during import. If this happens for any reason, you should switch to a conda installation. This nasty issue raises its head here and [there](https://github.com/tensorflow/tensorflow/issues/40978) without a clear solution except the following:

**First, make sure you remove tensorflow from everywhere possible**. This includes `~/.local`, **and** your conda's `site-packages`. (some times it is installed at both locations). After manually checking for these locations, install using conda. Note that conda installation can be quite slow:

```bash
yes | pip uninstall tensorflow
conda install --use-local tensorflow=2.3.1  # notice only one "="
```





## Issues and Questions?

Please report issues or error messages in the issues page of the main `jaynes` repo: [jaynes/issues](https://github.com/geyang/jaynes/issues). 

Happy Researching!  :heart:
