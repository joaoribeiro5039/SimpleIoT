FROM python:3.11-slim

RUN pip install --upgrade pip
RUN pip install pika
RUN pip install redis
RUN pip install requests

WORKDIR /usr/src/rabbitmqtoredis

COPY rabbitmqtoredis.py .

EXPOSE 5672
EXPOSE 15672
EXPOSE 6379

CMD ["python","rabbitmqtoredis.py"]