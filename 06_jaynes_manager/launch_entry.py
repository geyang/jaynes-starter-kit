import jaynes


def launch(sleep_time=1):
    from time import sleep
    print("this is running")
    sleep(sleep_time)
    print("this is done")


if __name__ == "__main__":
    jaynes.config(launch=dict(timeout=4))
    for i in range(4):
        print(f'launching {i}')
        o, *_ = jaynes.run(launch, sleep_time=0.5)
        print(o)
    jaynes.listen()
