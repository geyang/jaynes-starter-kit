from time import sleep


def train_fn(seed=None):
    from ml_logger import logger

    sleep(1)
    if seed:
        print(f"{logger.hostname} seed={seed}")
    else:
        print('done.')


if __name__ == "__main__":
    import jaynes

    jaynes.config()
    jaynes.add(train_fn, seed=100).chain(train_fn, seed=200).chain(train_fn, seed=300).chain(train_fn, seed=400)
    jaynes.execute()
    jaynes.listen()
