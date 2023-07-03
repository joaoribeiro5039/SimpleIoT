FROM python:3.11-slim

RUN mkdir /opcserver

WORKDIR /usr/src/opcserver

COPY opcuaserver.py .
COPY nodes.json nodes.json

RUN pip install --upgrade pip
RUN pip install numpy
RUN pip install opcua

EXPOSE 4840

CMD ["python","opcuaserver.py"]