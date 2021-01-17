import jaynes

green = lambda s: f"\x1b[32m{s}\x1b[0m"


def train_fn(seed=100):
    from time import sleep

    print(f'[seed: {seed}] See real-time pipe-back from the server:')
    for i in range(3):
        print(f"[seed: {seed}] step: {i}")
        sleep(0.1)

    print(green(f'[seed: {seed}] Finished!'))


if __name__ == "__main__":
    jaynes.config(verbose=False)
    for i in range(4):
        jaynes.run(train_fn, seed=i * 100)

    jaynes.listen(200)
