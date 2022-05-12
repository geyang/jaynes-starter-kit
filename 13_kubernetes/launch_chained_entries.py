from time import sleep


def train_fn(seed=None):
    from ml_logger import logger

    sleep(1)
    if seed:
        print(f"{logger.slurm_job_id} seed={seed}")
    else:
        print('done.')


if __name__ == "__main__":
    import jaynes

    jaynes.config()
    jaynes.add(train_fn, seed=100) \
        .chain(train_fn, seed=200) \
        .chain(train_fn, seed=300) \
        .chain(train_fn, seed=400) \
        .chain(train_fn, seed=500)
    jaynes.add(train_fn, seed=600) \
        .chain(train_fn, seed=700) \
        .chain(train_fn, seed=800) \
        .chain(train_fn, seed=900) \
        .chain(train_fn, seed=1000)
    jaynes.execute()
    jaynes.listen()
