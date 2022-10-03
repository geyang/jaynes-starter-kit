# Supercloud Proxy Setup

Supercloud admin has kindly offered a way for us to use proxy for outbound requests such as logging and requestiong pre-trained weights. An older version of this guide can be found [[here]](proxy_setup.md).

Where “PORT” is your desired port number. This will create a proxy.env file in your home directory containing the environment variables you need to use the proxy. You can then source this file at the beginning of your job that needs the proxy. For example:

## Manually

You can set this up once per month (it gets killed during downtime).

1. first run on the login node, their proxy setup script:

   ```bash
   /usr/local/bin/start_squid_proxy.sh PORT > ~/proxy.env
   ```

2. Now, source the generated `.env` file in the `.jaynes.yml` config

   ```yaml
   runner: !runners.Slurm
      setup: |
         source /etc/profile.d/modules.sh
         source $HOME/.bashrc
         module load cuda/10.2
         module load anaconda/2021b
         module load mpi/openmpi-4.0
         source $HOME/proxy.env
   ```
   
**Important Note** If you notice some of the requests not going through, it could be due to issues with the proxy. 
Message in the channel to let others know.

**Silent Errors** Sometimes, if your request is too large, like when you are trying to transfer large weights, it 
could fail silently if the proxy server is not setup with a sufficiently large request buffer. If you notice missing
results, also let us know and we can ask the admins to fix this.
