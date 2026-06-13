from dotenv import load_dotenv
import os
import boto3
from app.config.settings import AWS_REGION
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

#ec2_client = boto3.client(
#"ec2",
#aws_access_key_id=AWS_ACCESS_KEY_ID,
##aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
##region_name=AWS_REGION
#)
ec2_client = boto3.client(
    "ec2",
    region_name=AWS_REGION
)

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION
)

cloudwatch_client = boto3.client(
    "cloudwatch",
    region_name=AWS_REGION
)
