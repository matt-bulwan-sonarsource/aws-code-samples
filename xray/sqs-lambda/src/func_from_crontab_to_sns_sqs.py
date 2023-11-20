# HEADER

import boto3
import os
import random
import logging
from aws_lambda_powertools import Logger
import json
logger = Logger()
send_to = os.environ.get("EVENT_TARGET", "sns")
sns_topic = os.environ.get("SNS_TOPIC", "Unavailable")
sqs_queue = os.environ.get("SQS_QUEUE", "Unavailable")
bridge = os.environ.get("EVENT_BRIDGE", "Unavailable")
logger.setLevel(logging.INFO)

def publish_to_sns(event: dict[str:any]) -> None:
    client = boto3.client("sns")
    logger.info(f"About to post to SNS {sns_topic}")
    response = client.publish(
        TopicArn=sns_topic,
        Message=event.get("my_tracking_id"),
        Subject=event.get("my_tracking_id"),
    )
    logger.info(f"response from sns {response}")


def send_to_sqs(event: dict[str:any]) -> None:
    client = boto3.client("sqs")
    logger.info(f"About to send to SQS {sqs_queue}")
    response = client.send_message(
        QueueUrl=sqs_queue, MessageBody=event.get("my_tracking_id")
    )
    logger.info(f"response from sqs {response}")


def publish_to_bridge(event: dict[str:any]) -> None:
    client = boto3.client("events")
    logger.info(f"About to send to EventBridge")
    response = client.put_events(
        Entries=[
            {
                "Source": "publish_to_bridge",
                "DetailType": "publish_to_bridge",
                "Detail": json.dumps({"calling_function":"publish_to_bridge"}),
                "TraceHeader": os.environ.get("_X_AMZN_TRACE_ID"),
            },
        ]
    )

    logger.info(f"response from EventBridge {response}")


def end_of_the_road(event: dict[str:any]) -> None:
    logger.info(f"No handler implemented")


def handler(event: dict[str:any], context: dict[str:any]):
    send_to = os.environ.get("EVENT_TARGET", "Unknown")
    logger.append_keys(send_to=send_to)
    logger.info(event)
    logger.info(
        f"os.environ.get('_X_AMZN_TRACE_ID')={os.environ.get('_X_AMZN_TRACE_ID')}"
    )
    if not "my_tracking_id" in event:
        event["my_tracking_id"] = f"id-{random.randint(0,9999999)}"
    callable = {
        "sqs": send_to_sqs,
        "sns": publish_to_sns,
        "bridge": publish_to_bridge,
    }.get(send_to, end_of_the_road)
    callable(event)
