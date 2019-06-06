# Launching on Remote Server via SSH with `Jaynes`

This folder contains a working example for launching jobs with docker on multiple remote 
work stations via ssh, with subscription to all of the tty pipe-backs.

result looks like:

![./figures/multi-ssh-mode.png](./figures/multi-ssh-mode.png)

## Getting Started

You need to have `awscli` installed on your computer, plus `jaynes`. `boto3` is needed for launching `ec2` jobs, but it is not needed in this example.
```bash
pip install awscli jaynes
```

The experiment script looks like the following:

```python
import jaynes

if __name__ == "__main__":

    jaynes.config(mode='hodor')
    jaynes.run(launch)

    # try below
    jaynes.config(mode='oberyn')
    jaynes.run(launch)

    # try run locally!
    jaynes.config(mode='local')
    jaynes.run(launch)

    # this line allows you to keep the pipe open and hear back from the remote instance.
    jaynes.listen()
```

`hodor` and `oberyn` are two different machines. As you can see in the 
screenshot bellow, the local result gets print first. Then then hodor:

![./figures/multi-ssh-mode.png](./figures/multi-ssh-mode.png)

Because `oberyn` is down, the ssh remote call failed for that instance.

