from fastapi import APIRouter
from app.models.s3_models import CreateBucketRequest
from fastapi import UploadFile
from fastapi import File
from app.services.s3_service import (
    create_bucket,
    list_buckets,
    upload_file,
    delete_object,
)

router = APIRouter()


@router.post("/create-bucket")
def create_s3_bucket(data: CreateBucketRequest):
    return create_bucket(data.bucket_name)


@router.get("/list-buckets")
def get_buckets():
    return list_buckets()


@router.post("/upload-file/{bucket_name}")
def upload_s3_file(bucket_name: str, file: UploadFile = File(...)):
    return upload_file(bucket_name, file)


@router.post("/delete-object/{bucket_name}/{object_name}")
def delete_s3_objects(bucket_name: str, object_name: str):
    return delete_object(bucket_name, object_name)
