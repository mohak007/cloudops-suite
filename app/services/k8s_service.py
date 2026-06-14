from kubernetes import client, config

# from kubernetes.config.config_exception import ConfigException
from app.utils.logger import logger
from app.models.k8s_models import CreateDeploymentRequest

try:

    config.load_kube_config()

    core_api = client.CoreV1Api()

    apps_api = client.AppsV1Api()


except Exception as error:

    logger.warning(f"Kubernetes not available: {error}")

    core_api = None

    apps_api = None


def list_pods():
    if core_api is None:

        return {"error": "Kubernetes cluster not configured"}

    pods = core_api.list_pod_for_all_namespaces()

    return [
        {
            "name": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "status": pod.status.phase,
        }
        for pod in pods.items
    ]


def list_services():
    if core_api is None:

        return {"error": "Kubernetes cluster not configured"}

    services = core_api.list_service_for_all_namespaces()

    return [
        {
            "name": service.metadata.name,
            "namespace": service.metadata.namespace,
            "type": service.spec.type,
        }
        for service in services.items
    ]


def create_namespace(namespace: str):
    if core_api is None:

        return {"error": "Kubernetes cluster not configured"}

    body = client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace))

    core_api.create_namespace(body)

    return {"message": f"Namespace {namespace} created"}


def create_deployment(data: CreateDeploymentRequest):
    if apps_api is None:

        return {"error": "Kubernetes cluster not configured"}

    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=data.deployment_name),
        spec=client.V1DeploymentSpec(
            replicas=data.replicas,
            selector=client.V1LabelSelector(match_labels={"app": data.deployment_name}),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": data.deployment_name}),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(name=data.deployment_name, image=data.image)
                    ]
                ),
            ),
        ),
    )

    apps_api.create_namespaced_deployment(namespace=data.namespace, body=deployment)

    return {"message": f"Deployment {data.deployment_name} created"}


def scale_deployment(deployment_name: str, replicas: int, namespace="default"):
    if apps_api is None:

        return {"error": "Kubernetes cluster not configured"}

    deployment = apps_api.read_namespaced_deployment(deployment_name, namespace)

    deployment.spec.replicas = replicas

    apps_api.patch_namespaced_deployment(deployment_name, namespace, deployment)

    return {"message": f"Scaled to {replicas} replicas"}


def delete_deployment(deployment_name: str, namespace="default"):
    if apps_api is None:

        return {"error": "Kubernetes cluster not configured"}

    apps_api.delete_namespaced_deployment(deployment_name, namespace)

    return {"message": f"{deployment_name} deleted"}
