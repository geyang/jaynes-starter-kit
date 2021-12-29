from functools import partial

import jaynes
from jaynes.shell import run


def clean(csv_text):
    return csv_text.replace(" MiB", "").replace(" ", "")


def tally_gpu_csv(*keys):
    from ml_logger import logger

    logger.configure(root="http://44.241.150.228:8080", prefix="geyang/csail_machines/tally_gpus")

    cmd = f"/usr/bin/nvidia-smi --query-gpu={','.join(keys)} --format=csv".split(
        ' ')

    csv_output, err = run(cmd)
    csv_output = clean(csv_output.decode('utf-8'))
    first, *lines = csv_output.strip().split('\n')
    logger.print(*[f"{logger.hostname},{l}" for l in lines], sep="\n", end="\n", file="machine_list.csv")

    print(csv_output)
    logger.job_completed(logger.slurm_job_id)


def fast_tally(ip, keys: list):
    print(f"connecting to {ip}")
    jaynes.config(verbose=False, launch=dict(ip=ip))
    jaynes.run(tally_gpu_csv, *keys)


def build_gpu_table(keys, ip_list):
    from ml_logger import logger

    logger.configure(root="http://44.241.150.228:8080", prefix="geyang/csail_machines/tally_gpus")
    with logger.Sync():
        logger.remove('machine_list.csv')
    logger.print(f'hostname,{",".join(keys)}', file="machine_list.csv")

    list(map(partial(fast_tally, keys=keys), ip_list))

    jaynes.listen(200)


if __name__ == "__main__":
    build_gpu_table(keys=['memory.free', 'memory.total', 'gpu_name', 'gpu_bus_id'],
                    ip_list=["improbable208", "improbable005", "improbable006", "improbable009",
                             # "improbablex001", "improbablex002", "improbablex003", "improbablex004",
                             ] + [f"visiongpu{n:02d}" for n in range(1, 60)])
