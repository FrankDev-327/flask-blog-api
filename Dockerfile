# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ARG APP_DIR=/flask-api
WORKDIR $APP_DIR

COPY requirements.txt $APP_DIR/requirements.txt
RUN pip3 install -r requirements.txt

ENV DB_CONN="" \
    PORT= \
    DEBUG_MODE= \
    HOST="" \
    ENV_APP="" \
    SECRET_SESSION=""

COPY . .

CMD [ "python3", "-m", "flask", "--app", "run_server", "run", "--host=0.0.0.0"]