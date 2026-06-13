from tests.conftest import client


def test_list_containers():

    response = client.get(
        "/docker/list-containers"
    )

    assert response.status_code == 200


def test_list_images():

    response = client.get(
        "/docker/list-images"
    )

    assert response.status_code == 200
