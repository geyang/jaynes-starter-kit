def launch(lr, model_name="LeNet"):
    from time import sleep

    print(f"training model {model_name} with {lr}")
    print('...')
    print('This is working!!')
    sleep(10)


if __name__ == "__main__":
    import jaynes

    jaynes.config()
    jaynes.run(launch, lr=1e-3)

    # this line allows you to keep the pipe open and hear back from the remote instance.
    jaynes.listen(200)
