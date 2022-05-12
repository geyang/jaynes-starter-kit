def train_fn(seed=None):
    print("Training model...")
    print("seed:", seed)
    print("Done!")


if __name__ == '__main__':
    import jaynes

    jaynes.config(verbose=True)
    jaynes.run(train_fn, seed=100)
    jaynes.listen()
