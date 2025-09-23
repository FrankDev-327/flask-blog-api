import os
import jwt
import time
from flask import request, abort
from logger.logging import LoggerApp
from prometheus_client import Gauge, Histogram
from services.token_service import TokenService
from services.rabbit_mq_service import RabbitMqService
from flask_socketio import SocketIO, ConnectionRefusedError

request_latency = Histogram('socket_request_latency_seconds', 'Socket Request latency', ['event'])
request_gauge = Gauge('socket_active_connections', 'Number of active socket connections')

class SockerService:
    def __init__(self, appInstance):
        self.user_conn = []
        self.logger = LoggerApp()
        self.token_service = TokenService()
        #self.rabbit_service = RabbitMqService()
        self.socket = SocketIO(appInstance, cors_allowed_origins="*")
                
    def getSocketInstanceServer(self):
        return self.socket
    
    """ def callback(ch, method, properties, body):
        print(f"Received {body}") """    
    
    def register_all_sockets(self):

        @self.socket.on('connect')
        def init_connection(auth):
            token = request.args.get('token')
            check_token = self.token_service.getTokenById(token)

            if check_token is None:
                request_gauge.dec()
                raise ConnectionRefusedError('unauthorized!')
            elif check_token.get('marked_as_used'):
                raise ConnectionRefusedError('Token has been marked as used in blacklist!')
             
            try:
                payload = jwt.decode(
                    check_token['token'], 
                    os.getenv('SECRET_KEY'), 
                    do_time_check=True, 
                    algorithms=['HS256']
                )
                request.user = payload
                self.user_conn[request.user['id']] = request.sid
                request_gauge.inc()
            except jwt.ExpiredSignatureError:
                request_gauge.dec()
                self.logger.logErrorInfo({'errorMsg': 'Token expired'})
                raise ConnectionRefusedError('Token expired!')
            except jwt.InvalidTokenError:
                request_gauge.dec()
                self.token_service.createToken(token, marked_as_used=True)
                self.logger.logErrorInfo({'errorMsg': 'Invalid token'})
                raise ConnectionRefusedError('Invalid token!')
                       
        #self.rabbit_service.consume('mention_comment_notification', self.callback)  
            
        @self.socket.on('disconnect')
        def init_disconnection(reason):
            request_gauge.dec()

        @self.socket.on('message')
        def getClientMessages(data):
            startTime = time.time()
            latency = time.time() - startTime
            request_latency.labels(event='message').observe(latency)
            self.socket.emit('message', {'message': data}, to=request.sid)

    def callback(ch, method, properties, body):
        print(body)
        