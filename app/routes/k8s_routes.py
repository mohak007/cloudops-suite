from fastapi import APIRouter

from app.models.k8s_models import CreateDeploymentRequest

from app.services.k8s_service import (
    list_pods,
    list_services,
    create_namespace,
    create_deployment,
    scale_deployment,
    delete_deployment
)

router = APIRouter()


@router.get("/pods")
def get_pods():

    return list_pods()


@router.get("/services")
def get_services():

    return list_services()


@router.post("/create-namespace/{namespace}")
def create_ns(
    namespace: str
):

    return create_namespace(
        namespace
    )


@router.post("/create-deployment")
def deploy(
    data: CreateDeploymentRequest
):

    return create_deployment(
        data
    )


@router.post(
    "/scale-deployment/{deployment_name}/{replicas}"
)
def scale(
    deployment_name: str,
    replicas: int
):

    return scale_deployment(
        deployment_name,
        replicas
    )


@router.delete(
    "/delete-deployment/{deployment_name}"
)
def delete(
    deployment_name: str
):

    return delete_deployment(
        deployment_name
    )
