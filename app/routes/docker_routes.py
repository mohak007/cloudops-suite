from fastapi import APIRouter
from app.models.docker_models import RunContainerRequest
from app.services.docker_service import (
    build_docker_image,
    run_container,
    list_containers,
    get_container_logs,
    stop_container,
    remove_container,
    list_images,
    remove_image,
    get_container_status
)

router = APIRouter()

@router.post("/build-image")
def build_image():
    return build_docker_image()

@router.post("/run-container")
def start_container(
    data: RunContainerRequest
):
    return run_container(data)

@router.get("/list-containers")
def list_container():
    return list_containers()

@router.get("/container-logs/{container_id}")
def logs(container_id: str):
    return get_container_logs(container_id)

@router.post("/stop-container/{container_id}")
def stop(container_id: str):
    return stop_container(container_id)

@router.delete("/remove-container/{container_id}")
def remove(container_id: str):
    return remove_container(container_id)
@router.get("/images")
def images():
    return list_images()


@router.delete("/image/{image_name}")
def delete_image(image_name: str):
    return remove_image(image_name)


@router.get("/container-status/{container_id}")
def container_status(container_id: str):
    return get_container_status(container_id)

@router.get("/list-images")
def list_images_route():
    return list_images()
@router.delete(
    "/remove-image/{image_name}"
)
def delete_image(
    image_name: str
):

    return remove_image(
        image_name
    )
