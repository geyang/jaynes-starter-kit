import jaynes


def launch():
    from time import sleep
    print("this is running")
    sleep(10)
    print("this is done")


if __name__ == "__main__":
    jaynes.config(launch=dict(timeout=0))
    for i in range(64):
        jaynes.run(launch)
    jaynes.listen()
