def gym_render():
    import gym
    from ml_logger import logger

    env = gym.make("Reacher-v2")
    logger.print("gym Reacher-v2 is working!", color="green")
    img = env.render('rgb_array')
    logger.print(f"Reacher-v2 renders <{img.shape}>", color="green")


def mujoco_gpu_render():
    import mujoco_py
    assert 'gpu' in str(mujoco_py.cymj).split('/')[-1], "mujoco is not using GPU rendering"


def gym_dmc_render():
    import gym
    from ml_logger import logger

    env = gym.make("dmc:Cartpole-balance-v1")
    logger.print(f"dmc Cartpole starts!", color="green")
    img = env.render('rgb_array')
    logger.print(f"dmc:Cartpole renders <{img.shape}>", color="green")


def both():
    from ml_logger import logger

    logger.print("this is running", color="yellow")

    gym_render()
    gym_dmc_render()

    logger.print("success", color="green")


if __name__ == "__main__":
    import jaynes

    jaynes.config()
    jaynes.add(gym_render)
    jaynes.chain(mujoco_gpu_render)
    jaynes.chain(gym_dmc_render)
    jaynes.chain(both)
    jaynes.execute()
    jaynes.listen()
