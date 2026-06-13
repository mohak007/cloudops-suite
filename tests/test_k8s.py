from tests.conftest import client


def test_list_pods():

    response = client.get(
        "/k8s/pods"
    )

    assert response.status_code == 200


def test_list_services():

    response = client.get(
        "/k8s/services"
    )

    assert response.status_code == 200

