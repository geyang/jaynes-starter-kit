import os
import sys

import boto3
import botocore
from termcolor import cprint
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_DIR = REPO_DIR

AWS_PROFILE = os.environ['AWS_PROFILE']
print(f'You are using the AWS profile {AWS_PROFILE}')

USER = os.environ['USER']
PREFIX = f"{USER}-jaynes"
SECURITY_GROUP_NAME = f"{PREFIX}-sg"
INSTANCE_PROFILE_NAME = f"{PREFIX}-worker"
INSTANCE_ROLE_NAME = f"{PREFIX}-role"

AWS_REGIONS = [
    "ap-northeast-1", "ap-northeast-2", "ap-south-1", "ap-southeast-1",
    "ap-southeast-2", "eu-central-1", "eu-west-1", "sa-east-1", "us-east-1",
    "us-east-2", "us-west-1", "us-west-2", ]


def remove_instance_profile():
    iam = boto3.resource('iam')
    iam_client = boto3.client("iam")

    try:
        iam_client.remove_role_from_instance_profile(
            InstanceProfileName=INSTANCE_PROFILE_NAME,
            RoleName=INSTANCE_ROLE_NAME)
    except:
        pass
    try:
        iam_client.delete_instance_profile(InstanceProfileName=INSTANCE_PROFILE_NAME)
    except:
        pass

    try:
        existing_role = iam.Role(INSTANCE_ROLE_NAME)
        existing_role.load()

        for prof in existing_role.instance_profiles.all():
            for role in prof.roles:
                prof.remove_role(RoleName=role.name)
                cprint(f'removing {role.name}', 'green')
            cprint(f'removing {prof}', 'green')
            prof.delete()
        for policy in existing_role.policies.all():
            policy.delete()
        for policy in existing_role.attached_policies.all():
            existing_role.detach_policy(PolicyArn=policy.arn)
        existing_role.delete()
    except:
        pass


def setup_instance_profile():
    iam_client = boto3.client("iam")
    iam = boto3.resource('iam')

    iam_client.create_role(Path='/', RoleName=INSTANCE_ROLE_NAME,
                           AssumeRolePolicyDocument=open("role-policy.json", 'r').read())

    role = iam.Role(INSTANCE_ROLE_NAME)
    role.attach_policy(PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess')
    role.attach_policy(PolicyArn='arn:aws:iam::aws:policy/ResourceGroupsAndTagEditorFullAccess')

    iam_client.put_role_policy(RoleName=role.name, PolicyName='JaynesWorker',
                               PolicyDocument=open("additional-policies.json", 'r').read())

    iam_client.create_instance_profile(InstanceProfileName=INSTANCE_PROFILE_NAME)
    iam_client.add_role_to_instance_profile(InstanceProfileName=INSTANCE_PROFILE_NAME,
                                            RoleName=INSTANCE_ROLE_NAME)


def setup_security_groups(region):
    ec2 = boto3.resource("ec2", region_name=region, )
    ec2_client = boto3.client("ec2", region_name=region, )

    existing_vpcs = list(ec2.vpcs.all())
    assert len(existing_vpcs) >= 1, f"There is no existing vpc in {region}"
    for vpc in existing_vpcs:
        try:
            security_group, *_ = list(vpc.security_groups.filter(GroupNames=[SECURITY_GROUP_NAME]))
            break
        except:
            pass
    else:
        cprint(f"Creating security group in VPC {vpc.id}", "blue", end="\r")
        security_group = vpc.create_security_group(
            GroupName=SECURITY_GROUP_NAME, Description='Security group for Jaynes')
        ec2_client.create_tags(Resources=[security_group.id],
                               Tags=[dict(Key='Name', Value=SECURITY_GROUP_NAME)])
        cprint(f"Created security group in VPC {vpc.id}", "green")

    try:
        cprint(f"Authorizing Ingress...", "blue", end="\r")
        security_group.authorize_ingress(FromPort=22, ToPort=22, IpProtocol='tcp', CidrIp='0.0.0.0/0')
    except botocore.exceptions.ClientError as e:
        assert e.response['Error']['Code'] == 'InvalidPermission.Duplicate'
    cprint(f"Security group {security_group.id} is created.", "green")

    return security_group.id


def setup_key_pairs(region, key_name):
    ec2_client = boto3.client("ec2", region_name=region, )
    try:
        cprint(f"Creating key pair with name {key_name}...", "blue", end="\r")
        key_pair = ec2_client.create_key_pair(KeyName=key_name)
        cprint(f"Created key pair with name {key_name}...", "green")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'InvalidKeyPair.Duplicate':
            if not query_yes_no("Key pair with name %s exists. Proceed to delete and recreate?" % key_name, "no"):
                sys.exit()
            cprint(f"Deleting existing key pair with name {key_name}", "red", end="\r")
            ec2_client.delete_key_pair(KeyName=key_name)
            cprint(f"Recreating key pair with name {key_name}...", "blue", end="\r")
            key_pair = ec2_client.create_key_pair(KeyName=key_name)
            cprint(f"Recreated key pair {key_name}", "green", end="\r")
        else:
            raise e

    key_pair_folder_path = os.path.join(CONFIG_DIR, f"{AWS_PROFILE}.secret")
    file_name = os.path.join(key_pair_folder_path, "%s.pem" % key_name)

    cprint(f"Saving key pair {key_name}", "green", end="\r")
    os.makedirs(key_pair_folder_path, exist_ok=True)
    with os.fdopen(os.open(file_name, os.O_WRONLY | os.O_CREAT, 0o600), 'w') as handle:
        handle.write(key_pair['KeyMaterial'] + '\n')
    cprint(f"Saved key pair {key_name}", "green")
    return key_name


def get_subnets_info(region):
    client = boto3.client("ec2", region_name=region, )
    subnets = client.describe_subnets()['Subnets']
    return [n['AvailabilityZone'] for n in subnets]


def query_yes_no(question, default="yes", allow_skip=False):
    """Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).
    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if allow_skip:
        valid["skip"] = "skip"
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    if allow_skip:
        prompt += " or skip"
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


if __name__ == "__main__":
    import yaml

    all_subnets = sum(map(get_subnets_info, tqdm(AWS_REGIONS)), [])
    with open('ec2_subnets.yml', 'w+') as f:
        yaml.dump(all_subnets, f)

    remove_instance_profile()
    setup_instance_profile()
    sg_ids = list(map(setup_security_groups, AWS_REGIONS))
    [setup_key_pairs(region, f"{USER}-{region}") for region in AWS_REGIONS]
