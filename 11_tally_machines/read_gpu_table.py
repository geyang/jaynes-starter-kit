def kill_docker_instance(instance_id):
    from jaynes.shell import run

    out, err = run(f"docker kill {instance_id}")
    print(out)


class CSAIL_MACHINES:
    def __init__(self, ):
        self.get_machine_list()
        self.get_instance_list()

    def get_machine_list(self):
        from ml_logger import logger
        logger.configure(prefix="geyang/csail_machines/csail_machines")

        csv = logger.load_csv("machine_list.csv")
        self.machine_list = csv.sort_values(by="memory.free", ascending=False)
        self.machine_list.reset_index(drop=True, inplace=True)

    def get_instance_list(self):
        from ml_logger import logger
        logger.configure(prefix="geyang/csail_machines/running_instances")

        self.instance_list = logger.load_csv("instance_list.csv")
        self.instance_list.set_index('id', inplace=True)
        print(self.instance_list)

    def pop(self, order="memory.free"):
        row = self.machine_list.iloc[0]
        self.machine_list = self.machine_list.drop(0)
        self.machine_list.reset_index(drop=True, inplace=True)
        return row['hostname'].split('.')[0], row['device_id']

    def kill_instance(self, instance_id):
        import jaynes

        instance = self.instance_list.iloc[instance_id]
        jaynes.config("ssh", launch=dict(ip=instance['hostname'], block=True))
        jaynes.run(kill_docker_instance, instance_id=instance['id'])


if __name__ == '__main__':
    m = CSAIL_MACHINES()
    ip, gpu_id = m.pop()
    print(ip, gpu_id)
    ip, gpu_id = m.pop()
    print(ip, gpu_id)
    ip, gpu_id = m.pop()
    print(ip, gpu_id)
