FROM python:3-alpine
RUN mkdir /MonitorService
WORKDIR /usr/src/MonitorService
COPY MonitorService.py .
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 4840
EXPOSE 5672

CMD ["python","MonitorService.py","--host","0.0.0.0"]