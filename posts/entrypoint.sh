#!/bin/bash

echo "Waiting for MySQL Posts Database to start..."
./wait-for-it.sh posts-db:3306 --strict

echo "Waiting for RabbitMQ to start..."
./wait-for-it.sh rabbitmq:5672 --strict

echo "Making Migrations..."
python manage.py makemigrations

echo "Migrating the Database..."
python manage.py migrate

echo "Starting the consumer..."
python consumer.py &

echo "Starting the server..."
python manage.py runserver 0.0.0.0:8000


exec "$@"