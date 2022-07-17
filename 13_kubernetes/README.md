# Jaynes Guide for Kubernetes

This tutorial contains a working example of using `jaynes` to launch multiple jobs on a kubernetes cluster.

## Authenticating with Kubernetes

From the cluster admin, you should be able to obtain a `config` file, that you can place under you `~/.kube/config` path. 

```bash
mv ~/Downloads/config ~/.kube/config
```

After this, your `kubectl` should just work.

```bash
kubectl get pods
```

## Quick Start

This is a self-contained example that should work out of the box. First, make sure that your S3 bucket is setup correctly:  Make a copy of the `.secret.template.yml` -> `.secrete.yml` file in this example project. Edit this secret file, to include your S3 bucket name

```bash
mv .secret.template.yml .secret.yml
vim .secret.yml
```

Inside [.secrete.yml](.secrete.yml), put in the name of your bucket.

Then, run

```bash
python launch_entry.py
```

For an example that launches multiple pods, where multiple training jobs runs within each pod, you can look at 

```bash
python launch_chained_entries.py
```

```python
from time import sleep


def train_fn(seed=None):
    from ml_logger import logger

    sleep(1)
    if seed:
        print(f"{logger.slurm_job_id} seed={seed}")
    else:
        print('done.')


if __name__ == "__main__":
    import jaynes

    jaynes.config()
    jaynes.add(train_fn, seed=100) \
        .chain(train_fn, seed=200) \
        .chain(train_fn, seed=300) \
        .chain(train_fn, seed=400) \
        .chain(train_fn, seed=500)
    jaynes.add(train_fn, seed=600) \
        .chain(train_fn, seed=700) \
        .chain(train_fn, seed=800) \
        .chain(train_fn, seed=900) \
        .chain(train_fn, seed=1000)
    jaynes.execute()
    jaynes.listen()
```

## Detailed Setup Guide

### Kubernetes Examples

The [kube_examples](kube_examples) folder contains examples of working kube job config files. For details of the setup and a simple tutorial, refer to https://ucsd-prp.gitlab.io. They offer a very nice collection of examples.

### Setting Up S3 access

We use a publically accessible S3 bucket for uploading and downloading the code snapshot. Using `aws s3 cp` requires setting up local credentials. We by-pass this need by setting the code upload to be publically accessible. For details, refer to the [./jaynes.yml](./jaynes.yml) file in this example project.

### Getting a list of GPU Types

```bash
kubectl get nodes -L nvidia.com/gpu.product
```

## How To Debug

Use `desribe` to inspect the error messages.

```bash
kubectl describe pods <pod-id>
```

## Setting up secret for dockerhub login

Create a secret using this with a name `<secret-nam>` and put the secret under `image_pull_secret` field.

```bash
kubectl create secret docker-registry <secret-name> \
     --docker-server=docker.io --docker-username=<usernam> \
     --docker-password <your password>  \
     --docker-email <your email>
```