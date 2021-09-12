import os
import time

import googleapiclient.discovery
from params_proto.neo_proto import ParamsProto, Proto
from six.moves import input


def list_instances(compute, project_id, zone):
    result = compute.instances().list(project=project_id, zone=zone).execute()
    return result['items'] if 'items' in result else None


def create_instance(compute, project_id, zone, machine_type, name, preemptible=False):
    # Get the latest Debian Jessie image.
    image_response = compute.images().getFromFamily(project='debian-cloud', family='debian-9').execute()
    source_disk_image = image_response['selfLink']
    print(source_disk_image)

    # Configure the machine
    startup_script = open(os.path.join(os.path.dirname(__file__), 'startup-script.sh'), 'r').read()

    config = {
        'name': name,
        'machineType': f"zones/{zone}/machineTypes/{machine_type}",
        'scheduling': dict(preemptable=preemptible),

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [{
                # Startup script is automatically executed by the
                # instance upon startup.
                'key': 'startup-script',
                'value': startup_script
            }]
        },
    }

    return compute.instances().insert(
        project=project_id,
        zone=zone,
        body=config).execute()


def delete_instance(compute, project_id, zone, name):
    return compute.instances().delete(
        project=project_id,
        zone=zone,
        instance=name).execute()


def wait_for_operation(compute, project_id, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project_id,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)


def main(project_id, bucket_name, zone, machine_type, instance_name, wait=True):
    compute = googleapiclient.discovery.build('compute', 'v1')

    print('Creating instance.')

    operation = create_instance(compute, project_id, zone, machine_type, instance_name, bucket_name)
    wait_for_operation(compute, project_id, zone, operation['name'])

    instances = list_instances(compute, project_id, zone)

    print('Instances in project %s and zone %s:' % (project_id, zone))
    for instance in instances:
        print(' - ' + instance['name'])

    print("""
Instance created.
It will take a minute or two for the instance to complete work.
Check this URL: http://storage.googleapis.com/{}/output.png
Once the image is uploaded press enter to delete the instance.
""".format(bucket_name))

    if wait:
        input()

    print('Deleting instance.')

    operation = delete_instance(compute, project_id, zone, instance_name)
    wait_for_operation(compute, project_id, zone, operation['name'])


class CreateInstance(ParamsProto):
    """Example of using the Compute Engine API to create and delete instances.

    Creates a new compute engine instance and uses it to apply a caption to
    an image.

        https://cloud.google.com/compute/docs/tutorials/python-guide

    For more information, see the README.md under /compute.
    """
    project_id = Proto(env="JYNS_GCE_PROJECT", help='Your Google Cloud project ID.')
    bucket_name = Proto(env="USER_GCE_BUCKET", help='Your Google Cloud Storage bucket name.')
    machine_type = Proto("n1-standard-1", help="availability depends on region.")
    zone = Proto('us-central1-f', help='Compute Engine zone to deploy to.')
    instance_name = Proto('demo-instance', help='New instance name.')


if __name__ == '__main__':
    main(**vars(CreateInstance))
