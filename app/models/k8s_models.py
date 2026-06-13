from pydantic import BaseModel

class CreateDeploymentRequest(BaseModel):

    deployment_name: str
    image: str
    replicas: int = 1
    namespace: str = "default"
    
