import json
import boto3
from botocore.exceptions import ClientError, BotoCoreError

ec2_client = boto3.client('ec2')

def Stop_EC2():

    instance_ids = []

    try:
        # Get tagged instances
        response = ec2_client.describe_instances(
            Filters=[
                {
                    'Name': 'tag:env',
                    'Values': ['dev']
                }
            ]
        )
        # Loop through reservations and instances
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:

                instance_id = instance["InstanceId"]
                instance_ids.append(instance_id)

                print(f"Found instance: {instance_id}")

        # Stop all instances
        if instance_ids:
            print(f"Stopping instances: {instance_ids}")
            ec2_client.stop_instances(InstanceIds=instance_ids)
            print("All tagged EC2 instances are stopping.")

        else:
            print("No EC2 instances found.")

        return instance_ids

    except ClientError as e:
        print(f"AWS Client Error: {e}")
        raise

    except BotoCoreError as e:
        print(f"Boto3 Error: {e}")
        raise


def lambda_handler(event, context):

    stopped_instances = Stop_EC2()

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'EC2 instances are stopping.',
            'stopped_instances': stopped_instances
        })
    }