import jaynes


def launch(sleep_time=1, job_count=0):
    from time import sleep
    print(f"launch-{job_count} is running")
    sleep(sleep_time)
    print(f"launch-{job_count} is done")


if __name__ == "__main__":
    jaynes.config(launch=dict(timeout=4))
    for i in range(4):
        print(f'adding {i}')
        jaynes.add(launch, sleep_time=0.5, job_count=i)
    o, *_ = jaynes.execute()
    print(o)
    jaynes.listen()
