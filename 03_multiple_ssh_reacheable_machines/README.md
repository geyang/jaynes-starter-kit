# Launching on Remote Server via SSH with `Jaynes`

This folder contains a working example for launching jobs with docker on multiple remote 
work stations via ssh, with subscription to all of the tty pipe-backs.

result looks like:

![./figures/multi-ssh-mode.png](./figures/multi-ssh-mode.png)

## Getting Started

This example assumes that you can assess a remote Linux machine via a username and a password. First, install jaynes. This tutorial is written w.r.t version: [v0.6.0-rc14](./releases/v0.6.0-rc14)

```bash
pip install jaynes==0.6.0-rc14
```

 

This folder is structured as:

```bash
03_multiple_ssh_reacheable_machines
├── README.md
├── figures
└── launch_entry.py

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

