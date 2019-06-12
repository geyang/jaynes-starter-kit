from textwrap import dedent, indent

import jaynes
import jaynes.runners
import jaynes.mounts
import jaynes.shell

from jaynes.constants import JAYNES_PARAMS_KEY
from jaynes.param_codec import serialize
from jaynes.shell import popen

import datetime
import os
import uuid
import tempfile
import subprocess
import time


def ck(cmd, *args, verbose=False, **kwargs):
    if verbose:
        if args:
            print(cmd, *args)
        else:
            print(cmd)
    try:
        subprocess.check_call(cmd, *args, **kwargs, executable="/bin/bash")
    except subprocess.CalledProcessError as e:
        print(e.output)


from jaynes.shell import ck


class SlurmBatch(jaynes.runners.RunnerType):
    setup_script = ""
    run_script = ""
    post_script = ""

    def __init__(
            self,
            pypath="",
            setup="",
            startup="",
            launch_directory=None,
            envs=None,
            n_gpu=None,
            nodes=1,
            cpus_per_task=1,
            tasks_per_node=None,
            mem_per_cpu="100MB",
            partition="dev",
            time_limit="5",
            # label=False,
            constraints=None,
            name="jaynes",
            sbatch_directory=None,
            **_,
    ):
        launch_directory = launch_directory or os.getcwd()
        entry_script = f"{JAYNES_PARAMS_KEY}=${{1}} srun python -u -m jaynes.entry"
        # --get-user-env
        setup_cmd = (setup.strip() + "\n") if setup else ""
        setup_cmd += f"export PYTHONPATH={pypath}"

        sbatch_script = dedent(f"""
                #!/bin/bash
                #SBATCH --output=/checkpoint/%u/jobs/job.%j.out
                #SBATCH --error=/checkpoint/%u/jobs/job.%j.err
                #SBATCH --job-name {name}
                #SBATCH --nodes {nodes}
                #SBATCH --time={time_limit}
                #SBATCH --signal=USR1@600
                #SBATCH --cpus-per-task {cpus_per_task}
                #SBATCH --mem-per-cpu {mem_per_cpu}
                #SBATCH --partition {partition}
                #SBATCH --open-mode=append
                """).strip()
        if n_gpu:
            sbatch_script += f"#SBATCH --gres gpu:{n_gpu}\n"

        if tasks_per_node:
            sbatch_script += f"#SBATCH --ntasks-per-node {tasks_per_node}\n"
        elif n_gpu:
            sbatch_script += f"#SBATCH --ntasks-per-node {n_gpu}\n"
        else:
            sbatch_script += f"#SBATCH --ntasks-per-node 1\n"

        if constraints:
            sbatch_script += f"#SBATCH --constraint={constraints.strip}\n"

        startup = dedent(startup).strip() if startup else ""

        sbatch_script += dedent(f"""
            {startup}
            {"cd '{}';".format(launch_directory) if launch_directory else ""}""").strip()

        sbatch_script += envs if envs else ""
        sbatch_script += setup_cmd
        sbatch_script = sbatch_script.replace("$", "\$")
        sbatch_script += f"{{{entry_script.strip()}}}" \
            f"> >(tee -a ${{JAYNES_LOG_DIR}}/{name}.log) 2> >(tee -a ${{JAYNES_LOG_DIR}}/{name}.err.log >&2)"

        sbatch_file = f"/tmp/jaynes-batch-script-{name}.sh"

        self.run_script_thunk = f"sbatch {sbatch_file} {{encoded_thunk}}" \
            f"tail -f ${{{{JAYNES_LOG_DIR}}}}/{name}.log ${{{{JAYNES_LOG_DIR}}}}/{name}.err.log"


        sbatch_directory = os.path.abspath(sbatch_directory) if sbatch_directory else ""

        self.setup_script = f"""
            cd {sbatch_directory}
            cat >{sbatch_file} <<EOL 
            {indent(sbatch_script, " " * 8)}
        EOL
            """

        # todo: consider saving this in a mounted directory instead.
        self.post_script = f"""
            rm {sbatch_file}
            """

    def run(self, fn, *args, **kwargs):
        encoded_thunk = serialize(fn, args, kwargs)
        self.run_script = self.run_script_thunk.format(encoded_thunk=encoded_thunk)
        return self


jaynes.runners.SlurmBatch = SlurmBatch


class LocalCode:
    def __init__(
            self,
            *,
            source_path,
            dest_path=None,
            name=None,
            pypath=False,
            excludes=None,
            file_mask=None,
    ):
        """
        Copies code from a local path to a dest path

        :param source_path: path to the local directory. Doesn't have to be absolute.
        :param dest_path: The path on the remote instance. Default /tmp/{uuid4()}
        :param name: the name for the tar ball. Default to {uuid4()}
        :param pypath (bool): Whether this directory should be added to the python path
        :param excludes: The files paths to exclude, default to "--exclude='*__pycache__'"
        :param file_mask: The file mask for files to include. Default to "."
        :return: self
        """
        # I fucking hate the behavior of python defaults. -- GY
        file_mask = file_mask or "."  # file_mask can Not be None or "".
        excludes = (
                excludes
                or "--exclude='*__pycache__' --exclude='*.git' --exclude='*.idea' --exclude='*.egg-info'"
        )

        from uuid import uuid4
        name = name or uuid4()

        from jaynes import RUN
        source_abs = os.path.join(RUN.project_root, source_path)

        if dest_path:
            assert os.path.isabs(dest_path), "dest_path path has to be absolute"
        else:
            dest_path = f"/tmp/{name}"

        self.local_script = dedent(f"""
            mkdir -p '{dest_path}'

            _dir=$(pwd) # save pwd
            cd {source_abs}
            rsync -az {excludes} {file_mask} {dest_path}
            cd ${{_dir}} # reset to original wd
            """)
        self.host_path = dest_path
        self.host_setup = ""
        self.pypath = pypath
        self.container_path = ""
        self.docker_mount = ""


jaynes.mounts.LocalCode = LocalCode


def launch_local(self, dry=False, verbose=False, detached=False):
    with open("tmp.sh", "w") as f:
        f.write(self.launch_script)

    if dry:
        print(self.launch_script)
    else:
        if detached:
            import sys

            popen(
                self.launch_script,
                verbose=verbose,
                shell=True,
                stdout=sys.stdout,
                stderr=sys.stderr,
                executable="/bin/bash",
            )
        else:
            ck(self.launch_script, verbose=verbose, shell=True, executable="/bin/bash")


jaynes.Jaynes.launch_local = launch_local
jaynes.Jaynes.local = launch_local
