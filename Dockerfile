FROM python:3.7.13
ENV PYTHONUNBUFFERED 1
ENV APP_ENVIROMENT dev
WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app