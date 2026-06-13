import boto3
import os
from app.utils.logger import logger




AWS_REGION = os.getenv("AWS_REGION")
s3_client = boto3.client("s3")

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION
    )

def create_bucket(bucket_name: str):
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint" : AWS_REGION
                }
            )
        logger.info(
            f"Bucket created: {bucket_name}"
            )
        return{
            "message" : f"Bucket{bucket_name} created successfully"
            }
    except Exception as error:
        logger.error(str(error))
        return {
            "error" : str(error)
            }
def list_buckets():
    try:
        response = s3_client.list_buckets()
        return {
            "bucket" : [
                bucket["Name"]
                for bucket in response["Buckets"]
                ]
            }
    except Exception as error:
        logger.error(str(error))
        return {
            "error": str(error)
            }

def upload_file(bucket_name: str, file):
    try:
        s3_client.upload_fileobj(
            file.file,
            bucket_name,
            file.filename
            )
        return {"message": f"{file.filename} uploaded successfully"}

    except Exception as error:
        logger.error(str(error))
        return {"error": str(error)}

def list_objects(bucket_name: str):
    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name
            )
        return{
            "objects": [obj["Key"] for obj in response.get("Contents", [])
                        ]
            }
    except Exception as error:
        logger.error(str(error))
        return{"error": str(error)}

def delete_object(bucket_name: str, object_name: str):
    try:
        s3_client.delete_object( Bucket=bucket_name, Key=object_name)
        return {
            "message": f"{object_name} deleted"
            }
    except Exception as error:
        logger.error(str(error))
        return {"error" : str(error)}
