# Launching on Remote Server via SSH + TMux

This folder contains a working example for launching jobs on a remote workstation via ssh and tmux.

**Important** You won't see the `stdout` from this example. We can not run tmux in non-daemon mode
because it requires a tty.

## Note:

`jaynes` uses gnu-tar and an updated version of rsyn on Mac OS. To install these, run
```bash
brew install gnu-tar
brew install rsync
```
