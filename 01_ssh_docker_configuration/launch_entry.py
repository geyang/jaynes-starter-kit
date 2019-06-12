def launch(learning_rate, model_name):
    print(f"training model {model_name} with {learning_rate}")


if __name__ == "__main__":
    import jaynes

    jaynes.config("local")
    jaynes.run(launch)

    # # this line allows you to keep the pipe open and hear back from the remote instance.
    # jaynes.listen()
