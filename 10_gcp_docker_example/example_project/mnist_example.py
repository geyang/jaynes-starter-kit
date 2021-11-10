def main(seed=None, **kwargs):
    from ml_logger import logger

    logger.print(f'mnist example is running w/ seed {seed}')
    logger.job_running()
