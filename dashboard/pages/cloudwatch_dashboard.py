import streamlit as st

from utils.api_client import get


def cloudwatch_page():

    st.header(
        "CloudWatch Metrics"
    )

    instance_id = st.text_input(
        "Instance ID"
    )

    operation = st.selectbox(
        "Metric",
        [
            "CPU Utilization",
            "Network In",
            "Network Out",
            "Disk Read Bytes",
            "Disk Write Bytes"
        ]
    )

    if st.button(
        "Fetch Metric"
    ):

        metric_map = {

            "CPU Utilization":
            f"/cloudwatch/cpu-utilization/{instance_id}",

            "Network In":
            f"/cloudwatch/network-in/{instance_id}",

            "Network Out":
            f"/cloudwatch/network-out/{instance_id}",

            "Disk Read Bytes":
            f"/cloudwatch/disk-read/{instance_id}",

            "Disk Write Bytes":
            f"/cloudwatch/disk-write/{instance_id}"
        }

        response = get(
            metric_map[
                operation
            ]
        )

        st.json(
            response
        )
