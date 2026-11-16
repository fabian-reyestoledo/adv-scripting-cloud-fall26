
import boto3
from botocore.exceptions import ClientError, BotoCoreError

# Create an EC2 client
ec2_client = boto3.client("ec2")


# Function to stop tagged C2 instances
def Stop_EC2():
    try:
        response = ec2_client.describe_instances(
            Filters=[
                {
                    'Name': 'tag:env',
                    'Values': ['dev']
                }
            ]
        )

        instance_ids = []

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_ids.append(instance['InstanceId'])

        if instance_ids:
            print(f"Stopping instances: {instance_ids}")
            ec2_client.stop_instances(InstanceIds=instance_ids)
        else:
            print("No EC2 instances found with env=dev")

    except Exception as e:
        print(f"Error stopping EC2 instances: {e}")


# Function to start all EC2 instances
def Start_EC2():

    instance_ids = []

    try:
        # Get all instances
        response = ec2_client.describe_instances()

        # Loop through reservations and instances
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:

                instance_id = instance["InstanceId"]
                instance_ids.append(instance_id)

                print(f"Found instance: {instance_id}")

        # Start all instances
        if instance_ids:
            ec2_client.start_instances(InstanceIds=instance_ids)
            print("All EC2 instances are starting.")

        else:
            print("No EC2 instances found.")

    except ClientError as e:
        print(f"AWS Client Error: {e}")

    except BotoCoreError as e:
        print(f"Boto3 Error: {e}")


# Main function
def main():

    print("Stopping EC2 instances...")
    Stop_EC2()

    #print("\nStarting EC2 instances...")
    #Start_EC2()


# Execute main function
if __name__ == "__main__":
    main()
