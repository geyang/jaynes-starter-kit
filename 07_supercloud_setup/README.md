# Setup Guide on MIT Supercloud

### Before You Start
Frist, take a look at the [04 slurm setup guide](../04_slurm_configuration/README.md)**. That guide tells you how to get up and running with python. The following steps cover specific libraries needed for reinforcement learning.

### Note on Proxy
Outbound HTTP requests are blocked on the workers nodes, which means you can not run pip install or send logging request to our ec2 instrumentation server. The admins have kindly offered us a way to setup proxy servers. [[Proxy Setup Supercloud]](proxy_setup_supercloud.md)

### Old Note (pre 20220818)
Outbound HTTP requests are blocked on the workers nodes, which means you can not run pip install or send logging request to our ec2 instrumentation server. See [[link]](proxy_setup.md)




## High-level Guidelines

1. avoid using custom conda. The default conda environment is automatically copied to all workers, making the load a lot faster. Custom torch installation can take up to 30 s to load.
2. openai `mujoco-py` currently support 210 and below. `2.1.1` is not yet supported.
3. dm_control supports `2.1.1`
4. worker nodes have no access to the internet at large. to log to dash.ml, see [[link]](proxy_setup_supercloud.md)

This guide is provided as-is. If you want to install newer versions of the packages, please help update this guide so that others can build upon your work.

At the end of this tutorial, you should have the following in your `~/.bashrc` file:

```bash
# Just system text encoding
export LC_CTYPE=en_US.UTF-8 LANG=en_US.UTF-8 LANGUAGE=en_US

# Needed for MuJoCo-py
export LD_LIBRARY_PATH=$HOME/.mujoco/mujoco210/bin:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/nvidia
# dynamically link custom installation
export PYTHONPATH=$PYTHONPATH:/state/partition1/user/$USER/mujoco-py

# Needed for mujoco-py compilation using custom glew
export C_INCLUDE_PATH=$C_INCLUDE_PATH:$HOME/vendor/glew/include
# Needed for GLEW rendering with mujoco-py
export MUJOCO_GL=egl
export LD_PRELOAD=$HOME/vendor/glew/lib/libGLEW.so.2.2.0:/usr/lib/x86_64-linux-gnu/libEGL.so

# Needed for DeepMind control (dm_control)
export MJLIB_PATH=$HOME/.mujoco/mujoco-2.1.1/lib/libmujoco.so
```



## Setting up DeepMind Control

Setting up dm_control is relatively easy. **Note: you need the master from dm_control for mujoco-2.1.1**. The most up-to-date release won't do (**date: 2022-01-02**).

```bash
pip install gym --no-deps
pip install gym-dmc
pip install git+git://github.com/deepmind/dm_control.git
```

Now install `mujoco-2.1.1`

```bash
mkdir -p $HOME/.mujoco 
wget https://github.com/deepmind/mujoco/releases/download/2.1.1/mujoco-2.1.1-linux-x86_64.tar.gz -O mujoco.tar.gz
tar -xf mujoco.tar.gz -C $HOME/.mujoco
rm mujoco.tar.gz
```

Note that mujoco-py won't work with this version, but dm_control does. Now, add the following to your `.bashrc`

```bash
export MJLIB_PATH=$HOME/.mujoco/mujoco-2.1.1/lib/libmujoco.so
```

`dm_control` rendering should work now. You can test that this works via the following script:

```python
def gym_dmc_render():
    import gym
    from ml_logger import logger

    env = gym.make("dmc:Cartpole-balance-v1")
    logger.print(f"dmc Cartpole starts!", color="green")
    img = env.render('rgb_array')
    logger.print(f"dmc:Cartpole renders <{img.shape}>", color="green")
```

The [[launch_entry.py]](launch_entry.py) file automatically tests this on supercloud. You can run it to test it out.





## Setting up `mujoco-py`

