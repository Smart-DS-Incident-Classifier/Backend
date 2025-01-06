FROM ubuntu:latest
LABEL authors="DistributedSystemProject"
FROM python:3.12

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["top", "-b"]