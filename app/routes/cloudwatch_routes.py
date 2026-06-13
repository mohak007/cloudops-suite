from fastapi import APIRouter

from app.services.cloudwatch_service import (
    get_ec2_cpu_utilization,
    get_network_in,
    get_network_out,
    get_disk_read_bytes,
    get_disk_write_bytes
)

router = APIRouter()


@router.get(
    "/ec2-cpu/{instance_id}"
)
def cpu_utilization(
    instance_id: str
):

    return get_ec2_cpu_utilization(
        instance_id
    )
@router.get("/network-in/{instance_id}")
def network_in(instance_id: str):

    return get_network_in(instance_id)


@router.get("/network-out/{instance_id}")
def network_out(instance_id: str):

    return get_network_out(instance_id)


@router.get("/disk-read/{instance_id}")
def disk_read(instance_id: str):

    return get_disk_read_bytes(instance_id)


@router.get("/disk-write/{instance_id}")
def disk_write(instance_id: str):

    return get_disk_write_bytes(instance_id)
