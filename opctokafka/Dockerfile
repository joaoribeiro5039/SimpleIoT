FROM python:3.11-slim

RUN mkdir /opctokafka

WORKDIR /usr/src/opctokafka

COPY opctokafka.py .

RUN pip install --upgrade pip
RUN pip install opcua
RUN pip install confluent-kafka

EXPOSE 4840
EXPOSE 29092

CMD ["python","opctokafka.py"]