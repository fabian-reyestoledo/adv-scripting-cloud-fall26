import boto3

iam_client = boto3.client('iam')
lambda_client = boto3.client('lambda')


def Create_Lambda(function_name):
    role_response = iam_client.get_role(RoleName='LabRole')

    with open('lambda_stop_function.zip', 'rb') as zipped_file:
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
        Handler='lambda_stop_function.lambda_handler'
    )

    waiter = lambda_client.get_waiter('function_active_v2')
    waiter.wait(FunctionName=function_name)

def Invoke_Lambda(function_name):
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse'
    )

    payload = response['Payload'].read()
    print(payload.decode('utf-8'))

def main():
    function_name = 'lambda_stop_ec2'

    try:
        lambda_client.get_function(FunctionName=function_name)
        print(f"Lambda function {function_name} already exists.")

    except lambda_client.exceptions.ResourceNotFoundException:
        print(f"Lambda function {function_name} does not exist.")
        Create_Lambda(function_name)

    Invoke_Lambda(function_name)

if __name__ == "__main__":
    main()