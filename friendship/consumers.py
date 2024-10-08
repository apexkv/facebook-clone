import json
import os
import pika
from dotenv import load_dotenv
from time import sleep
import django


load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "friendship.settings")
django.setup()


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


channel.basic_consume(queue=CURRENT_QUEUE, on_message_callback=callback, auto_ack=True)

print("[FRIENDSHIP] Started consuming...")
channel.start_consuming()
channel.close()
