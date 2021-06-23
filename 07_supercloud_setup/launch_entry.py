def gym_render():
    import gym
    from ml_logger import logger

    env = gym.make("Reacher-v2")
    logger.print("gym Reacher-v2 is working!", color="green")
    img = env.render('rgb_array')
    logger.print(f"Reacher-v2 renders <{img.shape}>", color="green")


def gym_dmc_render():
    import gym
    from ml_logger import logger

    env = gym.make("dmc:Cartpole-balance-v1")
    logger.print(f"dmc Cartpole starts!", color="green")
    img = env.render('rgb_array')
    logger.print(f"dmc:Cartpole renders <{img.shape}>", color="green")


def launch(domain):
    from ml_logger import logger

    logger.print("this is running", color="yellow")

    if domain == 'dmc':
        gym_dmc_render()
    elif domain == 'mujoco':
        gym_render()

    logger.print("success", color="green")


if __name__ == "__main__":
    import jaynes
    import argparse
    from functools import partial

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--domain', type=str, choices=['mujoco', 'dmc'], default='mujoco')
    args = argparser.parse_args()

    jaynes.config(launch=dict(timeout=0))
    for i in range(1):
        jaynes.run(partial(launch, domain=args.domain))
    jaynes.listen()
