import pandas as pd
import streamlit as st

from utils.api_client import get, post, delete


def k8s_page():

    st.header(
        "Kubernetes Management"
    )

    operation = st.selectbox(
        "Operation",
        [
            "List Pods",
            "List Services",
            "Create Namespace",
            "Create Deployment",
            "Scale Deployment",
            "Delete Deployment"
        ]
    )

    if operation == "List Pods":

        if st.button(
            "Fetch Pods"
        ):

            response = get(
                "/k8s/pods"
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

    elif operation == "List Services":

        if st.button(
            "Fetch Services"
        ):

            response = get(
                "/k8s/services"
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

    elif operation == "Create Namespace":

        namespace = st.text_input(
            "Namespace"
        )

        if st.button(
            "Create Namespace"
        ):

            with st.spinner(
                "Creating namespace..."
            ):

                response = post(
                    f"/k8s/create-namespace/{namespace}"
                )

            if "error" in response:

                st.error(
                    response["error"]
                )

            else:

                st.success(
                    response["message"]
                )

    elif operation == "Scale Deployment":

        deployment_name = st.text_input(
            "Deployment Name"
        )

        replicas = st.number_input(
            "Replicas",
            value=1
        )

        if st.button(
            "Scale Deployment"
        ):

            response = post(
                f"/k8s/scale-deployment/{deployment_name}/{replicas}"
            )

            if "error" in response:

                st.error(
                    response["error"]
                )

            else:

                st.success(
                    response["message"]
                )

    elif operation == "Delete Deployment":

        deployment_name = st.text_input(
            "Deployment Name"
        )

        if st.button(
            "Delete Deployment"
        ):

            response = delete(
                f"/k8s/delete-deployment/{deployment_name}"
            )

            if "error" in response:

                st.error(
                    response["error"]
                )

            else:

                st.success(
                    response["message"]
                )
