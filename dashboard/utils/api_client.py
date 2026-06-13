import requests

BASE_URL = "http://127.0.0.1:8000"


def get(endpoint: str):

    response = requests.get(
        f"{BASE_URL}{endpoint}"
    )

    return response.json()


def post(
        endpoint: str,
        data=None
):

    response = requests.post(
        f"{BASE_URL}{endpoint}",
        json=data
    )

    return response.json()


def delete(endpoint: str):

    response = requests.delete(
        f"{BASE_URL}{endpoint}"
    )

    return response.json()
