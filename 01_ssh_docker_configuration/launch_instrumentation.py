def launch(lr, model_name="LeNet"):
    print(f"training model {model_name} with {lr}")
    print('...')
    print('This is working!!')

    print('now try to import ml-logger')
    from ml_logger import logger, RUN
    print('import succeeded')

    print(logger)


    print('now inspec the RUN object: RUN', vars(RUN))
    assert RUN.prefix == "set_from_outside"
    assert RUN.job_name == "ml-logger-test-job"


if __name__ == "__main__":
    import jaynes
    from ml_logger import RUN, instr

    RUN.prefix = "set_from_outside"
    # need to set the job name too
    RUN.job_name = "ml-logger-test-job"
    jaynes.config()
    thunk = instr(launch)
    jaynes.run(thunk, lr=1e-3)

    # this line allows you to keep the pipe open and hear back from the remote instance.
    jaynes.listen(200)
