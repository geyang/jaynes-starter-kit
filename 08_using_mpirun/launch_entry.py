def mpi_import():
    print('now import MPI')
    from mpi4py import MPI
    from ml_logger import logger

    logger.print(MPI, "success!", color="green")


if __name__ == "__main__":
    import jaynes

    jaynes.config(runner=dict(entry_script="mpirun python -u -m jaynes.entry"))
    jaynes.run(mpi_import)
    jaynes.listen()
