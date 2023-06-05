FROM python:3-alpine
RUN mkdir /api
WORKDIR /usr/src/api
COPY api.py .
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn","api:app","--host","0.0.0.0"]