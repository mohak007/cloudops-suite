import docker

from app.utils.logger import logger
from pydantic import BaseModel
docker_client = docker.from_env()

def build_docker_image():

    try:

        logger.info("Building Docker image")

        image, logs = docker_client.images.build( path=".", tag="cloudops-app:latest")

        logger.info("Docker image built successfully")

        return {
            "message": "Docker image built successfully",
            "image_tags": image.tags
            }
    except Exception as error:

        logger.error(f"Docker build failed: {str(error)}")

        return {
            "error": str(error)
            }

def run_container(data):

    try:

        container = docker_client.containers.run(
            image=data.image_name,
            name=data.container_name,
            detach=True,
            ports={
                f"{data.container_port}/tcp":
                data.host_port
            }
        )

        return {
            "container_id": container.id,
            "container_name": container.name,
            "status": "running"
        }

    except Exception as error:

        logger.error(str(error))

        return {
            "error": str(error)
        }
    
def list_containers():

        containers = docker_client.containers.list( all=True)
        return [{
            "id" : container.id[::12],
            "name":container.name,
            "status" : container.status,
            "image" : str(container.image.tags)
            }
                for container in containers
        ]
def get_container_logs(container_id: str):

        container = docker_client.containers.get(container_id)
        return {"logs" : container.logs().decode()}

def stop_container(container_id : str):
        container = docker_client.containers.get(container_id)
        container.stop()
        return{"Message" : f"{container_id} stopped" }

def remove_container(container_id : str):
        container = docker_client.containers.get(container_id)
        container.remove(force=True)
        return{"Message" : f"{container_id} removed" }
 
def list_images():

    images = docker_client.images.list()

    return [
        {
            "id": image.id.split(":")[1][:12],
            "tags": image.tags,
            "size_mb": round(image.attrs["Size"] / (1024 * 1024), 2)
        }
        for image in images
        ]
def remove_image(image_name: str):
    try:
        docker_client.images.remove(
            image=image_name,
            force=True
            )
        return {
            "message" : f"{image_name} removed"
            }
    except Exception as error:
        logger.error(str(error))
        return {
            "error": str(error)
            }
def get_container_status(container_id: str):
    try:
        container = docker_client.containers.get(container_id)
        return{
            "container_id" : container.id[::12],
            "name" : container.name,
            "status" : container.status,
            "image" : container.image.tags,
            "ports": container.attrs["NetworkSettings"]["Ports"]
            }
    except Exception as error:
        logger.error(str(error))
        return {"error" : str(error) }


def list_images():

    try:

        images = docker_client.images.list()

        result = []

        for image in images:

            result.append({

                "image_id":
                image.short_id,

                "tags":
                image.tags
            })

        return result

    except Exception as error:

        logger.error(
            str(error)
        )

        return {

            "error": str(error)
        }
def remove_image(image_name: str):

    try:

        logger.info(
            f"Removing image: {image_name}"
        )

        docker_client.images.remove(
            image=image_name,
            force=True
        )

        logger.info(
            f"Image removed successfully: {image_name}"
        )

        return {

            "image_name": image_name,

            "message":
            "Image removed successfully"
        }

    except Exception as error:

        logger.error(
            str(error)
        )

        return {

            "error": str(error)
        }
