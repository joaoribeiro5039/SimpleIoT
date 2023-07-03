FROM python:3.11-slim

RUN mkdir /opctorabbitmq

WORKDIR /usr/src/opctorabbitmq

COPY opctorabbitmq.py .

RUN pip install --upgrade pip
RUN pip install numpy
RUN pip install opcua
RUN pip install pika

EXPOSE 4840
EXPOSE 5672

CMD ["python","opctorabbitmq.py"]