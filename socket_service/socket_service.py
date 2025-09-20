import time
from prometheus_client import Gauge, Histogram
from flask_socketio import SocketIO, ConnectionRefusedError


request_latency = Histogram('socket_request_latency_seconds', 'Socket Request latency', ['event'])
request_gauge = Gauge('socket_active_connections', 'Number of active socket connections')

class SockerService:
    def __init__(self, appInstance):
        self.socket = SocketIO(appInstance)
                
    def getSocketInstanceServer(self):
        return self.socket
    
    def register_all_sockets(self):
        self.socket.on('connect')
        request_gauge.inc()
        def init_connection(auth):
            if auth is None:
                raise ConnectionRefusedError('unauthorized!')
            
        
        self.socket.on('disconnect')
        def init_disconnection(reason):
            request_gauge.dec()
            pass
        
        @self.socket.on('message')
        def getClientMessages(data):
            startTime = time.time()
            latency = time.time() - startTime
            request_latency.labels(event='message').observe(latency)
            self.socket.emit('message', {'message': data})
            
    