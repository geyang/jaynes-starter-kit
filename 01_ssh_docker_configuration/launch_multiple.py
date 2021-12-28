def launch(lr, model_name="LeNet"):
    print(f"training model {model_name} with {lr}")
    print('...')
    print('This is working!!')


if __name__ == "__main__":
    import jaynes

    jaynes.config(runner={"name": f"first-run"})
    jaynes.add(launch, lr=1e-4)
    jaynes.config(runner={"name": f"second-run"})
    jaynes.add(launch, lr=3e-4)
    jaynes.execute()

    # this line allows you to keep the pipe open and hear back from the remote instance.
    jaynes.listen(200)
