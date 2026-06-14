from fastapi import APIRouter
from app.models.ec2_models import EC2CreateRequest

from app.services.ec2_service import (
    create_ec2_instance,
    list_ec2_instances,
    stop_ec2_instance,
    start_ec2_instance,
    terminate_ec2_instance,
)

router = APIRouter()


@router.post("/create-instance")
def launch_instance(data: EC2CreateRequest):

    return create_ec2_instance(data)


@router.get("/list-instances")
def get_instances():

    return list_ec2_instances()


@router.get("/stop-instance/{instance_id}")
def stop_instance(instance_id: str):

    return stop_ec2_instance(instance_id)


@router.get("/start-instance/{instance_id}")
def start_instance(instance_id: str):

    return start_ec2_instance(instance_id)


@router.delete("/terminate-instance/{instance_id}")
def terminate_instance(instance_id: str):

    return terminate_ec2_instance(instance_id)
