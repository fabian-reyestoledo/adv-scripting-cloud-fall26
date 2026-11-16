
import json
import boto3
from botocore.exceptions import ClientError, BotoCoreError

# Create an EC2 client
ec2_client = boto3.client('ec2')


# Function to start tagged EC2 instances
def Start_EC2():

    instance_ids = []

    try:
        # Get stopped instances tagged env=dev
        response = ec2_client.describe_instances(
            Filters=[
                {
                    'Name': 'tag:env',
                    'Values': ['dev']
                },
                {
                    'Name': 'instance-state-name',
                    'Values': ['stopped']
                }
            ]
        )

        # Loop through reservations and instances
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:

                instance_id = instance['InstanceId']
                instance_ids.append(instance_id)

                print(f"Found instance: {instance_id}")

        # Start instances
        if instance_ids:

            print(f"Starting instances: {instance_ids}")

            ec2_client.start_instances(
                InstanceIds=instance_ids
            )

            print("All tagged EC2 instances are starting.")

        else:
            print("No stopped EC2 instances found with env=dev")

        return instance_ids

    except ClientError as e:
        print(f"AWS Client Error: {e}")
        raise

    except BotoCoreError as e:
        print(f"Boto3 Error: {e}")
        raise


# Lambda handler function
def lambda_handler(event, context):

    started_instances = Start_EC2()

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'EC2 instances are starting.',
            'started_instances': started_instances
        })
    }
