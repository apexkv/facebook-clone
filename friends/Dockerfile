FROM python:3.11.9

ENV PYTHONUNBUFFERED 1

# current working directory
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy files from users folder to /app folder
COPY . /app/

EXPOSE 8000

RUN chmod +x /app/wait-for-it.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
