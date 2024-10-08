#!/bin/bash

echo "Waiting for RabbitMQ to start..."
./wait-for-it.sh rabbitmq:5672 --strict

echo "Waiting for Neo4j Post-Write Database to start..."
./wait-for-it.sh friendship-db:7687 --strict

echo "Making Migrations..."
python manage.py makemigrations

echo "Migrating the Database..."
python manage.py install_labels

echo "Starting the server..."
python manage.py runserver 0.0.0.0:8000 &

echo "Starting RabbitMQ Consumer..."
python python consumers.py

exec "$@"