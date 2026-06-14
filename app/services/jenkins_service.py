import jenkins

from app.config.settings import JENKINS_URL, JENKINS_USERNAME, JENKINS_API_TOKEN

from app.utils.logger import logger


server = jenkins.Jenkins(
    JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_API_TOKEN
)


def list_jobs():

    try:

        jobs = server.get_jobs()

        return jobs

    except Exception as error:

        logger.error(str(error))

        return {"error": str(error)}


def trigger_job(job_name: str):

    try:

        server.build_job(job_name)

        return {"message": f"Build triggered for {job_name}"}

    except Exception as error:

        logger.error(str(error))

        return {"error": str(error)}


def get_build_status(job_name: str):

    try:

        job_info = server.get_job_info(job_name)

        return {"job_name": job_name, "last_build": job_info["lastBuild"]}

    except Exception as error:

        logger.error(str(error))

        return {"error": str(error)}


def get_console_output(job_name: str):

    try:

        last_build_number = server.get_job_info(job_name)["lastCompletedBuild"][
            "number"
        ]

        output = server.get_build_console_output(job_name, last_build_number)

        return {"console_output": output}

    except Exception as error:

        logger.error(str(error))

        return {"error": str(error)}
