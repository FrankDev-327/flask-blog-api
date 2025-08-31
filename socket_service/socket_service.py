from flask_socketio import SocketIO, ConnectionRefusedError

class SockerService:
    def __init__(self, appInstance):
        self.socket = SocketIO(appInstance)
                
    def getSocketInstanceServer(self):
        return self.socket
    
    def register_all_sockets(self):
        self.socket.on('connect')
        def init_connection(auth):
            if auth is None:
                raise ConnectionRefusedError('unauthorized!')
            
        
        self.socket.on('disconnect')
        def init_disconnection(reason):
            pass
        
        @self.socket.on('message')
        def getClientMessages(data):
            self.socket.emit('message', {'message': data})
            
    