import streamlit as st

from utils.api_client import get


def safe_count(response):

    if isinstance(response, list):
        return len(response)

    if isinstance(response, dict):

        # Handle wrapped responses like:
        # {"buckets": [...]}
        if "bucket" in response and isinstance(response["bucket"], list):
            return len(response["bucket"])

        if "instances" in response and isinstance(response["instances"], list):
            return len(response["instances"])

        if "containers" in response and isinstance(response["containers"], list):
            return len(response["containers"])

        if "pods" in response and isinstance(response["pods"], list):
            return len(response["pods"])

    return 0


def home_page():

    st.title("CloudOps Suite")

    st.markdown("Manage AWS, Docker and Kubernetes resources from one dashboard.")

    try:

        ec2_instances = get("/ec2/list-instances")

    except Exception:

        ec2_instances = []

    try:

        buckets = get("/s3/list-buckets")

    except Exception:

        buckets = []

    try:

        containers = get("/docker/list-containers")

    except Exception:

        containers = []

    try:

        pods = get("/k8s/pods")

    except Exception:

        pods = []

    col1, col2 = st.columns(2)

    with col1:

        st.metric("EC2 Instances", safe_count(ec2_instances))

        st.metric("Docker Containers", safe_count(containers))

    with col2:

        st.metric("Kubernetes Pods", safe_count(pods))

        st.metric("S3 Buckets", safe_count(buckets))
