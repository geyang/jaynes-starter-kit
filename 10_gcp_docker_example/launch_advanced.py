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
    from ml_logger import instr, RUN

    jaynes.config("local" if RUN.debug else None, verbose=True)
    RUN.job_name += "/{job_counter}"

    for seed in range(1):
        # instr wrapper automatically sets the jaynes.launch.name field of the config.
        thunk = instr(main, seed=seed)
        instances = jaynes.run(thunk)

    jaynes.listen(100)
