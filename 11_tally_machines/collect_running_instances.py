from functools import partial

import jaynes
from jaynes.shell import run


def clean(csv_text):
    return csv_text.replace(" MiB", "").replace(" ", "")


CSV_KEYS = "id", "image", "name", "status", "createdTime"
DOCKER_PS_KEYS = "ID", "Image", "Names", "Status", "CreatedAt"

PREFIX = "geyang/csail_machines/running_instances"
CSV_FILE = "instance_list.csv"


def tally_docker_instances(keys):
    from ml_logger import logger

    logger.configure(root="http://44.241.150.228:8080", prefix=PREFIX)

    # cmd = r"docker ps".split(' ')
    key_str = ','.join([r"{{." + key + r"}}" for key in keys])
    cmd = f"docker ps --format '{key_str}'".split(' ')

    try:
        csv_output, err = run(cmd)
        if err:
            logger.job_errored(job=dict(error=err, hostname=logger.hostname))
    except Exception as e:
        logger.job_errored(job=dict(error=e, hostname=logger.hostname))

    # print("==>", csv_output.decode('utf-8'), err)
    lines = csv_output.decode('utf-8').strip().rstrip()
    if lines:
        logger.print(*[f"{logger.hostname},{l[1:-2]}" for i, l in enumerate(lines.split('\n'))], sep="\n", end="\n",
                     file=CSV_FILE)
    logger.job_completed(logger.slurm_job_id)


def fast_tally(ip, keys: list):
    print(f"connecting to {ip}")
    jaynes.config(verbose=False, launch=dict(ip=ip))
    jaynes.run(tally_docker_instances, keys=keys)


def main(ip_list, keys, docker_keys):
    from ml_logger import logger

    logger.configure(root="http://44.241.150.228:8080", prefix=PREFIX)
    with logger.Sync():
        logger.remove(CSV_FILE)
    logger.print(f'hostname,{",".join(keys)}', file=CSV_FILE)

    list(map(partial(fast_tally, keys=docker_keys), ip_list))

    jaynes.listen(200)


if __name__ == "__main__":
    main(keys=CSV_KEYS, docker_keys=DOCKER_PS_KEYS,
         ip_list=["improbable208", "improbable005", "improbable006", "improbable009",
                  "improbablex001", "improbablex002", "improbablex003", "improbablex004",
                  ] + [f"visiongpu{n:02d}" for n in range(1, 60)], )
