# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "80"]