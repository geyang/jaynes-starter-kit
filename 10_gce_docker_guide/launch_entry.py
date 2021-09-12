import jaynes


def launch(root, prefix, seed):
    from ml_logger import logger

    logger.configure(root_dir=root, prefix=prefix, register_experiment=True)
    logger.print(f"this has be ran {seed}")
    logger.flush()


if __name__ == "__main__":
    import os

    logger_server = os.environ.get("ML_LOGGER_ROOT")

    for seed in range(20):
        # set the verbose to True to see everything
        jaynes.config(launch=dict(name=f"test-jaynes-launch-{seed}"), verbose=True)
        prefix = f"geyang/jaynes-demo/seed-{seed}"
        print(f'logging to {prefix}')
        instances = jaynes.run(launch, root=logger_server, prefix=prefix, seed=seed)

    jaynes.listen(100)
