def train_fn(seed=None):
    print("Training model...")
    print("seed:", seed)
    print("Done!")


if __name__ == '__main__':
    import jaynes

    jaynes.config(verbose=False)
    job_ids = jaynes.run(train_fn, seed=100)
    jaynes.listen(command=f"kubectl logs -f {job_ids[0]} --all-containers", interval=3)
