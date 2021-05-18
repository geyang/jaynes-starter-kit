# Launching On AWS with Jaynes and Docker

This folder contains a working example for launching jobs on EC2 with docker containers. At the end of the day, you would have 1. a python script and 2. a simple `.jaynes` script that allows you to scale your experiment instantly to thousands of instances on AWS.

```python
# launch_ec2.py

if __name__ == "__main__":
    import jaynes
    from your_project import train, Args

    jaynes.config()
    for seed in [100, 200, 300]:
        jaynes.run(train, seed=seed)
```



## Getting Started

You need to have `awscli` installed on your computer, as well as `jaynes`. 

```bash
pip install boto3
pip install jaynes
```

Then install your AWS cli according to these instructions: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-mac.html. You can verify that it is now installed via

```bash
$ which aws
/usr/local/bin/aws
$ aws --version
aws-cli/2.2.4 Python/3.8.8 Darwin/20.3.0 exe/x86_64 prompt/off
```

## AWS Profile and Credentials

Now to configure your aws credentials, follow the tutorials here: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html. You need to obtain your access key and secrete access key from your ec2 dashboard through this guide https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html.

```bash
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: json
```

### Supporting Multiple AWS CLI Profiles

Most of the time, you have multiple `aws` accounts that you use for work vs home projects. The best way to manage these different access credentials is to use **"profiles"**. You can set the `AWS_PROFILE` flag in your environment to select one as your default.

1. Inside your 

    ```ini
    [default]
    region=us-east-1
    output=text
    cli_pager=

    [profile your-org]
    region=us-east-1
    output=text
    cli_pager=
    s3 =
        max_concurrent_requests = 5
        max_queue_size = 10000
        multipart_threshold = 1MB
        multipart_chunksize = 1MB
        max_bandwidth = 300MB/s
        addressing_style = path
    ```

2. And then put this into your `~/.bashrc` file:

    ```bash
    export AWS_PROFILE=your-org
    ```
## Creating An S3 Bucket for Your Code and Data

After configuring your profile `your-org`, you should be able to look at the existing buckets using your current aws profile

```bash
aws s3api list-buckets
```

