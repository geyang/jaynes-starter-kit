import jaynes

green = lambda s: f"\x1b[32m{s}\x1b[0m"


def train_fn():
    from time import sleep

    print('See real-time pipe-back from the server:')
    for i in range(10):
        print(f"step: {i}")
        sleep(0.1)

    print(green('Finished!'))


if __name__ == "__main__":
    jaynes.config(verbose=False)
    jaynes.run(train_fn)

    jaynes.listen(200)
