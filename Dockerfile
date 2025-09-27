FROM python:3.8-slim-buster

ARG APP_DIR=/flask-api
WORKDIR $APP_DIR

COPY requirements.txt $APP_DIR/requirements.dev.txt
COPY entrypoint.sh /entrypoint.sh

RUN pip3 install build
RUN pip3 install --no-cache-dir -r requirements.dev.txt

RUN chmod +x /entrypoint.sh

COPY . .

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
