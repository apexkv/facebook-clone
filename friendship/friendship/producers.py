import pika

import os
from typing import List, Literal
import pika
import json
from dotenv import load_dotenv
from time import sleep
from django.utils import timezone
import django
import logging

load_dotenv()
django.setup()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "users.settings")

rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER")
rabbitmq_pass = os.getenv("RABBITMQ_DEFAULT_PASS")
rabbitmq_host = os.getenv("RABBITMQ_HOST")

logger = logging.getLogger(__name__)


def info(msg):
    timestamp = timezone.now()
    details = f"[{timestamp.day:02d}/{timestamp.month:02d}/{timestamp.year} {timestamp.hour:02d}:{timestamp.minute:02d}:{timestamp.second:02d}] {msg}"
    logger.info(details)
    print(details)


def warning(msg):
    timestamp = timezone.now()
    details = f"[{timestamp.day:02d}/{timestamp.month:02d}/{timestamp.year} {timestamp.hour:02d}:{timestamp.minute:02d}:{timestamp.second:02d}] {msg}"
    logger.warning(details)


def error(msg):
    timestamp = timezone.now()
    details = f"[{timestamp.day:02d}/{timestamp.month:02d}/{timestamp.year} {timestamp.hour:02d}:{timestamp.minute:02d}:{timestamp.second:02d}] {msg}"
    logger.error(details)


if not rabbitmq_user or not rabbitmq_pass:
    raise ValueError(
        "RabbitMQ credentials are not set properly in the environment variables."
    )


credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)


def connect_to_rabbitmq():
    connection = None
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(rabbitmq_host, credentials=credentials)
            )
            break
        except Exception as e:
            print(f"Failed to connect to RabbitMQ: {e}")
        sleep(1)

    return connection


connection = connect_to_rabbitmq()
channel = connection.channel()

QUEUE_LIST = os.getenv("QUEUE_LIST").split(",")


def publish(method, body, to: List[str] | Literal["broadcast"]):
    properties = pika.BasicProperties(method)
    to = QUEUE_LIST if to == "broadcast" else to
    for publish_to in to:
        try:
            channel.basic_publish(
                exchange="",
                routing_key=publish_to,
                body=json.dumps(body),
                properties=properties,
            )
            info(f'"PUBLISHED - QUEUE: {publish_to} | ACTION: {method}"')
        except Exception as e:
            error(f"Failed to publish to {publish_to}")
