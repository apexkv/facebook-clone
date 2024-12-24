#!/bin/bash

echo "Waiting for RabbitMQ to start..."
./wait-for-it.sh rabbitmq:5672 --strict -t 30

echo "Waiting for Redis Server to start..."
./wait-for-it.sh redis-chat:6379 --strict -t 30

echo "Waiting for Postgres Post-Write Database to start..."
./wait-for-it.sh chat-db:5432 --strict -t 30

echo "Making Migrations..."
python manage.py makemigrations

echo "Migrating the Database..."
python manage.py migrate

echo "Starting the server..."
python manage.py runserver 0.0.0.0:8000

exec "$@"