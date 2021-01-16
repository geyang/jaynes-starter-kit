import jaynes

from launch_entry import train_fn

if __name__ == "__main__":
    for i in range(3):
        jaynes.config(verbose=False, runner=dict(host=f"vision0{i}"))
        jaynes.run(train_fn)

    jaynes.listen(200)
