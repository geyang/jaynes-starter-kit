def train_fn(seed=None, log_interval=5):
    from time import sleep
    from ml_logger import logger
    import numpy as np

    logger.print('this is running')
    logger.print(f"The exp seed is: {seed}", color="green")

    steps = np.arange(100)
    losses = np.exp(-steps / 100)
    for step, loss in zip(steps, losses):
        logger.store_metrics(loss=loss)
        sleep(0.01)

        # log the averaged statistical summary
        if step % log_interval == 0:
            logger.log_metrics_summary(key_values={"step": step})

    logger.print('done!')


if __name__ == '__main__':
    import jaynes
    from ml_logger import logger, instr

    jaynes.config()

    for i in range(5):
        thunk = instr(train_fn)
        logger.log_text("""
        charts:
        - yKey: loss/mean
          xKey: step
        """, ".charts.yml", dedent=True, overwrite=True)
        jaynes.add(thunk, seed=i * 100)

    jaynes.execute()
    jaynes.listen()
