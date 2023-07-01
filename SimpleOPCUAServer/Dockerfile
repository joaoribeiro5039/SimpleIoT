FROM python:3.11-slim

RUN mkdir /opcserver

WORKDIR /usr/src/opcserver

COPY requirements.txt .
COPY opcuaserver.py .
COPY nodes.json nodes.json

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

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
EXPOSE 9092

CMD ["python","opcuaserver.py"]