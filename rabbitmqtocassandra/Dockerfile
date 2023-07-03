FROM python:3.11-slim

RUN pip install --upgrade pip
RUN pip install pika
RUN pip install cassandra-driver
RUN pip install requests

WORKDIR /usr/src/rabbitmqtocassandra

COPY rabbitmqtocassandra.py .

EXPOSE 5672
EXPOSE 15672

CMD ["python","rabbitmqtocassandra.py"]