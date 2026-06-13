from unittest.mock import patch

from tests.conftest import client

@patch("app.services.cloudwatch_service.cloudwatch_client")
def test_cpu_utilization(mock_cloudwatch):
    mock_cloudwatch.get_metric_statistics.return_value = {
        "Datapoints": [
        {
            "Average": 35,
            "Unit": "Percent"
        }
    ]
}

    response = client.get(
    "/cloudwatch/ec2-cpu/i-123"
)

    assert response.status_code == 200
