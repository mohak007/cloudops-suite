from pydantic import BaseModel, Field
from typing import List

class EC2CreateRequest(BaseModel):

    instance_type: str = Field(
        default="t3.micro",
        example="t3.micro"
    )

    instance_name: str = Field(
        default="dev-server",
        example="dev-server"
    )
    security_group_name: str
    key_pair_name: str
    ports: List[int] = [22]
