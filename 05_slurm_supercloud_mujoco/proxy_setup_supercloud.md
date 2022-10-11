# Supercloud Proxy Setup

Supercloud admin has kindly offered a way for us to use proxy for outbound requests such as logging and requestiong pre-trained weights. An older version of this guide can be found [[here]](proxy_setup.md).

Where “PORT” is your desired port number. This will create a proxy.env file in your home directory containing the environment variables you need to use the proxy. You can then source this file at the beginning of your job that needs the proxy. For example:

## Manually

You can set this up once per month (it gets killed during downtime).

1. first run on the login node the proxy setup script that we got from the supercloud admins. **Pick a random port number that is different from other people. Do NOT use the same port**

   ```bash
   export PORT=<your-random-port-do-not-use-the-same-port!!!>
   /usr/local/bin/start_squid_proxy.sh PORT > ~/proxy.env
   ```
   You need to do this once per month after the scheduled downtime.
   
   If you run into issues with your outbound http requests (like `ml-logger` raising `host not reachable` errors), it could be an issue with the proxy setup. In this case, you should delete the `~/proxy.env` file, and run the script above again, potentially with a different port.
   
   You could also do this every single time in your jaynes config's setup section.

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
