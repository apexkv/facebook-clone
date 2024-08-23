import os
import pika
from dotenv import load_dotenv
from time import sleep

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "users.settings")

CURRENT_QUEUE = "users"

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

channel.queue_declare(queue=CURRENT_QUEUE)


def callback(chnl, method, properties, body):
    print("[USERS] Received")
    print(body)


channel.basic_consume(queue=CURRENT_QUEUE, on_message_callback=callback, auto_ack=True)

print("[USERS] Started consuming")
channel.start_consuming()
channel.close()
