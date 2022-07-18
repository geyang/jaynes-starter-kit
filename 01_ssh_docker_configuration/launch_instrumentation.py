def train_fn(seed=None):
    from time import sleep
    from ml_logger import logger

    logger.print('this is running')
    logger.print(f"The exp seed is: {seed}", color="green")

    logger.print('This is sleeping...', color="yellow")
    sleep(5)
    logger.print('done!')


if __name__ == '__main__':
    import jaynes
    from ml_logger import logger, instr

    jaynes.config()

    for i in range(5):
        thunk = instr(train_fn)
        jaynes.add(thunk, seed=i * 100)

    jaynes.execute()
    jaynes.listen()
