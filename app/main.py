from fastapi import FastAPI
from app.routes.ec2_routes import router as ec2_router
from app.routes.docker_routes import (
    router as docker_router
    )
from app.routes.deployment_routes import (
    router as deployment_router
    )
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import(AWSOperationException)

from app.routes.s3_routes import (
    router as s3_router
    )
from app.routes import cloudwatch_routes
from app.routes import k8s_routes
app = FastAPI(
    title="CloudOps Automation Suite"
)

app.include_router(
    ec2_router,
    prefix="/ec2",
    tags=["EC2 Automation"]
)

app.include_router(
    docker_router,
    prefix="/docker",
    tags=["Docker Automation"]
    )

app.include_router(
    deployment_router,
    prefix="/deploy",
    tags=["Deployment Automation"]
)



app.include_router(
    s3_router,
    prefix = "/s3",
    tags=["s3 Automation"]
    )

app.include_router(
    cloudwatch_routes.router,
    prefix="/cloudwatch",
    tags=["cloudwatch Monitoring"]
    )

app.include_router(
    k8s_routes.router,
    prefix="/k8s",
    tags=["kubernetes"]
    )
@app.exception_handler(
AWSOperationException
)
async def aws_exception_handler(request,exc):

    return JSONResponse(

    status_code=500,

    content={
        "error": str(exc)
    }
)
@app.get("/")
def health_check():

    return {
        "status": "running"
    }
