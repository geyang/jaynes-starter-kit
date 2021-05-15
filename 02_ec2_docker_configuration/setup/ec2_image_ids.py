import boto3

from setup_aws import AWS_REGIONS


def list_image_by_region(image_id=None, name=None, region=None):
    ec2 = boto3.client("ec2", region_name=region, )
    amis = ec2.describe_images(Owners=['amazon'])['Images']
    pred = lambda ami: ami.get('Name', None) == name or ami['ImageId'] == image_id
    return [dict(region=region,
                 image_id=img['ImageId'],
                 name=img['Name']) for img in filter(pred, amis)]


if __name__ == "__main__":
    from tqdm import tqdm
    import yaml

    image_list = {
        region: list_image_by_region(name="Deep Learning AMI (Amazon Linux) Version 44.1", region=region)[0]
        for region in tqdm(AWS_REGIONS)
    }
    with open("ec2_image_ids.yml", 'w+') as f:
        yaml.dump(image_list, f)
