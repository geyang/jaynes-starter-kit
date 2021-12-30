from functools import partial

import jaynes
from jaynes.shell import run

# CSV_KEYS = "id", "image", "name", "status", "createdTime"
QUERY_KEYS = 'memory.free', 'memory.total', 'gpu_name', 'gpu_bus_id'

PREFIX = "geyang/csail_machines/csail_machines"
CSV_FILE = "machine_list.csv"


def clean(csv_text):
    return csv_text.replace(" MiB", "").replace(" ", "")


def tally_gpu_csv(keys):
    from ml_logger import logger

    logger.configure(root="http://44.241.150.228:8080", prefix=PREFIX)

    cmd = f"/usr/bin/nvidia-smi --query-gpu={','.join(keys)} --format=csv".split(
        ' ')

    csv_output, err = run(cmd)
    csv_output = clean(csv_output.decode('utf-8'))
    first, *lines = csv_output.strip().split('\n')
    logger.print(*[f"{i},{logger.hostname},{l}" for i, l in enumerate(lines)], sep="\n", end="\n", file=CSV_FILE)

    print(csv_output)
    logger.job_completed(logger.slurm_job_id)


def fast_tally(ip, keys: list):
    print(f"connecting to {ip}")
    jaynes.config(verbose=False, launch=dict(ip=ip))
    jaynes.run(tally_gpu_csv, keys=keys)


def main(keys, ip_list):
    from ml_logger import logger

    logger.configure(root="http://44.241.150.228:8080", prefix=PREFIX)
    with logger.Sync():
        logger.remove(CSV_FILE)
    logger.print(f'device_id,hostname,{",".join(keys)}', file=CSV_FILE)

    list(map(partial(fast_tally, keys=keys), ip_list))

    jaynes.listen(200)


if __name__ == "__main__":
    main(keys=QUERY_KEYS,
         ip_list=["improbable208", "improbable005", "improbable006", "improbable009",
                             "improbablex001", "improbablex002", "improbablex003", "improbablex004",
                             ] + [f"visiongpu{n:02d}" for n in range(1, 60)])
