from unittest.mock import patch

from tests.conftest import client


@patch("app.services.s3_service.s3_client")
def test_list_buckets(mock_s3):

    mock_s3.list_buckets.return_value = {"Buckets": [{"Name": "cloudops-test"}]}

    response = client.get("/s3/list-buckets")

    assert response.status_code == 200
