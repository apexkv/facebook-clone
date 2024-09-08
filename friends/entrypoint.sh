#!/bin/bash

echo "Waiting for MySQL Posts Database to start..."
./wait-for-it.sh friends-db:7687 --strict

echo "Waiting for Redis server to start..."
./wait-for-it.sh friends-cache:6379 --strict

echo "Waiting for RabbitMQ to start..."
./wait-for-it.sh rabbitmq:5672 --strict

echo "Making Migrations..."
python manage.py makemigrations

echo "Migrating the Database..."
python manage.py install_labels

echo "Starting the consumer..."
python consumer.py &

echo "Starting the server..."
python manage.py runserver 0.0.0.0:8000


exec "$@"