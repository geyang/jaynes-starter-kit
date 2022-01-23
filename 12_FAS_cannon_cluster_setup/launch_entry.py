from termcolor import cprint

import jaynes


def launch(pause=1):
    from time import sleep
    print("this is running")
    sleep(pause)
    print("this is done")


if __name__ == "__main__":
    jaynes.config(launch=dict(timeout=1), runner=dict(partition="gpu"))
    for i in range(10):
        stdout, stderr, is_err = jaynes.run(launch, pause=100)
        if stdout:
            print(stdout)
        if is_err:
            print(f"Launch Error:")
            cprint(stderr, "red")
    jaynes.listen()
