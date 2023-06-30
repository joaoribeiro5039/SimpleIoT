FROM python:3.11-slim

RUN pip install --upgrade pip
RUN pip install opcua
RUN pip install confluent-kafka

WORKDIR /usr/src/edgeservice

COPY edgeservice.py .
COPY monitorconfig.json .

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
EXPOSE 4849
EXPOSE 9092


CMD ["python","edgeservice.py"]