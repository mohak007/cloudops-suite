from unittest.mock import patch

from tests.conftest import client


@patch("app.services.ec2_service.ec2_client")
def test_list_instances(mock_ec2):
    mock_ec2.describe_instances.return_value = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-123",
                        "InstanceType": "t2.micro",
                        "State": {"Name": "running"},
                        "PublicIpAddress": "1.2.3.4",
                    }
                ]
            }
        ]
    }

    response = client.get("/ec2/list-instances")

    assert response.status_code == 200
