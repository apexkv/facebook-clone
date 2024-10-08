import pika

import os
from typing import List
import pika
import json
from dotenv import load_dotenv
from time import sleep
import django

load_dotenv()
django.setup()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "postwrite.settings")

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


def publish(action, body, to: List[str]):
    properties = pika.BasicProperties(action)
    for queue in to:
        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(body),
            properties=properties,
        )
