#!/bin/bash

echo "Waiting for RabbitMQ to start..."
./wait-for-it.sh rabbitmq:5672 --strict -t 30

echo "Waiting for MySQL Post-Write Database to start..."
./wait-for-it.sh posts-write-db:3306 --strict -t 30

echo "Making Migrations..."
python manage.py makemigrations

echo "Migrating the Database..."
python manage.py migrate

echo "Starting the server..."
python manage.py runserver 0.0.0.0:8000 &

echo "Starting RabbitMQ Consumer..."
python consumers.py

exec "$@"