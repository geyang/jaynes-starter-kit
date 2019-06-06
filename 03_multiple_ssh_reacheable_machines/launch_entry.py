import jaynes


def launch():
    s = """
    # The Awesome ML-Logger
    
    You can run the following code with ml-logger:
    
    ```python
    from ml_logger import logger
    
    logger.log(lr=0, clip range=0.200, step=0, timestamp='2018-11-16T00:09:27.198142', reward=-109.43)
    logger.flush()
    ```
    ╒════════════════════╤════════════════════════════╕
    │         lr         │           0.000            │
    ├────────────────────┼────────────────────────────┤
    │     clip range     │           0.200            │
    ├────────────────────┼────────────────────────────┤
    │        step        │             0              │
    ├────────────────────┼────────────────────────────┤
    │      timestamp     │'2018-11-16T00:09:27.198142'│
    ├────────────────────┼────────────────────────────┤
    │       reward       │          -109.43           │
    ╘════════════════════╧════════════════════════════╛
    """
    print(s)


if __name__ == "__main__":

    jaynes.config(mode='hodor')
    jaynes.run(launch)

    # try below
    jaynes.config(mode='oberyn')
    jaynes.run(launch)

    # try run locally!
    jaynes.config(mode='local')
    jaynes.run(launch)

    # this line allows you to keep the pipe open and hear back from the remote instance.
    jaynes.listen()
