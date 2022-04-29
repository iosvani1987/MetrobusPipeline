FROM python:3.7.13

ENV MYSQL_HOST 192.168.1.115
ENV MYSQL_PORT 33066
ENV MYSQL_USER root
ENV MYSQL_PASSWORD root
ENV MYSQL_DATABASE metrobus_db

WORKDIR /api
COPY requirements.txt /api/requirements.txt

RUN pip install -r requirements.txt

COPY . /api

# Run server
EXPOSE 5000
CMD ["python", "api/main.py"]