from time import sleep

import jaynes


def launch(root, prefix, seed):
    from ml_logger import logger

    logger.configure(root_dir=root, prefix=prefix, register_experiment=True)
    logger.print(f"this has be ran {seed}")
    logger.flush()

    sleep(600)


if __name__ == "__main__":
    from example_project.mnist_example import main
    from ml_logger import RUN

    jaynes.config("local" if RUN.debug else None, verbose=True)
    RUN.job_name += "/{job_counter}"

    jaynes.config()
    jaynes.add(main, seed=100) \
        .chain(main, seed=200) \
        .add(main, seed=300) \
        .chain(main, seed=400)

    jaynes.execute()
