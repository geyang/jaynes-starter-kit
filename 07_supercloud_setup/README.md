# Setup Guide on MIT Supercloud

**Note** outbound HTTP requests are blocked on the workers nodes, which means you can not run pip install or send logging request to our ec2 instrumentation server. See [[link]](proxy_setup.md)

## Setting up MuJoCo-py (for gym)

**Summary:** First install mujoco (step 1 below), and then add the following to your `~/.bashrc` 

```bash
export MJKEY_PATH=$HOME/.mujoco/mujoco200/mjkey.txt
# These are required for mujoco-py installation
export MUJOCO_PY_MJPRO_PATH=$HOME/.mujoco/mujoco200/
export MUJOCO_PY_MJKEY_PATH=$HOME/.mujoco/mujoco200/mjkey.txt
# These are required for GPU-accelerated rendering
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/.mujoco/mujoco200/bin
export MUJOCO_GL=egl
# this is required my dm_control but Ge does not rememeber.
export MJLIB_PATH=$HOME/.mujoco/mujoco200/bin/libmujoco200.so
# the reason for this see the detailed setup below
export PYTHONPATH=$PYTHONPATH:/state/partition1/user/$USER/mujoco-py
```

**Detailed setup steps** see below: 


1. install mujoco

   ```bash
   # Download mujoco
   mkdir $HOME/.mujoco
   cd $HOME/.mujoco
   curl -O https://www.roboti.us/download/mujoco200_linux.zip
   unzip mujoco200_linux.zip
   ```

   And then in your ~/.bashrc file you  need to have the following

   ```bash
   export LD_LIBRARY_PATH $LD_LIBRARY_PATH:$HOME/.mujoco/mujoco200_linux/bin
   export MUJOCO_PY_MJPRO_PATH $HOME/.mujoco/mujoco200_linux
   export MJLIB_PATH $HOME/.mujoco/mujoco200_linux/bin/libmujoco200.so
   export MJKEY_PATH $HOME/.mujoco/mjkey.txt
   ```

2. Installing `mujoco-py` **(specific to the MIT Supercloud cluster)**:

   If you run 

   ```bash
   pip install --user mujoco-py
   ```

   it will raise an error that says:

   - [ ] add error
   - [ ] add link to github issue.

   What’s going on is mujoco uses file locking, which can cause a lot of performance issues, particularly on shared file systems. For that reason it’s disabled on the Lustre Shared Filesystem that we have the home directories. Luckily each node has its own local filesystem where file locking is not disabled, so there is a workaround. I’ve had someone run into this before, here is what I sent her as a workaround (along with some handy scripts to get you started). Let us know if you run into any problems or you have any questions.To do this you’ll need a copy of the source code (I’m grabbing the latest release from the github repo, you can pick a different release here if you want https://github.com/openai/mujoco-py/releases, right click on a “Source Code (tar.gz)” link and select “Copy link address” to get the URL for a different release):

   ```
   wget https://github.com/openai/mujoco-py/archive/v2.0.2.5.tar.gz
   tar -xzf v2.0.2.5.tar.gz
   mv mujoco-py-2.0.2.5 mujoco-py
   ```

   (this creates a directory mujoco-py-2.0.2.5 and renames it for simplicity later)Then you’ll need to do the build in the local filesystem on the login node. This will make sure all the paths are set properly.Make a directory under /state/partition1/user/ with your username:

   ```bash
   mkdir /state/partition1/user/$USER 
   ```

   Then copy the mujoco-py folder there and go to that directory:

   ```bash
   cp -r /home/gridsan/$USER/mujoco-py /state/partition1/user/$USER
   cd /state/partition1/user/$USER/mujoco-py 
   ```

   Build/install the package (use whichever anaconda module you’d like):

   ```bash
   module load anaconda/2021a
   python setup.py install --user
   ```
   Then check if the installation succeeds by 

   ```bash
   pip show mujoco_py
   ```

   **Important** this shall not fail. If this fails, there is something wrong.``

   Now copy this directory back to your home directory: 

   **Important:** the '/' at the end is important -- it means putting the `mujoco-py` folder **under** the `$USER` 

   ```bash
   cp -r /state/partition1/user/$USER/mujoco-py /home/gridsan/$USER/
   ```

   Since each node on the system has its own local filesystem, compute nodes won’t be able to see what’s on the login node local filesystem. So what we’ll do is copy the mujoco install to the local filesystem at the start of the job. I’ve written a setup.sh script that will check to see if it’s already been copied, and copy it over if not. I also have the start of a submission script, you’ll have to put in the name of your python script and any other scheduler options you need. (edited)


4. In your `.jaynes.yml` file, add the following segment to the `startup` entry. This is ran inside the the worker machine. `setup` happens in the login node instead.

   ```bash
   starup: >-
       mkdir -p /state/partition1/user/$USER;
       echo "copying mujoco-py";
       cp -r /home/gridsan/$USER/mujoco-py /state/partition1/user/$USER/;
       echo "finished";
   ```

## To Render with `dmc` domains

Add the following to your `setup` config

```yaml
startup: | 
    export MUJOCO_GL=egl;
    export CUDA_VISIBLE_DEVICES=0;
```



## Archived Setup Instructions

These steps are no-longer needed because of the availability of default packages through the `anaconda/2021a` module. However, we keep these here in case you need a custom environment.

### Setting up GPU Accelerated Rendering with DeepMind Control suite domains

**Update**: this is no longer needed because the supercloud admins made `libglew ` available directly. You will still need to add the `egl` setting to get accelerated rendering. See the steps above.

1. You need to install `glew` with the following script

   ```bash
   mkdir ~/vendor
   cd ~/vendor
   wget https://github.com/nigels-com/glew/releases/download/glew-2.2.0/glew-2.2.0.zip     
   unzip glew-2.2.0.zip
   mv glew-2.2.0 glew
   cd glew
   make 
   ```

2.  Then add the following into your `setup` config

   ```yaml
   startup: | 
       export MUJOCO_GL=egl;
       export CUDA_VISIBLE_DEVICES=0;
       export LD_PRELOAD=$HOME/vendor/glew/lib/libGLEW.so.2.2.0:/usr/lib/libGL.so.1;
   ```

