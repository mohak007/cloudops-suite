import streamlit as st

from utils.api_client import get, post, delete


def docker_page():

    st.header("Docker Management")

    operation = st.selectbox(
        "Operation",
        [
            "Build Image",
            "Run Containers",
            "List Containers",
            "List Images",
            "Container Logs",
            "Start Container",
            "Stop Container",
            "Remove Container",
            "Remove Image",
        ],
    )

    if operation == "Build Image":

        if st.button("Build Docker Image"):

            st.json(post("/docker/build-image"))
    elif operation == "Run Containers":

        image_name = st.text_input("Image Name", value="nginx")

        container_name = st.text_input("Container Name", value="my-nginx")

        container_port = st.number_input("Container Port", value=80)

        host_port = st.number_input("Host Port", value=8080)

        if st.button("Run Container"):

            response = post(
                "/docker/run-container",
                {
                    "image_name": image_name,
                    "container_name": container_name,
                    "container_port": container_port,
                    "host_port": host_port,
                },
            )

            st.json(response)

    elif operation == "List Containers":

        if st.button("List Containers"):

            st.json(get("/docker/list-containers"))

    elif operation == "Container Logs":

        container_id = st.text_input("Container ID")

        if st.button("Get Logs"):

            st.json(get(f"/docker/container-logs/{container_id}"))

    elif operation == "Start Container":

        container_id = st.text_input("Container ID")

        if st.button("Start Container"):

            st.json(post(f"/docker/start-container/{container_id}"))
    elif operation == "Stop Container":

        container_id = st.text_input("Container ID")

        if st.button("Stop Container"):

            st.json(post(f"/docker/stop-container/{container_id}"))

    elif operation == "Remove Container":

        container_id = st.text_input("Container ID")

        if st.button("Remove Container"):

            st.json(delete(f"/docker/remove-container/{container_id}"))
    elif operation == "Remove Image":
        image_name = st.text_input("Image Name")
        if st.button("Remove Image"):
            response = delete(f"/docker/remove-image/{image_name}")

            st.json(response)
    elif operation == "List Images":

        if st.button("Fetch Image"):
            st.json(delete("/docker/list-images"))
