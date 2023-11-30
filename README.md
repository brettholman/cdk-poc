# Python AWS CDK POC

The goal of this repository is to spin up a cloud formation stack with AWS CDK which handles generating various AWS resources as well as the IAM roles necessary to provide a secure application all written in python. Ultimately this application will have one "health check" lambda which will establish a connection with all of the provisioned resources. The heath checks will be more of a check to ensure a message can be written to a queue, a notification can be published, or an item can be read from a dynamo table not the more traditional connection health check (looking for 200 status code within BOTO when spinning up clients)

Resources:

- ~~SQS~~
- ~~SNS~~
- ~~Dynamo~~
- S3
- Lambda (lambda to lambda connection)

Stretch Goals:

- API Gateway (public api to be able to cURL health check lamdba)
- Simple Hello World Step Function with multiple lambdas
