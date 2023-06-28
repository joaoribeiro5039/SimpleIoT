FROM python:3.11-slim

RUN pip install --upgrade pip
RUN pip install opcua
RUN pip install confluent-kafka

WORKDIR /usr/src/edgeservice

COPY edgeservice.py .
COPY monitorconfig.json .

CMD ["python","edgeservice.py","--host","0.0.0.0"]