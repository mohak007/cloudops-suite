import streamlit as st
import pandas as pd

from utils.api_client import get, post, delete


def ec2_page():

    st.header("EC2 Management")

    operation = st.selectbox(
        "Operation",
        [
            "Create Instances",
            "List Instances",
            "Start Instance",
            "Stop Instance",
            "Terminate Instance"
        ]
    )

    if operation == "Create Instances":

        instance_name = st.text_input(
            "Instance Name",
            value="dev-server"
        )

        instance_type = st.selectbox(
            "Instance Type",
            [
                "t2.micro",
                "t3.micro"
            ]
        )

        security_group_name = st.text_input(
            "Security Group Name",
            value="cloudops-sg"
        )

        key_pair_name = st.text_input(
            "Key Pair Name",
            value="cloudops-key"
        )

        ports = st.text_input(
            "Ports (comma separated)",
            value="22,80"
        )

        if st.button("Create Instance"):

            ports_list = [
                int(port.strip())
                for port in ports.split(",")
            ]

            with st.spinner(
                "Launching EC2 instance..."
            ):

                response = post(
                    "/ec2/create-instance",
                    {
                        "instance_name": instance_name,
                        "instance_type": instance_type,
                        "security_group_name": security_group_name,
                        "key_pair_name": key_pair_name,
                        "ports": ports_list
                    }
                )

            if "error" in response:

                st.error(
                    response["error"]
                )

            else:

                st.success(
                    response["message"]
                )

                st.json(
                    response
                )

    elif operation == "List Instances":

        if st.button("Fetch Instances"):

            response = get(
                "/ec2/list-instances"
            )

            if isinstance(
                response,
                list
            ):

                st.dataframe(
                    pd.DataFrame(
                        response
                    ),
                    use_container_width=True
                )

            else:

                st.error(
                    response
                )

    elif operation == "Start Instance":

        instance_id = st.text_input(
            "Instance ID"
        )

        if st.button("Start"):

            with st.spinner(
                "Starting instance..."
            ):

                response = get(
                    f"/ec2/start-instance/{instance_id}"
                )

            if "error" in response:

                st.error(
                    response["error"]
                )

            else:

                st.success(
                    response["message"]
                )

    elif operation == "Stop Instance":

        instance_id = st.text_input(
            "Instance ID"
        )

        if st.button("Stop"):

            with st.spinner(
                "Stopping instance..."
            ):

                response = get(
                    f"/ec2/stop-instance/{instance_id}"
                )

            if "error" in response:

                st.error(
                    response["error"]
                )

            else:

                st.success(
                    response["message"]
                )

    elif operation == "Terminate Instance":

        instance_id = st.text_input(
            "Instance ID"
        )

        if st.button("Terminate"):

            with st.spinner(
                "Terminating instance..."
            ):

                response = delete(
                    f"/ec2/terminate-instance/{instance_id}"
                )

            if "error" in response:

                st.error(
                    response["error"]
                )

            else:

                st.success(
                    response["message"]
                )

