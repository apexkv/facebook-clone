import os
from typing import Literal
import pika
import json
from dotenv import load_dotenv
from time import sleep

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "posts.settings")

rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER")
rabbitmq_pass = os.getenv("RABBITMQ_DEFAULT_PASS")


if not rabbitmq_user or not rabbitmq_pass:
    raise ValueError(
        "RabbitMQ credentials are not set properly in the environment variables."
    )

# Set up RabbitMQ connection
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)


def connect_to_rabbitmq():
    connection = None
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters("rabbitmq", credentials=credentials)
            )
            break
        except Exception as e:
            print(f"Failed to connect to RabbitMQ: {e}")
        sleep(1)

    return connection


connection = connect_to_rabbitmq()
channel = connection.channel()
channel = connection.channel()

TO_USERS = "users"

TO = Literal["users"]


def publish(method, body, to: TO):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="",
        routing_key=to,
        body=json.dumps(body),
        properties=properties,
    )
