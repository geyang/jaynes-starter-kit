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

    jaynes.config()
    jaynes.add(launch, root=logger_server, seed=100)
    jaynes.chain(launch, root=logger_server, seed=200)
    jaynes.add(launch, root=logger_server, seed=300)
    jaynes.chain(launch, root=logger_server, seed=400)
    jaynes.execute()
    jaynes.listen(100)
