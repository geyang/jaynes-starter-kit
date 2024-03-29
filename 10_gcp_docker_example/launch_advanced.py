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
    from ml_logger import logger, instr, RUN

    jaynes.config("local" if RUN.debug else None, verbose=True)
    RUN.job_name += "/{job_counter}"


    # instr wrapper automatically sets the jaynes.launch.name field of the config.
    jaynes.config()
    thunk = instr(main, seed=100)
    jaynes.add(thunk)
    thunk = instr(main, seed=200)
    jaynes.chain(thunk)
    thunk = instr(main, seed=300)
    jaynes.add(thunk)
    thunk = instr(main, seed=400)
    jaynes.chain(thunk)

    jaynes.execute()

    jaynes.listen(100)
