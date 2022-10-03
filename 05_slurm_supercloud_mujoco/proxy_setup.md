# Setting up `http` proxy for outbound logging requests

Sometimes outbound http requests are blocked, making it difficult to send out logging requests to our instrumentation server. In this case, we can setup a proxy server on the login nodes to relay the requests out.

1. first `pip install proxy.py`

   ```bash
   pip install --user proxy.py
   ```
   
2. Create a script called  `~/proxy.sh` contianing the following
   
   
   ```bash
   # manually add the local path
   export PATH=$HOME/.local/bin:$PATH
   
   export PROXY_PORT=5090
   export http_proxy=http://$HOSTNAME:$PROXY_PORT
   export https_proxy=http://$HOSTNAME:$PROXY_PORT
   # This line runs the proxy in a screen session in the background
   screen -dm proxy --hostname 0.0.0.0 --port $PROXY_PORT --timeout 3600 --client-recvbuf-size 131072 --server-recvbuf-size 131072
   ```
   
   **Note**: make sure you use a different port from `5000`, since others might be using it.
   
   **How to Debug**: to make sure that the proxy runs and the port is unoccupied, try the following with different ports
   
   ```bash
   proxy --hostname 0.0.0.0 --port $PROXY_PORT --timeout 3600 --client-recvbuf-size 131072 --server-recvbuf-size 131072
   ```
   
   **Important**: save these in a separate ~/proxy.sh file and reference that file in your `.jaynes.yml` config. If you put these into your ~/.bashrc file, `pip install`ing from the worker node would fail. 
   
   **Important**: pip install uses the `$https_proxy` variable, where the ml-logger instrumentation server is using `http` at the moment.
   
3. **How to check if your proxy is running**

   You can check by typing `screen -ls` and it should show a list of running `screen` sessions. **To attached to a running screen session**, you can type
   
   ```bash
   screen -r <your-session-id>
   ```
   
   🚨 `Ctrl-C` kills the screen session. To **detach** from the screen session without terminating it, use <kbd>ctrl-a</kbd> + <kbd>d</kbd>.
   
These environment parameters should setup the `requests` module to automatically use your login node as the proxy server. `ml_logger` uses the `requests-future` module, which inherets from `requests` module for async http calls.

In case you want to run `pip` install from within the worker node and the `https_proxy` variable is not set, you need to use the following syntax:

```bash
pip install --user --proxy <your http_proxy value> <your-package>
```

**A common mistake** is setting the `http_proxy` variable which pip does not use because pyPI servers are all https already.
