import json
import config
import boto3


def handler(event, context):
    response = {'code': 200}
    try:
        __handle_queue(response)
    except:
        response.code = 500
    return response


def __handle_queue(response) -> None:

    try:
        response['sqs'] = {}
        sqs_client = boto3.client('sqs')

    except Exception as e:
        response['sqs'] = {
            'message': "unable to send sqs message",
            "reason": e
        }
        raise e
