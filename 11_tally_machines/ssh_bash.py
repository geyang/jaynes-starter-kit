import jaynes


def install_ml_logger():
    from jaynes.shell import run
    run("pip install munch".split(' '))


if __name__ == '__main__':
    ip_list = ["improbable208", "improbable005", "improbable006", "improbable009",
               # "improbablex001", "improbablex002", "improbablex003", "improbablex004",
               ] + [f"visiongpu{n:02d}" for n in range(1, 60)]
    for ip in ip_list:
        jaynes.config(launch=dict(ip=ip))
        jaynes.run(install_ml_logger)

    jaynes.listen()
