FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN  pip install --no-cache-dir -r requirements.txt

COPY . /app/
