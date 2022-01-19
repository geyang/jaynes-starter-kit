export JYNS_MANAGER_PORT=$RANDOM
tmux split-window "python -m jaynes.server --port $JYNS_MANAGER_PORT --host 0.0.0.0"
tmux split-window "ngrok http --region=us $JYNS_MANAGER_PORT"