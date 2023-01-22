default:
        echo $$((4000 + $$$$ % 2000)) > _
        echo $$(hostname) > LOGIN_HOSTNAME
        export PATH=$$HOME/.local/bin:$$PATH && tensorboard --port $$(cat _)
worker:
        echo $$((4000 + $$$$ % 1000)) > WORKER_PORT
        echo "export http_proxy=http://localhost:$$(cat WORKER_PORT); export https_proxy=http://localhost:$$(cat WORKER_PORT)" > $$HOME/.worker_export
        echo "http_proxy=http://localhost:$$(cat WORKER_PORT) https_proxy=http://localhost:$$(cat WORKER_PORT)" > $$HOME/.worker
        @echo $$(cat WORKER_PORT):localhost:$$(cat _) $$(cat LOGIN_HOSTNAME)
        ssh -L $$(cat WORKER_PORT):localhost:$$(cat _) $$(cat LOGIN_HOSTNAME) -fN
kill:
        kill -s 9 `ps -ef | grep tensorboard |grep -v grep | awk '{print $$2}'` &
        kill -s 9 `ps -ef | grep tee |grep -v grep | awk '{print $$2}'`  &
        kill -s 9 `ps -ef | grep escher |grep -v grep | awk '{print $$2}'` &
kill_all: kill
        kill -s 9 `ps -ef | grep srun |grep -v grep | awk '{print $$2}'` &
        kill -s 9 `ps -ef | grep jaynes |grep -v grep | awk '{print $$2}'` &
        kill -s 9 `ps -ef | grep 'bash -s' |grep -v grep | awk '{print $$2}'` &
cleanup: kill