**Summary:** `mujoco-py` at this moment (2022-01-02) still does not support `mujoco-2.1.1` (see this issue [[#662: Support MuJoCo 2.1.1]](https://github.com/openai/mujoco-py/issues/662)). Therefore you need to install both mujoco-200 for mujoco-py, and `mujoco-210` for DeepMind control.

**Key issue is compiling mujoco-py with mujoco-210 on EGL version of GLEW**. We will do this in three steps:

1. install GLEW and compile with a `SYSTEM=linux-egl` flag.
2. `LD_PRELOAD` the EGL version of the library
3. Include `GL/glew.h` headers from our custom installation path during the mujoco-py compilation.

See detailed steps below:

### Step-1: Installing GLEW for GPU accelerated rendering

You need to install `glew` directly from source, and compile using the `linux-egl` flag. This is required in order for mujoco to render with EGL. For details, see this issue: [[EGL OpenGL headless rendering]](https://roboti.us/forum/index.php?threads/egl-opengl-headless-rendering.3588/).

```bash
mkdir ~/vendor
cd ~/vendor
wget https://github.com/nigels-com/glew/releases/download/glew-2.2.0/glew-2.2.0.zip     
unzip glew-2.2.0.zip
mv glew-2.2.0 glew
cd glew
# This is key
make SYSTEM=linux-egl
```

Then add the following into your `startup` or `envs` part of the config in jaynes:

```bash    
export MUJOCO_GL=egl;
export LD_PRELOAD=$HOME/vendor/glew/lib/libGLEW.so.2.2.0:/usr/lib/x86_64-linux-gnu/libEGL.so;
```

Note that we are using the **EGL** version of the driver: `/usr/lib/x86_64-linux-gnu/libEGL.so`. Without this, you will get a "RuntimeError: Failed to initialize OpenGL" error.


### Step-2: Downloading and Setting up `mujoco-210`

Let's install mujoco 210 because `mujoco-py` does not work with `2.1.1` yet.

```bash
# Download mujoco
mkdir -p $HOME/.mujoco 
wget https://mujoco.org/download/mujoco210-linux-x86_64.tar.gz -O mujoco.tar.gz
tar -xf mujoco.tar.gz -C $HOME/.mujoco
rm mujoco.tar.gz
```

And then in your ~/.bashrc file you  need to have the following

```bash
export LD_LIBRARY_PATH=$HOME/.mujoco/mujoco210/bin:$LD_LIBRARY_PATH
```

### Step-3: Installing `mujoco-py` into Worker Node's Local Storage


If you run 

```bash
pip install --user mujoco-py
```

it will raise an error that says:

```bash
RuntimeError: Unable to acquire lock on `b'/home/gridsan/geyang/.local/lib/python3.8/site-packages/mujoco_py-2.1.2.14-py3.8.egg/mujoco_py/generated/mujocopy-buildlock'` due to [Errno 38] Function not implemented
```

**Why does this happen?** So what’s going on here is that mujoco uses file locking, which can cause a lot of performance issues, particularly on shared file systems. For that reason it’s disabled on the Lustre Shared Filesystem that we have the home directories. Luckily each node has its own local filesystem where file locking is not disabled, so there is a workaround. 

---

**Important Note**: 
Your should add the following to your `~/.bashrc` file in supercloud at the **beginning** of the file, **before** the non-interactive session escape (which is the first few lines). This is because the default `bashrc` default to not doing anything and exists after the first command, as soon as it detects a non-interactive session.
```bash
export PYTHONPATH=$PYTHONPATH:/state/partition1/user/$USER/mujoco-py
# These are needed for mujoco-py to compile
export MUJOCO_GL=egl
export C_INCLUDE_PATH=$C_INCLUDE_PATH:$HOME/vendor/glew/include
# This is needed for OpenGL to initialize Properly
export LD_PRELOAD=$HOME/vendor/glew/lib/libGLEW.so.2.2.0:/usr/lib/x86_64-linux-gnu/libEGL.so
```
   
Now install `mujoco-py` **(specific to the MIT Supercloud cluster)**:

   
Full script:

```bash
mkdir /state/partition1/user/$USER -p
rm -rf /state/partition1/user/$USER/mujoco-py

wget https://github.com/openai/mujoco-py/archive/refs/tags/v2.1.2.14.tar.gz
tar -xf v2.1.2.14.tar.gz -C /state/partition1/user/$USER/mujoco-py

cd /state/partition1/user/$USER/mujoco-py
module load anaconda/2021b
python setup.py install --user

cp -r /state/partition1/user/$USER/mujoco-py /home/gridsan/$USER/
```
   
Then check if the installation succeeds by 

```bash
pip show mujoco_py
```
**Important** this shall not fail. If this fails, there is something wrong.

- **Important Note 1:** The last line copies the installation directory back to your home directory. You can do this after running `mujoco-py` once, so that your worker does not have to re-compile every single time it runs.
- **Important Note 2:** the '/' at the end is important -- it means putting the `mujoco-py` folder **under** the `$USER` 

```bash
cp -r /state/partition1/user/$USER/mujoco-py /home/gridsan/$USER/
```

Since each node on the system has its own local filesystem, compute nodes won’t be able to see what’s on the login node local filesystem. So what we’ll do is copy the mujoco install to the local filesystem at the start of the job. I’ve written a setup.sh script that will check to see if it’s already been copied, and copy it over if not. I also have the start of a submission script, you’ll have to put in the name of your python script and any other scheduler options you need. (edited)


In your `.jaynes.yml` file, add the following segment to the `startup` entry. This is ran inside the the worker machine. `setup` happens in the login node instead.

```bash
starup: >-
    mkdir -p /state/partition1/user/$USER;
    echo "copying mujoco-py";
    cp -r /home/gridsan/$USER/mujoco-py /state/partition1/user/$USER/;
    echo "finished";
```

For the complete setup, take a look at the `.jaynes.yml` file in this folder. It works.

