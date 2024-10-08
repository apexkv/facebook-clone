import pika

import os
import pika
import json
from dotenv import load_dotenv
from time import sleep
from django.utils import timezone
import django
import logging


load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "postwrite.settings")
django.setup()


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


CURRENT_QUEUE = "friendship"

rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER")
rabbitmq_pass = os.getenv("RABBITMQ_DEFAULT_PASS")
rabbitmq_host = os.getenv("RABBITMQ_HOST")


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

channel.queue_declare(queue=CURRENT_QUEUE)


def callback(chnl, method, properties, body):
    data = json.loads(body)
    action_type = properties.content_type
    ConsumeHandler(action_type, data)


channel.basic_consume(queue=CURRENT_QUEUE, on_message_callback=callback, auto_ack=True)

print("[FRIENDSHIP] Started consuming...")
channel.start_consuming()
channel.close()


class ConsumeHandler:
    def __init__(self, action_type: str, data: dict):
        self.handle(action_type, data)

    def handle(self, action_type: str, data: dict):
        method_name = action_type.replace(".", "_")
        method = getattr(self, method_name, None)

        if callable(method):
            method(json.loads(data))
        else:
            msg = f"New action detected. Cannot find handling method for,\nAction: {action_type}"
            warning(msg)
