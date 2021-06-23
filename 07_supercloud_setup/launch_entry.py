def gym_render():
    import gym
    from ml_logger import logger

    env = gym.make("Reacher-v2")
    img = env.render('rgb_array')
    logger.print(f"image renders at <{img.shape}> succeeds", color="green")


def launch():
    from ml_logger import logger

    logger.print("this is running", color="yellow")

    gym_render()

    logger.print("success", color="green")

if __name__ == "__main__":
    import jaynes

    jaynes.config(launch=dict(timeout=0))
    for i in range(1):
        jaynes.run(launch)
    jaynes.listen()
