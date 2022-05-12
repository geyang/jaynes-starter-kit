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

This is a self-contained example that should work out of the box. Run

```bash
python 
```







## Launching Jobs

The [kube_examples](kube_examples) folder contains examples of working kube job config files. For details of the setup and a simple tutorial, refer to https://ucsd-prp.gitlab.io. They offer a very nice collection of examples.

## Setting Up S3 access

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