from time import sleep



def train_fn(seed=None):
    from ml_logger import logger
    import torch.cuda

    sleep(1)
    if seed:
        print(f"{logger.hostname} seed={seed}")
    else:
        print('done.')

    print(f'torch cuda {torch.cuda.is_available()}')


if __name__ == "__main__":
    import jaynes

    jaynes.config()
    jaynes.add(train_fn, seed=100).chain(train_fn, seed=200).chain(train_fn, seed=300)
    jaynes.add(train_fn, seed=400).chain(train_fn, seed=500).chain(train_fn, seed=600)
    job_ids = jaynes.execute()
    jaynes.listen(command=f"/bin/bash -c 'kubectl logs {job_ids[0]} --follow --all-containers'", backoff_limit=3)
