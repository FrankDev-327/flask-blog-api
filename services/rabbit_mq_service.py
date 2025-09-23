import os 
import pika

class RabbitMqService:
    def __init__(self):
        print(os.getenv('RABBITMQ_HOST'))
        self.user = os.getenv('RABBITMQ_USER', 'guest')
        self.password = os.getenv('RABBITMQ_PASSWORD', 'guest')
        self.host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
        self.port = int(os.getenv('RABBITMQ_PORT', 5672)) 
        self.connection = None
        self.channel = None
        self.connect()
        
    def connect(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        
    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            
    def consume(self, queue_name, callback):
        if not self.channel:
            raise Exception("Connection is not established.")
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def publish(self, queue_name, message):
        try:
            if not self.channel:
                self.logger.logErrorInfo({'messerrorMsgage':  f'Connection is not established raised:  {str(e)}'})
                raise Exception("Connection is not established.")
            self.channel.queue_declare(queue=queue_name, durable=True)
            self.channel.basic_publish(
            exchange='mention_comment',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                )
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
        except pika.exceptions.AMQPError as e:  # general AMQP error
            print("AMQPError:", e)
            raise
        except Exception as e:
            print("Other exception:", e)
            raise