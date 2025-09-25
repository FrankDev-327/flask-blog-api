import os
import time
import traceback
from flasgger import Swagger
from flask_restful import Api
from utils.helpers import bcrypt
from logger.logging import LoggerApp
from connection import init_db, init_migrate 
from db_connection.data_base import DataBase
from werkzeug.exceptions import HTTPException
from routes.authentication.auth_user import register_auth_user
from prometheus_client import Histogram, Counter
from routes.roles.role_route import register_role_route
from routes.mentions.mention_route import register_mentions_routes
from routes.users.user_route import register_user_routes
from routes.posts.post_route import register_post_routes
from routes.notifications.notification_route import register_notifications_route
from flask import Flask, jsonify, Response, request
from socket_service.socket_service import SockerService
from routes.comments.comment_route import register_comment_route
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from routes.health_check_route import register_health_check_route

request_count = Counter('api_request_count', 'Total API Request Count', ['method', 'route', 'status'])
request_latency = Histogram('api_request_latency_seconds', 'API latency', ['method', 'route', 'status'])

log = LoggerApp()
dbConn = DataBase()
app = Flask(__name__)
swagger = Swagger(app)
bcrypt.init_app(app)
socketInstance = SockerService(app)
socketio = socketInstance.getSocketInstanceServer()
app.secret_key = os.getenv('SECRET_SESSION')
api = Api(app, prefix="/api", default_mediatype='application/json', catch_all_404s=True)

init_db(app)
init_migrate(app)
log.initLoggerInstance()
socketInstance.register_all_sockets()
socketInstance.start_redis_listener()

if not dbConn.connect():
    dbConn.disconnect() 

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    method = request.method
    endpoint = request.endpoint or 'unknown'
    statusEndpoint = str(response.status_code)
    latency = time.time() - request.start_time
    request_count.labels(method=method, route=endpoint, status=statusEndpoint).inc()
    request_latency.labels(method=method, route=endpoint, status=statusEndpoint).observe(latency)
    return response

#Routes section
register_auth_user(api)
register_role_route(api)
register_user_routes(api)
register_post_routes(api)
register_comment_route(api)
register_mentions_routes(api)
register_health_check_route(api)
register_notifications_route(api)

@app.route("/metrics")
def returnMetrics():
    return  Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)   

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    response = {
        "error": e.name,
        "message": e.description,
        "status": e.code
    }
    return jsonify(response), e.code

@app.errorhandler(Exception)
def handle_all_exceptions(e):
    response = {
        "error": "Internal Server Error",
        "type": type(e).__name__, 
        "message": str(e) or repr(e),
        "status": 500
    }
    
    print("".join(traceback.format_exception(None, e, e.__traceback__)))
    return jsonify(response), 500




