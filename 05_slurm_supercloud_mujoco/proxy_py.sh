# manually add the local path
export PATH=$HOME/.local/bin:$PATH

export PROXY_PORT=5090
export http_proxy=http://$HOSTNAME:$PROXY_PORT
export https_proxy=http://$HOSTNAME:$PROXY_PORT
# This line runs the proxy in a screen session in the background
screen -dm proxy --hostname 0.0.0.0 --port $PROXY_PORT --timeout 3600 --client-recvbuf-size 131072 --server-recvbuf-size 131072