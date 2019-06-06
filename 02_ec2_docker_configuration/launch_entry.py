import jaynes


def launch(some_key_word=None):
    s = f"""
    # The Awesome ML-Logger
    
    You can run the following code with ml-logger:
    
    ```python
    from ml_logger import logger
    
    logger.log(lr=0, clip range=0.200, step=0, timestamp='2018-11-16T00:09:27.198142', reward={some_key_word})
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
    │       reward       │ {    some_key_word:^26   } │
    ╘════════════════════╧════════════════════════════╛
    """
    print(s)


if __name__ == "__main__":
    jaynes.config(verbose=True, launch=dict(name="test-jaynes-launch"))
    jaynes.run(launch)
    jaynes.listen(10)
