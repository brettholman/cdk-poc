import config
import boto3


def handler(event, context) -> dict:
    response = {'code': 200}
    try:
        __handle_queue(response)
    except:
        response['code'] = 500
    return response


def __handle_queue(response) -> None:
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
