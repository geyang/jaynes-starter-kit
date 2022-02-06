# Getting `mujoco-py` to work on M1 Mac

Issue [#662](https://github.com/openai/mujoco-py/issues/662) is getting a bit mangled, so here is a working script that worked for me.  A copy of this guide can be found at [jaynes-starter-kit/docker/m1_mac_setup](https://github.com/geyang/jaynes-starter-kit/blob/master/docker/m1_mac_mujoco_setup.md). This is adapted from @wookayin's script. The most crucial part for me is to use `sudo` to link the framework to the `/usr/local/lib` folder. Without this step, it did not work. @nikhilweee's comment confirms this.

Another key step is to remove the mujoco-py installation with a clean `rm -rf .../site-packages/mujoco-py`. This way the compiled binaries can be removed.


## Background

Mujoco-py currently does not support `mujoco2.1.1`. The first arm64 release, which is needed for M1 Macs, came out a few weeks ago. Therefore `mujoco2.1.1` is needed in order to run MuJoCo natively on the M1 Mac.

## Pre-requisits:

- make sure you use `Miniforge` as your Conda environment
- install `glfw` via `brew install glfw`. **Note the location for the installation**
- download MuJoCo2.1.1 image that ends with a `*.dmg`. The new `mujoco2.1.1` is released as a Framework. You can copy the `MuJoCo.app` into `/Applications/` folder.

## Installation Script

Make a file locally called `install-mujoco.sh`, and put the following into it.

```bash
mkdir -p $HOME/.mujoco/mujoco210
ln -sf /Applications/MuJoCo.app/Contents/Frameworks/MuJoCo.framework/Versions/Current/Headers/ $HOME/.mujoco/mujoco210/include

mkdir -p $HOME/.mujoco/mujoco210/bin
ln -sf /Applications/MuJoCo.app/Contents/Frameworks/MuJoCo.framework/Versions/Current/libmujoco.2.1.1.dylib $HOME/.mujoco/mujoco210/bin/libmujoco210.dylib
sudo ln -sf /Applications/MuJoCo.app/Contents/Frameworks/MuJoCo.framework/Versions/Current/libmujoco.2.1.1.dylib /usr/local/lib/

# For M1 (arm64) mac users:
# brew install glfw
ln -sf /opt/homebrew/lib/libglfw.3.dylib $HOME/.mujoco/mujoco210/bin

# remove old installation
rm -rf /opt/homebrew/Caskroom/miniforge/base/lib/python3.9/site-packages/mujoco_py

# which python
# exit

export CC=/opt/homebrew/bin/gcc-11         # see https://github.com/openai/mujoco-py/issues/605
pip install mujoco-py && python -c 'import mujoco_py'
```