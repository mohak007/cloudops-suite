from datetime import datetime, timedelta

from app.config.aws_config import cloudwatch_client
from app.utils.logger import logger


def get_metric(instance_id: str, metric_name: str):

    try:

        end_time = datetime.utcnow()

        start_time = end_time - timedelta(minutes=30)

        response = cloudwatch_client.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName=metric_name,
            Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["Average"],
        )

        datapoints = response["Datapoints"]

        if not datapoints:

            return {"message": f"No {metric_name} metrics available"}

        latest_datapoint = sorted(datapoints, key=lambda x: x["Timestamp"])[-1]

        return {
            "instance_id": instance_id,
            "metric_name": metric_name,
            "average_value": round(latest_datapoint["Average"], 2),
            "unit": latest_datapoint["Unit"],
        }

    except Exception as error:

        logger.error(str(error))

        return {"error": str(error)}


def get_ec2_cpu_utilization(instance_id: str):

    return get_metric(instance_id, "CPUUtilization")


def get_network_in(instance_id: str):

    return get_metric(instance_id, "NetworkIn")


def get_network_out(instance_id: str):

    return get_metric(instance_id, "NetworkOut")


def get_disk_read_bytes(instance_id: str):

    return get_metric(instance_id, "DiskReadBytes")


def get_disk_write_bytes(instance_id: str):

    return get_metric(instance_id, "DiskWriteBytes")