Details of the s3api could be found @[create  bucket](https://docs.aws.amazon.com/cli/latest/reference/s3api/create-bucket.html).

1. Now, create two buckets using the following command:

    ```bash
    aws s3api create-bucket --acl public-read-write --bucket $USER-jaynes-$AWS_PROFILE --region us-east-1
    aws s3api create-bucket --acl public-read-write --bucket $USER-data-$AWS_PROFILE --region us-east-1
    ```
2. If you mess up, remember even if you delete a bucket, it would take a while for its name to be released, so that you can recreate it using different settings. Just don't panic!

3. If you want to make the upload faster, you can enable the `accelerate_endpoint`.

    ```bash
    aws s3api put-bucket-accelerate-configuration --bucket your_bucket_name --accelerate-configuration Status=Enabled
    ```

    Note that this endpoint takes a while to spin up. Before it finishes spinning up, uploading and s3api using the accelerated endpoint would result into the following **S3 Upload Failure**:

    ```
    upload failed: An error occurred (InvalidRequest) when calling the PutObject operation: S3 Transfer Acceleration is not configured on this bucket
    ```

    When this happens, remove this `use_accelerate_endpont` line from  `~/.aws/config` file (**The last line**).

    ```ini
    [profile <your-profile>]
    ...
    s3 =
        use_accelerate_endpoint = true
    ```

    If larger file upload fails, you can put in these additional thresholding parameters. My config looks like this:

    ```ini
    [profile <your-profile>]
    region=us-east-1
    output=text
    cli_pager=
    s3 =
        use_accelerate_endpoint = true  # you can remove this if you have an endpoint error.
        max_concurrent_requests = 5
        max_queue_size = 10000
        multipart_threshold = 1MB
        multipart_chunksize = 1MB
        max_bandwidth = 300MB/s
        addressing_style = path
    ```

## Setting Up AWS Instance Profiles and Keys

We include these detailed setup and expectations as a list.

1. **Expected Environment Variables**, you need to have these in your [~/.profile](file://~/.profile).

   ```bash
   #~/.profile
   export ML_LOGGER_ROOT=http://<your logging server id>:8080
   export ML_LOGGER_USER=geyang
   export ML_LOGGER_TOKEN=""
   
   export AWS_PROFILE=<your-org>
   export JYNS_AWS_S3_BUCKET=$USER-jaynes-<your-org>
   export JYNS_AWS_INSTANCE_PROFILE=arn:aws:iam::<your-org-account>:instance-profile/ge-jaynes-worker
   ```

2. A list of Deep Learning AMI `image_ids`, one for each region is listed [./setup/ec2_image_ids.csv](./setup/ec2_image_ids.csv)

   ```
   Region, Image Id, Name,
   ap-northeast-1, ami-0c0e137eb96fcec44,  Deep Learning AMI (Amazon Linux) Version 44.1
   ap-northeast-2, ami-0bbc5115b8bab3b02, Deep Learning AMI (Amazon Linux) Version 44.1
   ap-south-1, ami-0fb6238e606fbadf8, Deep Learning AMI (Amazon Linux) Version 44.1
   ap-southeast-1, ami-0ba1614bbcc249f4b, Deep Learning AMI (Amazon Linux) Version 44.1
   ap-southeast-2, ami-069dac0ee54855944, Deep Learning AMI (Amazon Linux) Version 44.1
   eu-central-1, ami-0f06ff3e6c127ad45, Deep Learning AMI (Amazon Linux) Version 44.1
   eu-west-1, ami-05c2951a7e0123999, Deep Learning AMI (Amazon Linux) Version 44.1
   sa-east-1, ami-02049815b31982d90, Deep Learning AMI (Amazon Linux) Version 44.1
   us-east-1, ami-0c5f0a577c97b13a8, Deep Learning AMI (Amazon Linux) Version 44.1
   us-east-2, ami-067146664e0b80d8b, Deep Learning AMI (Amazon Linux) Version 44.1
   us-west-1, ami-0e32a3ff68ac83e10, Deep Learning AMI (Amazon Linux) Version 44.1
   us-west-2, ami-0cf77af10d63c7969, Deep Learning AMI (Amazon Linux) Version 44.1
   ```

3. pem key, one for each region: You need to generate this for yourself. Please run the [./ec2_setup/setup_aws.py](./ec2_setup/setup_aws.py) script from inside that folder.
    ```bash
    cd ec2_setup
    python setup_aws.py
    ```
    This should **first generate a set of access key pairs**, inside the [./private](./private) folder.
    Second, it should also generates an ec2 instance profile. Write down the instance profile's name, go to the next step.
4. Add `JYNS_AWS_INSTANCE_PROFILE` to your [~/.profile](file://~/.profile), using the value of the instance profile you generated in the previous step.

## Docker Image

We include an example docker image in the [./docker/Dockerfile](./docker) file. You need to install `jaynes` via `RUN pip install jaynes` in the docker image, to make the jaynes entry script available.

## Launch

Now the launch is as simple as running
```bash
python launch_entry.py
```
Remember, turn on the  `verbose=True` flag, to see the script being generated and details of the request.

### Common Errors

- error: **bad-parameters** that occurs during spot instance request contains a short message after that explains the specific parameter at fault. You can use `aws ec2 describe-spot-instance-requests` command to inspect the details.

## Under The Hood

When you run the [./example_launch.py](launch_entry.py) script, it generates two pieces of script:

> **A local script** and **a remote host script**

Then when you call `jaynes.run(fn, **keyword_arguments)`, `jaynes` uses `boto3` to launch an aws spot/on-demand 
instance, and attaches the script to the launch request. When the instance is ready, this launch script would be ran. There is a maximum length limit for this launch script. Because we serialize your python function, it is best to keep the function short, so that the `JAYNS_ENTRY` environment variable is not too large. Large entry function can cause the launch to fail silently. 

You can take a peek at this script by setting `verbose=True` in the `jaynes.config` call, or you can add this 
`verbose` flag to the yaml file.

EC2 and GCE launches via jaynes does not support real-time pipe-back.

Here is the ec2 instance inside the AWS console:

![./figures/launched-ec2-screenshot.png](figures/launched-ec2-screenshot-1043600.png)