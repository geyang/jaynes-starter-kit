# Supercloud Manager Setup

We need to make sure the python environments are identical between users. To make everything generic, run the following:

```bash
bash setup.sh
```

The contnt of the setup.sh is the following:

```bash
module load cuda/10.2
module load anaconda/2021b

echo 'export DATA_DIR=$HOME/escher_shared' >> $HOME/.bashrc

echo '
export ML_LOGGER_ROOT=http://44.241.150.228:8080
export ML_LOGGER_USER=geyang
export ML_LOGGER_TOKEN=' >> $HOME/.bashrc

echo "
# manually add the local path
export PATH=$HOME/.local/bin:$PATH

export PROXY_PORT=$RANDOM
export http_proxy=http://\$HOSTNAME:\$PROXY_PORT
export https_proxy=http://\$HOSTNAME:\$PROXY_PORT
# This line runs the proxy in a screen session in the background
screen -dm proxy --hostname 0.0.0.0 --port $PROXY_PORT --timeout 3600 --client-recvbuf-size 131072 --server-recvbuf-size 131072
" >> haha.sh

conda install --yes pyCurl
pip install -r requirements.txt
```

This should setup your python environment.
