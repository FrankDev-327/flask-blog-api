import os
import jwt
import time
import json
from threading import Thread
from flask import request, abort
from logger.logging import LoggerApp
from prometheus_client import Gauge, Histogram, Counter
from services.token_service import TokenService
from redis_serve.redis_service import RedisService
from flask_socketio import SocketIO, ConnectionRefusedError
from services.notifications_service import NotificationService
from services.private_message_service import PrivateMessageService

request_latency = Histogram('socket_request_latency_seconds', 'Socket Request latency', ['event'])
request_gauge = Gauge('socket_active_connections', 'Number of active socket connections')
request_count_messages = Counter('messages_counter', 'Number of messages sent', ['count_messages'])

class SockerService:
    def __init__(self, appInstance):
        self.user_conn = {}
        self.logger = LoggerApp()
        self.app = appInstance
        self.token_service = TokenService()
        self.redis_service = RedisService()
        self.notification_service = NotificationService()
        self.private_message_service = PrivateMessageService()
        self.socket = SocketIO(appInstance, cors_allowed_origins="*")
                
    def getSocketInstanceServer(self):
        return self.socket
    
    def start_redis_listener(self):
        def listen_user_mentioned():
            with self.app.app_context():
                pubsub = self.redis_service.subscribe("mention_comment_notification")
                try:
                    for message in pubsub.listen():
                        if message['type'] == 'message':  
                            data = json.loads(message['data'])
                            user_ids = data.get("user_ids", [])
                            for user_id in user_ids:
                                self.notification_service.create_notification(
                                    user_id,
                                    data.get('comment_id'),
                                    data.get('type'),
                                    data.get('content')
                                )
                                if user_id in self.user_conn:
                                    sid = self.user_conn[user_id]
                                    self.socket.emit(data.get('type'), data, to=sid)
                                else:
                                    self.logger.logInfoServer(f"User {user_id} not connected, skipping")
                except Exception as e:
                    self.logger.logErrorInfo({"errorMsgRedis": str(e)})
                    
        def friend_request_listener():
            with self.app.app_context():
                pubsub = self.redis_service.subscribe("friend_request_notification")
                try:
                    for message in pubsub.listen():
                        if message['type'] == 'message':  
                            data = json.loads(message['data'])
                            user_id = data.get("contact_id")
                            if user_id:
                                self.notification_service.create_notification(
                                    user_id,
                                    data.get('contact_id'),
                                    data.get('type'),
                                    data.get('content')
                                )
                                if user_id in self.user_conn:
                                    sid = self.user_conn[user_id]
                                    self.socket.emit(data.get('type'), data, to=sid)
                                else:
                                    self.logger.logInfoServer(f"User not connected, skipping")
                except Exception as e:
                    self.logger.logErrorInfo({"errorMsgRedis": str(e)}) 

        thread_to_listen = Thread(target=listen_user_mentioned, daemon=True)
        thread_to_request_friend = Thread(target=friend_request_listener, daemon=True)
        
        thread_to_listen.start()
        thread_to_request_friend.start()

    def register_all_sockets(self):
        @self.socket.on('connect')
        def init_connection(auth):
            try:
                token = request.args.get('token')
                check_token = self.token_service.getTokenById(token)

                if check_token is None:
                    request_gauge.dec()
                    raise ConnectionRefusedError('unauthorized!')
                elif check_token.get('marked_as_used'):
                    raise ConnectionRefusedError('Token has been marked as used in blacklist!')
             
                payload = jwt.decode(
                    check_token['token'], 
                    os.getenv('SECRET_KEY'), 
                    algorithms=['HS256']
                )
                request.user = payload
                self.user_conn[request.user['id']] = request.sid
                socket_user_key = f"socket_{request.user['id']}"
                self.redis_service.setTemporalInfo(socket_user_key, payload, ttl=None)
                request_gauge.inc()
            except jwt.ExpiredSignatureError:
                self.logger.logErrorInfo({'errorMsg': 'Token expired'})
                raise ConnectionRefusedError('Token expired!')
            except jwt.InvalidTokenError:
                self.token_service.createToken(token, marked_as_used=True)
                self.logger.logErrorInfo({'errorMsg': 'Invalid token'})
                raise ConnectionRefusedError('Invalid token!')
                        
        @self.socket.on('disconnect')
        def init_disconnection(reason):
            for user_id, sid in list(self.user_conn.items()):
                if sid == request.sid:
                    request_gauge.dec()
                    del self.user_conn[user_id]
                    socket_user_key = f"socket_{user_id}"
                    self.redis_service.deleteTemporalInfo(socket_user_key)
                    break
        
        @self.socket.on('message')
        def getClientMessages(data):
            startTime = time.time()
            latency = time.time() - startTime
            self.private_message_service.save_private_message(data)
            request_latency.labels(event='message').observe(latency)
            request_count_messages.labels(count_messages=1).inc()
            self.socket.emit('message', {'message': data}, to=request.sid)
            
        