from pydantic import BaseModel


class RunContainerRequest(BaseModel):
    image_name: str
    container_name: str
    host_port: int
    container_port: int
