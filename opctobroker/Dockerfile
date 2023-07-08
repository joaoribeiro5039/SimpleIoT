FROM python:3.11-slim

RUN mkdir /opctobroker

WORKDIR /usr/src/opctobroker

COPY opctobroker.py .

RUN pip install --upgrade pip
RUN pip install numpy
RUN pip install opcua
RUN pip install pika
RUN pip install confluent-kafka
RUN pip install paho-mqtt

EXPOSE 4840
EXPOSE 5672
EXPOSE 29092
EXPOSE 9092
EXPOSE 9042
EXPOSE 1883

CMD ["python","opctobroker.py"]