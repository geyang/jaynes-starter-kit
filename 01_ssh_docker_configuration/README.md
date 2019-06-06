# Launching on Remote Server via SSH with `Jaynes`

This folder contains a working example for launching jobs with docker on a remote work station via ssh.

The code is first uploaded to `S3`.

result looks like:

![running instance screenshot](./figures/jaynes-output-ssh.png)

## Getting Started

You need to have `awscli` installed on your computer. To do so, run
```bash
pip install awscli
```

## Setting up your AWS Bucket

Take a look at the configuration file below, you need to have replace the following configurations for your machine:
```yaml
version: 0
mounts:
  - !mounts.S3Code
    s3_prefix: s3://ge-bair/jaynes-debug
    local_path: .
    host_path: /home/ubuntu/jaynes-mounts/{NOW:%Y-%m-%d}/{NOW:%H%M%S.%f}
    # container_path: /Users/geyang/learning-to-learn
    pypath: true
    excludes: "--exclude='*__pycache__' --exclude='*.git' --exclude='*.idea' --exclude='*.egg-info' --exclude='*.pkl'"
    compress: true
runner:
  !runners.Docker
  name: "some-job"  # only for docker
  image: "episodeyang/super-expert"
  startup: yes | pip install jaynes ml-logger -q
  envs: "LANG=utf-8"
  pypath: "{mounts[0].container_path}"
  launch_directory: "{mounts[0].container_path}"
  ipc: host
  use_gpu: false
launch:
  type: ssh
  ip: oberyn.banatao.berkeley.edu
  username: ubuntu
  pem: ~/.ssh/incrementium-berkeley
```

When you run the [./example_launch.py](launch_entry.py) script, it generates two pieces of script:

**1. A Local Script**

```bash
type gtar >/dev/null 2>&1 && alias tar=`which gtar`
mkdir -p '/private/var/folders/q9/qh3g18bs0vq3xjqtvv636vfmx6y0dw/T/tmpl5cmntgw'
# Do not use absolute path in tar.
tar --exclude='*__pycache__' --exclude='*.git' --exclude='*.idea' --exclude='*.egg-info' --exclude='*.pkl' -czf '/private/var/folders/q9/qh3g18bs0vq3xjqtvv636vfmx6y0dw/T/tmpl5cmntgw/3e95eff1-e180-49a4-ae6c-b88cdaa965d6.tar' -C '/Users/geyang/berkeley/packages/jaynes/example_projects/01_ssh_docker_configuration/.' .
aws s3 cp '/private/var/folders/q9/qh3g18bs0vq3xjqtvv636vfmx6y0dw/T/tmpl5cmntgw/3e95eff1-e180-49a4-ae6c-b88cdaa965d6.tar' 's3://ge-bair/jaynes-debug/3e95eff1-e180-49a4-ae6c-b88cdaa965d6.tar' --acl public-read-write
```

and 

**2. A Remote Host Script**

