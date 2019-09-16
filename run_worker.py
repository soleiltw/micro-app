import json

import logging
import time
from json import JSONDecodeError

import boto3
from bottle import default_app

from app.app import init_app
from app.worker import actions

app = default_app()


def parse_message(raw_message):
    receipt_handle = raw_message['ReceiptHandle']

    body_json = json.loads(raw_message['Body'])

    if body_json.get('Type') == 'Notification':
        msg_id = body_json['MessageId']
        message = body_json['Message']
    else:
        msg_id = raw_message['MessageId']
        message = body_json

    return receipt_handle, msg_id, message


def loop():
    client = boto3.client('sqs')

    while True:
        query_url = app.config['aws.sqs.queue_url']
        wait_time_seconds = int(app.config['aws.sqs.wait_time_seconds'])

        resp = client.receive_message(
            QueueUrl=query_url,
            WaitTimeSeconds=wait_time_seconds)
        for raw_message in resp.get('Messages', []):
            receipt_handle, msg_id, message = parse_message(raw_message)

            if isinstance(message, str):
                try:
                    message = json.loads(message)
                except JSONDecodeError:
                    logging.info('invalid json: %s', message)
                    delete_message(client, query_url, receipt_handle)
                    continue

            message_action = message.get('action', '').lower()
            message_payload = message.get('payload', {})

            action_funcs = actions.get(message_action, [])

            for action_func in action_funcs:
                logging.info('aws sqs message receive: %s %s', msg_id, message)

                wk = None
                start = time.time()
                if message_action:
                    wk = worker_create(msg_id, message_action, message_payload)

                try:
                    action_func(message_payload, msg_id)
                    logging.info('message process done: %s func: %s',
                                 msg_id, action_func.__name__)
                    if wk:
                        worker_done(wk, start)
                except:  # noqa
                    logging.exception('message process failed: %s func: %s',
                                      msg_id, action_func.__name__)
                    if wk:
                        worker_failed(wk, start)
                    break
                finally:
                    # if not db.is_closed():
                    #     db.close()
                    pass
            else:
                delete_message(client, query_url, receipt_handle)


def worker_create(msg_id, message_action, message_payload):
    if not (msg_id and message_action):
        return
    # WorkerLog.create(message_id=msg_id, action=message_action,
    #                  payload=json.dumps(message_payload))
    # wk = (WorkerLog
    #       .filter(WorkerLog.message_id == msg_id)
    #       .order_by(WorkerLog.id.desc())
    #       .first())
    # return wk
    pass


def worker_failed(wk, start):
    # wk.time_spent = diff_end_time(start)
    # wk.result = WorkerResult.FAILED.value
    # wk.save()
    pass


def worker_done(wk, start):
    # wk.time_spent = diff_end_time(start)
    # wk.result = WorkerResult.DONE.value
    # wk.save()
    pass


def delete_message(client, query_url, receipt_handle):
    delete_resp = client.delete_message(
        QueueUrl=query_url,
        ReceiptHandle=receipt_handle,
    )
    logging.info('delete sqs msg %s resp: %s', receipt_handle, delete_resp)


if __name__ == '__main__':
    init_app()
    loop()
