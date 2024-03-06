## AWS Lambda Function Starter Template


### AWS SAM local setup

- Install sam-cli - [Details](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Install docker (*required only to test functions locally*)

#### Test application locally

##### Step1: Build

```
sam build -t sam/templates/template.yaml
```

##### Step2: Invoke
A lambda can be invoked locally using various event types. These events can be stored as json in a file. 
More details on generating events for local testing - [Details](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/using-sam-cli-local-generate-event.html)
##### SQS
```commandline
sam local invoke <lambda function resource name from template.yaml> -e sam/events/<filename>.json
```
example
```commandline
sam local invoke SqsLambda -e sam/events/sqs.json
```

##### API
```
sam local start-api
```
It will start a localhost server on port 3000. To use different port use below command
```
sam local start-api -p 8000
```
#### Deployment
We can use SAM to deploy the lambda functions and create resources automatically - [Details](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-deploy.html)

Example
```
sam deploy --config-file sam/samconfig.toml --config-env dev
```

##### AWS Permissions
We need below roles with required permission in order to run SAM template.
###### Role for execute SAM deploy command
- S3 Access
- Cloudformation Access
- iam:PassRole
Sample IAM Policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Action": [
                "iam:PassRole"
            ],
            "Resource": [
                "arn:aws:iam::1234567890:role/cloudformation-role"
            ]
        }
    ]
}
```

###### Role for cloudformation to create resources mentioned in SAM template
Add required permissions according to the resources added in the SAM template file.

#### Invoke Lambda
Lambda can be invoked in multiple ways. Following are few
- SQS
- function Url 
- API Gateway
- AWS SKD eg. boto3

Invoke lambda without any external event trigger using boto3 - [Details](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/invoke.html)

Example code
```python
import json
import boto3

# Create a Boto3 Lambda client
lambda_client = boto3.client('lambda')

# payload is optional
payload = {
    "key": "value"
}


# Invoke the Lambda function
# InvocationType="Event" -> just invoke
# InvocationType="RequestResponse" -> invoke and get function response
response = lambda_client.invoke(
    FunctionName="function_url_lambda",
    InvocationType="Event",
    Payload=json.dumps(payload)
)

print(response)

# if InvocationType is RequestResponse
response_data = response['Payload'].read()
print(json.loads(response_data))

```

