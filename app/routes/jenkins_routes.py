from fastapi import APIRouter

from app.services.jenkins_service import (
    list_jobs,
    trigger_job,
    get_build_status,
    get_console_output,
)

router = APIRouter()


@router.get("/jobs")
def jobs():

    return list_jobs()


@router.post("/trigger-job/{job_name}")
def trigger(job_name: str):

    return trigger_job(job_name)


@router.get("/build-status/{job_name}")
def build_status(job_name: str):

    return get_build_status(job_name)


@router.get("/console-output/{job_name}")
def console_output(job_name: str):

    return get_console_output(job_name)
