import pika

import os
import pika
import json
from dotenv import load_dotenv
from time import sleep
from django.utils import timezone
import django
import logging


"""
This script is responsible for consuming messages from the RabbitMQ queue.
"""


load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat.settings")
django.setup()

from base.models import User, Room

logger = logging.getLogger(__name__)


# Log the message and print it to the console
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


CURRENT_QUEUE = os.getenv("CURRENT_QUEUE")

rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER")
rabbitmq_pass = os.getenv("RABBITMQ_DEFAULT_PASS")
rabbitmq_host = os.getenv("RABBITMQ_HOST")


if not rabbitmq_user or not rabbitmq_pass:
    raise ValueError(
        "RabbitMQ credentials are not set properly in the environment variables."
    )


credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)


def connect_to_rabbitmq():
    # Connect to RabbitMQ server
    connection = None
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    rabbitmq_host, credentials=credentials, heartbeat=0
                )
            )
            break
        except Exception as e:
            print(f"Failed to connect to RabbitMQ: {e}")
        sleep(1)

    return connection


connection = connect_to_rabbitmq()
channel = connection.channel()

channel.queue_declare(queue=CURRENT_QUEUE)


class ConsumeHandler:
    """
    Handle the consumed messages from the RabbitMQ queue
    """
    def __init__(self, action_type: str, data: dict):
        # Handle the action
        self.handle(action_type, data)

    def handle(self, action_type: str, data: dict):
        """
        Handle the action based on the action type
        """
        method_name = action_type.replace(".", "_")
        method = getattr(self, method_name, None)

        if callable(method):
            method(data)
        else:
            msg = f"New action detected. Cannot find handling method for,\nAction: {action_type}"
            warning(msg)

    def user_created(self, data):
        # Create a new user
        try:
            user = User(
                id=data["id"],
                full_name=data["full_name"],
            )
            user.save()
            info(f"QUEUE - {CURRENT_QUEUE}: User created")
        except Exception as e:
            error(f"QUEUE - {CURRENT_QUEUE}: Failed to save user [{data['id']}]: {e}")

    def user_updated(self, data):
        # Update an existing user
        try:
            user = User.objects.get(id=data["id"])
            user.full_name = data["full_name"]
            user.save()
            info(f"QUEUE - {CURRENT_QUEUE}: User updated")
        except Exception as e:
            error(f"QUEUE - {CURRENT_QUEUE}: Failed to update user [{data['id']}]: {e}")

    def user_deleted(self, data):
        # Delete a user
        try:
            user = User.objects.get(id=data["id"])
            user.delete()
            info(f"QUEUE - {CURRENT_QUEUE}: User deleted")
        except Exception as e:
            error(f"QUEUE - {CURRENT_QUEUE}: Failed to delete user [{data['id']}]: {e}")

    def friend_created(self, data):
        # Create a friend room
        try:
            room = Room()
            room.save()
            for usr in data["friends"]:
                user = User.objects.filter(id=usr["id"]).first()
                if not user:
                    user = User(
                        id=usr["id"],
                        full_name=usr["full_name"],
                    )
                    user.save()
                room.users.add(user)
            info(f"QUEUE - {CURRENT_QUEUE}: Friend Room created")
        except Exception as e:
            error(f"QUEUE - {CURRENT_QUEUE}: Failed to create friend: {e}")


def callback(chnl, method, properties, body):
    # Callback function to consume messages
    data = json.loads(body)
    action_type = properties.content_type
    info(f'"CONSUMED - QUEUE: {CURRENT_QUEUE} | ACTION: {action_type}"')
    ConsumeHandler(action_type, data)


channel.basic_consume(queue=CURRENT_QUEUE, on_message_callback=callback, auto_ack=True)

print(f"[{CURRENT_QUEUE.upper()}] Started consuming...")
channel.start_consuming()
channel.close()
