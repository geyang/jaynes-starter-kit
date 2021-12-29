def read_gpu_table():
    from ml_logger import logger
    logger.configure(root="http://44.241.150.228:8080", prefix="geyang/csail_machines/tally_gpus")

    csv = logger.load_csv("machine_list.csv")
    print(csv)


if __name__ == '__main__':
    read_gpu_table()
    exit()
