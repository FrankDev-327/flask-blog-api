import os
import pika
import time
from pika.exceptions import AMQPConnectionError


class RabbitMqService:
    def __init__(self, max_retries=5, retry_delay=5):
        self.user = os.getenv("RABBITMQ_USER", "guest")
        self.password = os.getenv("RABBITMQ_PASSWORD", "guest")
        self.host = os.getenv("RABBITMQ_HOST", "rabbitmq")
        self.port = int(os.getenv("RABBITMQ_PORT", 5672))
        self.connection = None
        self.channel = None
        self.connect()
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.connect_with_retry()

    def connect_with_retry(self):
        retries = 0
        while retries < self.max_retries:
            try:
                self.connect()
                print(f"Connected to RabbitMQ at {self.host}:{self.port}")
                return
            except AMQPConnectionError as e:
                retries += 1
                print(f"RabbitMQ connection failed ({retries}/{self.max_retries}): {e}")
                time.sleep(self.retry_delay)
        raise Exception(
            f"Could not connect to RabbitMQ after {self.max_retries} retries"
        )

    def connect(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300,
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connect_with_retry()

    def consume(self, queue_name, callback):
        if not self.channel:
            self.connect_with_retry()

        self.channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True
        )
        self.channel.start_consuming()

    def publish(self, queue_name, message):
        try:
            if not self.channel:
                self.logger.logErrorInfo(
                    {
                        "messerrorMsgage": "Connection is not established raised: publish rabbit}"
                    }
                )
                raise Exception("Connection is not established.")
            self.channel.queue_declare(queue=queue_name, durable=True)
            self.channel.basic_publish(
                exchange="mention_comment",
                routing_key=queue_name,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
            )

            print(f"Sent message to queue {queue_name}: {message}")
        except pika.exceptions.AMQPConnectionError as e:
            print("AMQPConnectionError:", e)
            raise
        except pika.exceptions.AMQPChannelError as e:
            print("AMQPChannelError:", e)
            raise
        except pika.exceptions.ProbableAuthenticationError as e:
            print("Authentication failed:", e)
            raise
        except pika.exceptions.ProbableAccessDeniedError as e:
            print("Access denied:", e)
            raise
        except pika.exceptions.AMQPError as e:
            print("AMQPError:", e)
            raise
        except Exception as e:
            print("Other exception:", e)
            raise
