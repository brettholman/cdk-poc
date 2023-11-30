#!/bin/bash

## Bootstraps the project with expected depdencies for the health check endpoint to read/manipulate

source .venv/bin/activate

command -v cdk >/dev/null 2>&1 || { echo >&2 "cdk required to continue, please install and retry..."; exit 1; }
command -v aws >/dev/null 2>&1 || { echo >&2 "aws required to continue, please install and retry..."; exit 1; }

read -p "Do you want to deploy the stack? (yes/no) " yn

result=0

case $yn in
    yes) echo "deploying cdk...";
        result=$(cdk deploy)
        ;;
    *) echo "response not \"yes\", assuming you meant \"no\"";
        ;;
esac

if $result; then
    echo "Unable to delpoy stack. Exiting..."
    exit 1;
fi

echo "adding dependencies..."

echo "putting dynamo item"

aws dynamodb put-item --table-name dev-us-west-2-102797817500-healthCheckTable --item "{\"pk\": {\"S\": \"HealthCheck\"}, \"column1\": {\"S\": \"Health Check Item\"}}"

echo invoking the health check lambda... 🤞

aws lambda invoke --function-name healthCheckLambda out.json >> /dev/null

cat out.json | jq .
rm out.json
