import streamlit as st

from pages.home_dashboard import home_page
from pages.ec2_dashboard import ec2_page
from pages.s3_dashboard import s3_page
from pages.docker_dashboard import docker_page
from pages.cloudwatch_dashboard import cloudwatch_page
from pages.k8s_dashboard import k8s_page


st.set_page_config(page_title="CloudOps Suite", page_icon="", layout="wide")

st.sidebar.title("CloudOps Suite")

page = st.sidebar.radio(
    "Services", ["Home", "EC2", "S3", "Docker", "CloudWatch", "Kubernetes"]
)

if page == "Home":

    home_page()

elif page == "EC2":

    ec2_page()

elif page == "S3":

    s3_page()

elif page == "Docker":

    docker_page()

elif page == "CloudWatch":

    cloudwatch_page()

elif page == "Kubernetes":

    k8s_page()
