FROM python:3.11-slim

RUN pip install --upgrade pip
RUN pip install pika
RUN pip install cassandra-driver

WORKDIR /usr/src/dataservice

COPY dataservice.py .

EXPOSE 5672

CMD ["python","dataservice.py"]