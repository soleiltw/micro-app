import json
from enum import Enum

import boto3
import logging
from bottle import default_app

app = default_app()


class MessageAction(Enum):
    HEALTH_CHECK = 'HEALTH_CHECK'


def send_to_bus(action, payload):
    arn = app.config['aws.sns.arn_bus']
    if arn == '__placeholder__':
        return
    return send_to_sns(arn, action, payload)


def send_to_sns(arn, action, payload):
    assert isinstance(action, MessageAction)

    client = boto3.client('sns')

    message = json.dumps({
        'action': action.value,
        'payload': payload,
    })
    logging.info('sns message body: %s', message)

    response = client.publish(
        TopicArn=arn,
        Message=message,
    )

    msg_id = response['MessageId']
    logging.info('sns message id: %s', msg_id)
    return msg_id


def send_to_default_q(action, payload):
    url = app.config['aws.sqs.queue_url']
    if '__placeholder__' == url:
        return
    return send_to_sqs(url, action, payload)


def send_to_long_q(action, payload):
    url = app.config['aws.sqs.queue_long_url']
    if '__placeholder__' == url:
        return
    return send_to_sqs(url, action, payload)


def send_to_sqs(url, action, payload):
    assert isinstance(action, MessageAction)

    client = boto3.client('sqs')

    message = json.dumps({
        'action': action.value,
        'payload': payload,
    })
    logging.info('send sqs message body: %s', message)

    response = client.send_message(
        QueueUrl=url,
        MessageBody=message,
    )

    msg_id = response
    logging.info('sqs message id: %s', response['MessageId'])
    return msg_id
