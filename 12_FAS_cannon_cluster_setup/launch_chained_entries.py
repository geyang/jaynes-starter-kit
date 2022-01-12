from time import sleep


def train_fn(seed=None):
    from ml_logger import logger

    sleep(1)
    if seed:
        print(f"{logger.slurm_job_id} {logger.hostname} seed={seed}")
    else:
        print('done.')


def find_torch():
    import torch
    assert torch.cuda.is_available(), "cuda should be available"
    print('cuda is available!')


if __name__ == "__main__":
    import jaynes

    jaynes.config(launch=dict(timeout=100))
    jaynes.add(train_fn, seed=100) \
        .chain(train_fn, seed=200) \
        .chain(train_fn, seed=300) \
        .chain(train_fn, seed=400) \
        .chain(train_fn, seed=500) \
        .chain(train_fn, seed=600)
    out, err, is_err = jaynes.execute()
    print("out >>>", out, err)
    print("err >>>", err)
    print("is err >>", is_err)

    jaynes.add(find_torch)
    out, err, is_err = jaynes.execute()
    print("out >>>", out, err)
    print("err >>>", err)
    print("is err >>", is_err)
    jaynes.listen()
