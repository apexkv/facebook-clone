#!/bin/bash

echo "Waiting for MySQL Post-Write Database to start..."
./wait-for-it.sh friendship-db:7474 --strict

echo "Waiting for RabbitMQ to start..."
./wait-for-it.sh rabbitmq:5672 --strict

echo "Making Migrations..."
python manage.py makemigrations

echo "Migrating the Database..."
python manage.py install_labels

echo "Starting the server..."
python manage.py runserver 0.0.0.0:8000

exec "$@"