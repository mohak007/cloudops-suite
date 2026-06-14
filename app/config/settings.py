import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
DEFAULT_INSTANCE_TYPE = os.getenv("DEFAULT_INSTANCE_TYPE", "t3.micro")
KEY_PAIR_NAME = os.getenv("KEY_PAIR_NAME", "cloudops-key")
JENKINS_URL = os.getenv("JENKINS_URL", "http://localhost:8080")


JENKINS_USERNAME = os.getenv("JENKINS_USERNAME", "admin")


JENKINS_API_TOKEN = os.getenv("JENKINS_API_TOKEN")


DEFAULT_INSTANCE_TYPE = os.getenv("DEFAULT_INSTANCE_TYPE", "t2.micro")

DEFAULT_AMI_ID = os.getenv("DEFAULT_AMI_ID")

SECURITY_GROUP_NAME = os.getenv("SECURITY_GROUP_NAME", "cloudops-sg")

DOCKER_IMAGE_TAG = os.getenv("DOCKER_IMAGE_TAG", "cloudops-app:latest")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

USER_DATA_SCRIPT = """#!/bin/bash
        apt update -y
        apt install docker.io -y
        systemctl start docker
        systemctl enable docker
        docker --version> /home/ubuntu/docker-version.txt
        """