```bash
#!/bin/bash
# to allow process substitution
set +o posix
mkdir -p ~/debug-outputs
{
    # clear main_log
    truncate -s 0 ~/debug-outputs/jaynes-launch.log
    truncate -s 0 ~/debug-outputs/jaynes-launch.err.log

    if ! type aws > /dev/null; then
        pip install awscli --upgrade --user
    fi

    # remote_setup

        aws s3 cp 's3://ge-bair/jaynes-debug/3e95eff1-e180-49a4-ae6c-b88cdaa965d6.tar' '/tmp/3e95eff1-e180-49a4-ae6c-b88cdaa965d6.tar' --no-sign-request
        mkdir -p '/home/ubuntu/jaynes-mounts/2019-01-04/213434.826353'
        tar -zxf '/tmp/3e95eff1-e180-49a4-ae6c-b88cdaa965d6.tar' -C '/home/ubuntu/jaynes-mounts/2019-01-04/213434.826353'

    # upload_script

    # todo: include this inside the runner script.

    # sudo service docker start # this is optional.
    # docker pull episodeyang/super-expert

    echo 'kill running instances'
    docker kill some-job
    echo 'remove existing container with name'
    LANG=utf-8 docker rm some-job
    echo 'Now run docker'
    LANG=utf-8 docker run -i  --ipc=host -v '/home/ubuntu/jaynes-mounts/2019-01-04/213434.826353':'/Users/geyang/berkeley/packages/jaynes/example_projects/01_ssh_docker_configuration/.' --name 'some-job' \
    episodeyang/super-expert /bin/bash -c 'echo "Running in docker";yes | pip install jaynes ml-logger -q;export PYTHONPATH=$PYTHONPATH:/Users/geyang/berkeley/packages/jaynes/example_projects/01_ssh_docker_configuration/.;cd '/Users/geyang/berkeley/packages/jaynes/example_projects/01_ssh_docker_configuration/.';JAYNES_PARAMS_KEY=gASVsQcAAAAAAAB9lCiMBXRodW5rlIwXY2xvdWRwaWNrbGUuY2xvdWRwaWNrbGWUjA5fZmlsbF9mdW5jdGlvbpSTlChoAowPX21ha2Vfc2tlbF9mdW5jlJOUaAKMDV9idWlsdGluX3R5cGWUk5SMCENvZGVUeXBllIWUUpQoSwBLAEsBSwJLQ0MQZAF9AHQAfACDAQEAZABTAJROWP4FAAAKICAgICMgVGhlIEF3ZXNvbWUgTUwtTG9nZ2VyCiAgICAKICAgIFlvdSBjYW4gcnVuIHRoZSBmb2xsb3dpbmcgY29kZSB3aXRoIG1sLWxvZ2dlcjoKICAgIAogICAgYGBgcHl0aG9uCiAgICBmcm9tIG1sX2xvZ2dlciBpbXBvcnQgbG9nZ2VyCiAgICAKICAgIGxvZ2dlci5sb2cobHI9MCwgY2xpcCByYW5nZT0wLjIwMCwgc3RlcD0wLCB0aW1lc3RhbXA9JzIwMTgtMTEtMTZUMDA6MDk6MjcuMTk4MTQyJywgcmV3YXJkPS0xMDkuNDMpCiAgICBsb2dnZXIuZmx1c2goKQogICAgYGBgCiAgICDilZLilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilaTilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZUKICAgIOKUgiAgICAgICAgIGxyICAgICAgICAg4pSCICAgICAgICAgICAwLjAwMCAgICAgICAgICAgIOKUggogICAg4pSc4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pS84pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSkCiAgICDilIIgICAgIGNsaXAgcmFuZ2UgICAgIOKUgiAgICAgICAgICAgMC4yMDAgICAgICAgICAgICDilIIKICAgIOKUnOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUvOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUpAogICAg4pSCICAgICAgICBzdGVwICAgICAgICDilIIgICAgICAgICAgICAgMCAgICAgICAgICAgICAg4pSCCiAgICDilJzilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilLzilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilKQKICAgIOKUgiAgICAgIHRpbWVzdGFtcCAgICAg4pSCJzIwMTgtMTEtMTZUMDA6MDk6MjcuMTk4MTQyJ+KUggogICAg4pSc4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pS84pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSkCiAgICDilIIgICAgICAgcmV3YXJkICAgICAgIOKUgiAgICAgICAgICAtMTA5LjQzICAgICAgICAgICDilIIKICAgIOKVmOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVp+KVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVmwogICAglIaUjAVwcmludJSFlIwBc5SFlIxlL1VzZXJzL2dleWFuZy9iZXJrZWxleS9wYWNrYWdlcy9qYXluZXMvZXhhbXBsZV9wcm9qZWN0cy8wMV9zc2hfZG9ja2VyX2NvbmZpZ3VyYXRpb24vZXhhbXBsZV9sYXVuY2gucHmUjAZsYXVuY2iUSwRDBAAXBAGUKSl0lFKUSv////+MCF9fbWFpbl9flIeUUpR9lCiMB2dsb2JhbHOUfZSMCGRlZmF1bHRzlE6MBGRpY3SUfZSMDmNsb3N1cmVfdmFsdWVzlE6MBm1vZHVsZZRoGIwEbmFtZZRoFIwDZG9jlE6MCHF1YWxuYW1llGgUdXRSjARhcmdzlCmMBmt3YXJnc5R9lHUu python -u -m jaynes.entry'

} > >(tee -a ~/debug-outputs/jaynes-launch.log) 2> >(tee -a ~/debug-outputs/jaynes-launch.err.log >&2)
```

Then when you call `jaynes.run(fn, **keyword_arguments)`, `jaynes` sends the remote script to your remote host (the computer on which you want to run the job), and executes this script.

You can peek at this script by setting `verbose=True` in the `jaynes.config` call, or you can add that to the yaml file.

Now, the result is piped back via ssh to your computer at real time:

![running instance screenshot](./figures/jaynes-output-ssh.png)
