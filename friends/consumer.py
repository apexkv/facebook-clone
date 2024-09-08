import json
import os
import pika
from dotenv import load_dotenv
from time import sleep
import django


load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "posts.settings")
django.setup()


CURRENT_QUEUE = "posts"

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
    data = json.loads(body)
    print("--------------------------------")
    print("[POSTS] Event Received")
    print(properties.content_type)
    print(data)
    print("--------------------------------")

    action_type = properties.content_type

    # if action_type == "user.created":
    #     user = User(
    #         user_id=data["id"],
    #         full_name=data["full_name"],
    #         profile_pic=data["profile_pic"],
    #     )
    #     user.save()


channel.basic_consume(queue=CURRENT_QUEUE, on_message_callback=callback, auto_ack=True)

print("[POSTS] Started consuming")
channel.start_consuming()
channel.close()
