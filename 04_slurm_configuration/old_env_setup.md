# Setting up Env Variables [Older Version] 

**Important**: we have moved to `.secret` files instead. Refer to the [README](README.md) for details.

This example assumes that you can access a remote SLURM cluster via ssh. **First, make sure** ssh works:

```bash
ssh $JYNS_USERNAME@$JYNS_SLURM_HOST -i $JYNS_SLURM_PEM
```
to do so, you need to configure these in your environment script `./bashrc`

```bash
export JYNS_SLURM_HOST=/*your slurm cluster login node*/
export JYNS_USERNAME=/*your username*/
export JYNS_SLURM_PEM=~/.ssh/<*your rsa key*>
export JYNS_SLURM_DIR=/home/gridsan/geyang/jaynes-mount
```

> password login are usually disabled on managed SLURM clusters.

**Second, install `jaynes`.** This tutorial is written w.r.t version: [0.7.2](https://github.com/geyang/jaynes/releases/tag/0.7.2).
