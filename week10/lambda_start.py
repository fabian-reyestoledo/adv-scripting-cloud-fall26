
import boto3
from botocore.exceptions import ClientError, BotoCoreError

iam_client = boto3.client('iam')
lambda_client = boto3.client('lambda')


# Function to create Lambda
def Create_Lambda(function_name):

    try:
        role_response = iam_client.get_role(
            RoleName='LabRole'
        )

        with open('lambda_start_function.zip', 'rb') as zipped_file:
            zipped_code = zipped_file.read()

        response = lambda_client.create_function(
            FunctionName=function_name,
            Timeout=15,
            Role=role_response['Role']['Arn'],
            Publish=True,
            PackageType='Zip',
            Runtime='python3.9',
            Code={
                'ZipFile': zipped_code
            },
            Handler='lambda_start_function.lambda_handler'
        )

        waiter = lambda_client.get_waiter('function_active_v2')
        waiter.wait(FunctionName=function_name)

        print(f"Lambda function {function_name} created successfully.")

    except (ClientError, BotoCoreError) as e:
        print(f"Error creating Lambda function: {e}")
        raise


# Function to invoke Lambda
def Invoke_Lambda(function_name):

    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse'
        )

        payload = response['Payload'].read()
        print(payload.decode('utf-8'))

    except (ClientError, BotoCoreError) as e:
        print(f"Error invoking Lambda: {e}")
        raise


# Main function
def main():

    function_name = 'lambda_start_ec2'

    try:
        lambda_client.get_function(
            FunctionName=function_name
        )

        print(f"Lambda function {function_name} already exists.")

    except lambda_client.exceptions.ResourceNotFoundException:

        print(f"Lambda function {function_name} does not exist.")

        Create_Lambda(function_name)

    Invoke_Lambda(function_name)


# Execute main function
if __name__ == "__main__":
    main()
