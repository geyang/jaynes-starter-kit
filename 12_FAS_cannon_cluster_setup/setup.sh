# Load the python module
module load python/3.8.5-fasrc01
pip install jaynes -q

# make the mount for the jaynes server
mkdir -p /n/holyscratch01/iaifi_lab/$USER/jaynes-mounts
cd /n/holyscratch01/iaifi_lab/$USER
screen -dm python -m jaynes.server --host 0.0.0.0

# You should see your jaynes.server up and running
screen -ls

# download and install ngrok
sudo tar -xvzf ~/Downloads/ngrok-stable-linux-amd64.tgz -C /usr/local/bin
tar -xvzf ~/Downloads/ngrok-stable-linux-amd64.tgz -C .local/bin
mkdir .local
mkdir -p .local/bin
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.tgz --no-check-certificate
tar -xzf ngrok-stable-linux-amd64.tgz -C .local/bin

# test if ngrok is available
which ngrok

# Now authenticate ngrok:
ngrok authtoken $YOUR_NGROK_TOKEN
screen -dm ngrok http --region=us --hostname=$YOUR_NGROK_DOMAIN 3000
screen -ls
