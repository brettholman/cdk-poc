import config
import boto3


def handler(event, context) -> dict:
    response = {"code": 200}
    try:
        __handle_sqs(response)
        __handle_sns(response)
        __handle_dynamo(response)
        __handle_s3(response)
        __handle_lambda(response)
    except Exception as e:
        response["code"] = 500
        if "error" not in response:
            response["error"] = {
                "body": "unable to process",
                "reason": str(e)
            }
    return response


def __handle_sqs(response) -> None:
    response["sqs"] = {}
    try:
        sqs_client = boto3.client("sqs")

        message = sqs_client.send_message(
            QueueUrl=config.resources["health_check_queue_url"],
            DelaySeconds=1,
            MessageAttributes={
                "body": {
                    "DataType": "String",
                    "StringValue": "this is a test"
                }
            },
            MessageBody="This is a test!"
        )

        if "MessageId" in message:
            response["sqs"] = {
                "body": "message sent!",
                "status": "healthy"
            }
        else:
            raise RuntimeError(
                "No message identifier associated to attempted message")

    except Exception as e:
        response["sqs"] = {
            "message": "unable to send sqs message",
            "reason": str(e),
            "debug": config.resources["health_check_queue_url"]
        }


def __handle_sns(response) -> None:
    response["sns"] = {}
    try:
        sns_client = boto3.client("sns")

        notification_result = sns_client.publish(
            TopicArn=config.resources["health_check_sns_topic"],
            Message="This is a test!"
        )

        if "MessageId" in notification_result:
            response["sns"] = {
                "body": "Notification sent!",
                "status": "healthy"
            }
        else:
            raise RuntimeError(
                "No MessageId associated to attempted message")

    except Exception as e:
        response["sqs"] = {
            "message": "unable to send sns notification",
            "reason": str(e),
            "debug": config.resources["health_check_sns_topic"]
        }


def __handle_dynamo(response) -> None:
    response["dynamo"] = {}
    try:
        dynamo_client = boto3.client("dynamodb")

        item = dynamo_client.get_item(
            TableName=config.resources["health_check_dynamo_table"],
            Key={
                "pk": {
                    "S": "HealthCheck"
                }
            }
        )

        if "Item" in item:
            response["dynamo"] = {
                "message": "Found the item!",
                "status": "healthy",
                "item_details": item["Item"]["column1"]["S"]
            }
        else:
            raise LookupError("Unable to fetch item from dynamo")

    except Exception as e:
        response["dynamo"] = {
            "message": "unable to retrieve dynamo item",
            "reason": str(e),
            "debug": config.resources["health_check_dynamo_table"]
        }


def __handle_s3(response) -> None:
    response["s3"] = {}
    try:
        s3_client = boto3.client("s3")

        item = s3_client.get_object(
            Bucket=config.resources["health_check_s3_bucket"],
            Key="item.json"
        )
        if "Body" in item:
            response["s3"] = {
                "message": "Found the item!",
                "status": "healthy",
                "item_details": item["Body"].read()
            }
        else:
            raise LookupError("Unable to fetch item from s3")

    except Exception as e:
        response["s3"] = {
            "message": "Unable to retrieve s3 item",
            "reason": str(e),
            "debug": config.resources["health_check_s3_bucket"]
        }


def __handle_lambda(response) -> None:
    pass
