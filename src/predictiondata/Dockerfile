FROM python:3.11-slim

RUN mkdir /opcserver

WORKDIR /usr/src/opcserver

COPY predictdata.py .

RUN pip install --upgrade pip

CMD ["python","predictdata.py"]