from fastapi import APIRouter

from app.services.deployment_service import deploy_container_to_ec2

router = APIRouter()


@router.post("/deploy-nginx")
def deploy_nginx():

    return deploy_container_to_ec2(
        host="13.233.177.3", username="ubuntu", pem_file="YOUR_KEY.pem"
    )
