FROM python:3-alpine

RUN mkdir /opcserver

WORKDIR /usr/src/opcserver

COPY requirements.txt .
COPY edgeservice.py .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 4840

CMD ["python","edgeservice.py","--host","0.0.0.0"]