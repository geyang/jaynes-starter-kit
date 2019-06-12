# parameters
USERNAME=<your-username>
JUMP_HOST=fairjmp.thefacebook.com
LOCAL_PORT=41000
INTRA_HOST=<your-dev-machine-ip>
SSH_PORT=22
RSA_KEY=<your-rsa-key-no-pub-postfix>

# targets
ssh:
	ssh -i ${RSA_KEY} ${USERNAME}@${JUMP_HOST}
tunnel:
	echo "\033[32mBuilding Tunnel in the foreground...\033[0m\n"
	ssh -N -J ${USERNAME}@${JUMP_HOST} -i ${RSA_KEY} -L ${LOCAL_PORT}:${INTRA_HOST}:${SSH_PORT} ${INTRA_HOST}
tunnel-background:
	echo "\033[32mBuilding Tunnel in the background...\033[0m\n"
	ssh -N -f -J ${USERNAME}@${JUMP_HOST} -i ${RSA_KEY} -L ${LOCAL_PORT}:${INTRA_HOST}:${SSH_PORT} ${INTRA_HOST}
	echo "\033[32mTunnel Built Successfully!!\033[0m\n"
kill-all-tunnel:
	ps aux | grep -ie 'ssh -N -f' | awk '{print $$2}' | xargs kill -9
ssh-local:
	ssh -i ${RSA_KEY} localhost -p ${LOCAL_PORT}
