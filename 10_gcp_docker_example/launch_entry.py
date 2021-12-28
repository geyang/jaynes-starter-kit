from time import sleep

import jaynes


def launch(root, prefix, seed):
    from ml_logger import logger

    logger.configure(root_dir=root, prefix=prefix, register_experiment=True)
    logger.print(f"this has be ran {seed}")
    logger.flush()

    sleep(600)


if __name__ == "__main__":
    import os
    from ml_logger import USER, ROOT

    for seed in range(10):
        prefix = f"{USER}/jaynes-demo/gcp/launch_entry/seed-{seed}"
        jaynes.config(launch=dict(name=prefix), verbose=True)
        instances = jaynes.run(launch, root=ROOT, prefix=prefix, seed=seed)

    jaynes.listen(100)
