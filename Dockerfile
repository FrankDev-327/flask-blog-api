# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ARG APP_DIR=/flask-api
WORKDIR $APP_DIR

COPY requirements.txt $APP_DIR/requirements.txt
COPY entrypoint.sh /entrypoint.sh

RUN pip3 install --no-cache-dir -r requirements.txt
RUN chmod +x /entrypoint.sh

COPY . .

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
