import config
import boto3


def handler(event, context) -> dict:
    response = {'code': 200}
    try:
        __handle_sqs(response)
        __handle_sns(response)
        __handle_dynamo(response)
        __handle_s3(response)
        __handle_lambda(response)
    except:
        response['code'] = 500
    return response


def __handle_sqs(response) -> None:
    try:
        response['sqs'] = {}
        sqs_client = boto3.client('sqs')

        message = sqs_client.send_message(
            QueueUrl=config.dev.healthCheck_queue_url,
            DelaySeconds=.25,
            MessageAttributes={
                'body': "I came from the health check lambda"
            },
            MessageBody="This is a test!"
        )

        if "messageId" in message:
            response['sqs'] = {
                "body": "message sent!",
                "status": "healthy"
            }

    except Exception as e:
        response['sqs'] = {
            'message': "unable to send sqs message",
            "reason": str(e)
        }
        raise e


def __handle_sns(response) -> None:
    pass


def __handle_dynamo(response) -> None:
    pass


def __handle_s3(response) -> None:
    pass


def __handle_lambda(response) -> None:
    pass
