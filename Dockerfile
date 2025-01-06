FROM ubuntu:latest
LABEL authors="MX"
FROM python:3.12

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["top", "-b"]