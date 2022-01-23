import jaynes


def launch(pause=1):
    from time import sleep
    print("this is running")
    sleep(pause)
    print("this is done")


if __name__ == "__main__":
    jaynes.config(launch=dict(timeout=5), runner=dict(partition="gpu_test"))
    for i in range(10):
        stdout, stderr, is_err = jaynes.run(launch, pause=100)
        print(stdout, stderr, is_err)
    jaynes.listen()
