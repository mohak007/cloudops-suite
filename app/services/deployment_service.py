import paramiko

from app.utils.logger import logger


def deploy_container_to_ec2(host, username, pem_file):

    try:

        logger.info(f"Connecting to EC2: {host}")

        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname=host, username=username, key_filename=pem_file)

        logger.info("SSH connection established")

        commands = ["docker pull nginx", "docker run -d -p 80:80 nginx"]

        for command in commands:

            logger.info(f"Executing command: {command}")

            stdin, stdout, stderr = ssh.exec_command(command)

            output = stdout.read().decode()

            error = stderr.read().decode()

            logger.info(f"Output: {output}")

            if error:

                logger.error(f"Error: {error}")

        ssh.close()

        logger.info("Deployment completed successfully")

        return {"message": "Container deployed successfully"}

    except Exception as error:

        logger.error(f"Deployment failed: {str(error)}")

        return {"error": str(error)}
