from app.config.aws_config import ec2_client
from app.utils.logger import logger
from botocore.exceptions import ClientError
from app.models.ec2_models import EC2CreateRequest
from botocore.exceptions import ClientError
from app.config.settings import DEFAULT_AMI_ID
from app.config.settings import USER_DATA_SCRIPT
from app.exceptions.custom_exceptions import(AWSOperationException)

def create_ec2_instance(data: EC2CreateRequest):
    try:
        logger.info("Creating EC2 instance")
        security_group_id = create_security_group(
            data.security_group_name,
            data.ports
        )

        user_data_script = """..."""
        subnet_id = get_default_subnet()
        logger.info(f"Using security group: {security_group_id}")

        key_pair_name = create_key_pair(data.key_pair_name)
        response = ec2_client.run_instances(
            ImageId= DEFAULT_AMI_ID,
            MinCount=1,
            MaxCount=1,
            InstanceType=data.instance_type,
            SecurityGroupIds = [ security_group_id],
            SubnetId=subnet_id,
            KeyName=key_pair_name,
            UserData=user_data_script,
            TagSpecifications=[
                {
                    "ResourceType": "instance",
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": data.instance_name
                        }
                    ]
                }
            ]
        )

        instance_id = response["Instances"][0]["InstanceId"]

        logger.info(f"waiting for EC2 instance to enter"
                    f"running state{instance_id}")
        waiter = ec2_client.get_waiter('instance_running')

        instance_description = ec2_client.describe_instances(InstanceIds=[instance_id])

        instance = instance_description["Reservations"][0]["Instances"][0]

        public_ip = instance.get("PublicIpAddress")

        waiter.wait(InstanceIds=[instance_id])

        logger.info(f"Ec2 instance is now running: {instance_id}")

        return {
            "instance_id": instance_id,
            "state" : instance["State"]["Name"],
            "public_ip": public_ip,
            "message": "EC2 instance launched successfully"
        }

    except ClientError as error:
        logger.error(f"AWS ClientError occurred: {str(error)}")

        return {
            "error": str(error)
        }
        raise AWSOperationException(str(error))

    except Exception as error:
        logger.error(f"Unexpected error occurred: {str(error)}")

        return {
            "error": str(error)
        }


def list_ec2_instances():

    try:

        logger.info(
            "Fetching EC2 instances"
        )

        response = ec2_client.describe_instances()

        instances = []

        for reservation in response["Reservations"]:

            for instance in reservation["Instances"]:

                instances.append({
                    "instance_id":
                        instance.get("InstanceId"),

                    "instance_type":
                        instance.get("InstanceType"),

                    "state":
                        instance["State"]["Name"],

                    "public_ip":
                        instance.get(
                            "PublicIpAddress"
                        )
                })

        logger.info(
            f"Fetched {len(instances)} instances"
        )

        return instances

    except Exception as error:

        logger.error(
            f"Error fetching instances: "
            f"{str(error)}"
        )
        
        raise AWSOperationException(str(error))


        return {
            "error": str(error)
        }


def stop_ec2_instance(instance_id: str):
    try:

        ec2_client.stop_instances(
        InstanceIds=[instance_id]
        )

        logger.info(f"Stopped EC2 instance request submitted for {instance_id}")

        return {
        "message": f"Stopping instance {instance_id}"
        }
    except ClientError as error:
        logger.error(str(error))    
        raise AWSOperationException(str(error))

        return { "error" : str(error)}


def start_ec2_instance(instance_id: str):
    try:

        ec2_client.start_instances(
        InstanceIds=[instance_id]
        )

        logger.info(f"Start EC2 instance request submitted for {instance_id}")

        return {
        "message": f"Starting instance {instance_id}"
        }
    except ClientError as error:
        logger.error(str(error))   
        raise AWSOperationException(str(error)) 
        return { "error" : str(error)}


def terminate_ec2_instance(instance_id: str):

    try:

        logger.info(
            f"Terminating EC2 instance: {instance_id}"
        )

        response = ec2_client.terminate_instances(
            InstanceIds=[instance_id]
        )

        current_state = response[
            "TerminatingInstances"
        ][0]["CurrentState"]["Name"]

        logger.info(
            f"Terminate request submitted for "
            f"{instance_id}"
        )

        return {
            "instance_id": instance_id,
            "current_state": current_state,
            "message": "Termination initiated successfully"
        }

    except ClientError as error:

        logger.error(
            f"AWS ClientError while terminating "
            f"instance: {str(error)}"
        )
        raise AWSOperationException(str(error))

        return {
            "error": str(error)
        }

    except Exception as error:

        logger.error(
            f"Unexpected error while terminating "
            f"instance: {str(error)}"
        )

        return {
            "error": str(error)
        }

def create_security_group(group_name: str, ports: list):

    try:

        logger.info(
            f"Checking if security group exists: "
            f"{group_name}"
        )

        existing_groups = ec2_client.describe_security_groups(
            Filters=[
                {
                    'Name': 'group-name',
                    'Values': [group_name]
                }
            ]
        )

        # Reuse existing SG
        if existing_groups["SecurityGroups"]:

            security_group_id = existing_groups[
                "SecurityGroups"
            ][0]["GroupId"]

            logger.info(
                f"Using existing security group: "
                f"{security_group_id}"
            )

            return security_group_id

        # Create new SG
        logger.info(
            "Security group not found. Creating new one."
        )

        response = ec2_client.create_security_group(
            GroupName=group_name,
            Description="Security group for CloudOps Suite"
        )

        security_group_id = response["GroupId"]

        logger.info(
            f"Created security group: "
            f"{security_group_id}"
        )

        # Open SSH Port

        ip_permissions = []
        for port in ports:
            ip_permissions.append(
                {
                    'IpProtocol' : 'tcp',
                    'FromPort' : port,
                    'ToPort' : port,
                    'IpRanges' : [
                        {
                            'CidrIp' : '0.0.0.0/0'
                        }
                    ]
                }
            )

        
        ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=ip_permissions
            )

        logger.info(
            "SSH port 22 opened successfully"
        )

        return security_group_id

    except ClientError as error:

        logger.error(
            f"AWS ClientError while handling SG: "
            f"{str(error)}"
        )
        raise AWSOperationException(str(error))

        raise error

    except Exception as error:

        logger.error(
            f"Unexpected error while handling SG: "
            f"{str(error)}"
        )

        raise error


def get_default_subnet():

    response = ec2_client.describe_subnets()

    subnet_id = response["Subnets"][0]["SubnetId"]

    logger.info(f"Using subnet: {subnet_id}")

    return subnet_id

def create_key_pair(key_name: str):

    try:

        logger.info(
            f"Checking if key pair exists: {key_name}"
        )

        ec2_client.describe_key_pairs(
            KeyNames=[key_name]
        )

        logger.info(
            f"Using existing key pair: {key_name}"
        )

        return key_name

    except ClientError as error:

        if "InvalidKeyPair.NotFound" in str(error):

            logger.info(
                "Key pair not found. Creating new key pair."
            )

            response = ec2_client.create_key_pair(
                KeyName=key_name
            )

            private_key = response["KeyMaterial"]

            pem_file = f"{key_name}.pem"

            with open(pem_file, "w") as file:

                file.write(private_key)

            logger.info(
                f"Created key pair and saved PEM: "
                f"{pem_file}"
            )

            return key_name

        logger.error(
            f"Key pair error: {str(error)}"
        )
        raise AWSOperationException(str(error))

        raise error

    except Exception as error:

        logger.error(
            f"Unexpected key pair error: "
            f"{str(error)}"
        )

        raise error
