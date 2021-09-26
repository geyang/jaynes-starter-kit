import jaynes


def launch(root, seed=None):
    from ml_logger import logger

    logger.configure(root_dir=root,
                     prefix=f"geyang/jaynes-demo/seed-{seed}",
                     register_experiment=True)
    logger.print("this has be ran")


if __name__ == "__main__":
    import os
    logger_server = os.environ.get("ML_LOGGER_ROOT")

    for seed in range(4):
        # set the verbose to True to see everything
        jaynes.config(launch=dict(name=f"test-jaynes-launch-{seed}"))
        jaynes.run(launch, root=logger_server, seed=seed)
    jaynes.listen(100)
