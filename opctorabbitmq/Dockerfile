FROM python:3.11-slim

RUN mkdir /opcserver

WORKDIR /usr/src/opcserver

COPY opcuaserver.py .
COPY nodes.json nodes.json

RUN pip install --upgrade pip
RUN pip install numpy
RUN pip install opcua
RUN pip install confluent_kafka
RUN pip install pika

EXPOSE 4840
EXPOSE 4841
EXPOSE 4842
EXPOSE 4843
EXPOSE 4844
EXPOSE 4845
EXPOSE 4846
EXPOSE 4847
EXPOSE 4848
EXPOSE 4849
EXPOSE 5672

CMD ["python","opcuaserver.py"]