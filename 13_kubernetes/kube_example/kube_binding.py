from kubernetes import client, config

config.load_kube_config()

v1 = client.CoreV1Api()


def get_pods():
    # Configs can be set in Configuration class directly or using helper utility
    print("Listing pods with their IPs:")
    # ret = v1.get_api_resources()
    # ret = config.list_kube_config_contexts()
    # ret = v1.list_pod_for_all_namespaces(watch=False)
    ret = v1.list_namespaced_pod(namespace="rl-dev")
    for i in ret.items:
        print(f"{i.status.pod_ip}\t{i.metadata.namespace}\t{i.metadata.name}, {i.status.phase}")


get_pods()


# create_pot()
def create_pod(image):
    pod = client.V1Pod()
    pod.metadata = client.V1ObjectMeta(name="test-pod")

    # this is the
    pod.ttlSecondsAfterFinished = 10

    container = client.V1Container(name="test-container", image=image, args=["sleep", "10000"])

    container.resources = client.V1ResourceRequirements()
    container.resources.requests = {"cpu": "50m", "memory": "50Mi", "nvidia.com/gpu": 1}
    container.resources.limits = {"cpu": "100m", "memory": "200Mi", "nvidia.com/gpu": 1}

    pod.spec = client.V1PodSpec(containers=[container])

    v1.create_namespaced_pod(namespace="rl-dev", body=pod)


# create_pod("improbableailab/model-free:latest")
def delete_pods(pod_name):
    v1.delete_namespaced_pod(name=pod_name, namespace="rl-dev", body=client.V1DeleteOptions())


delete_pods("test-pod")
