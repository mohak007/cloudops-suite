import pandas as pd
import streamlit as st

from utils.api_client import get, post, delete


def s3_page():

    st.header("S3 Management")

    operation = st.selectbox(
        "Operation",
        [
            "Create Bucket",
            "List Buckets",
            "Upload File",
            "List Objects",
            "Delete Object",
        ],
    )

    if operation == "Create Bucket":

        bucket_name = st.text_input("Bucket Name")

        if st.button("Create Bucket"):

            with st.spinner("Creating bucket..."):

                response = post("/s3/create-bucket", {"bucket_name": bucket_name})

            if "error" in response:

                st.error(response["error"])

            else:

                st.success(response["message"])

                st.json(response)

    elif operation == "List Buckets":

        if st.button("Fetch Buckets"):

            response = get("/s3/list-buckets")

            if isinstance(response, list):

                st.dataframe(pd.DataFrame(response), use_container_width=True)

            else:

                st.error(response)

    elif operation == "Upload File":

        bucket_name = st.text_input("Bucket Name")

        uploaded_file = st.file_uploader("Choose File")

        if uploaded_file and st.button("Upload File"):

            with st.spinner("Uploading file..."):

                response = post(
                    f"/s3/upload-file/{bucket_name}", files={"file": uploaded_file}
                )

            if "error" in response:

                st.error(response["error"])

            else:

                st.success(response["message"])

    elif operation == "List Objects":

        bucket_name = st.text_input("Bucket Name")

        if st.button("Fetch Objects"):

            response = get(f"/s3/list-objects/{bucket_name}")

            if isinstance(response, list):

                st.dataframe(pd.DataFrame(response), use_container_width=True)

            else:

                st.error(response)

    elif operation == "Delete Object":

        bucket_name = st.text_input("Bucket Name")

        object_key = st.text_input("Object Key")

        if st.button("Delete Object"):

            response = delete(f"/s3/delete-object/{bucket_name}/{object_key}")

            if "error" in response:

                st.error(response["error"])

            else:

                st.success(response["message"])
