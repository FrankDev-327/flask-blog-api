import os
import models

from flask_restful import Api
from flask import Flask, jsonify, Response
from utils.helpers import bcrypt
from logger.logging import LoggerApp
from connection import init_db, init_migrate 
from db_connection.data_base import DataBase
from werkzeug.exceptions import HTTPException
from routes.auth_user import register_auth_user
from routes.role_route import register_role_route
from routes.user_route import register_user_routes
from routes.post_route import register_post_routes
from socket_service.socket_service import SockerService
from routes.comment_route import register_comment_route
from prometheus_client import start_http_server, generate_latest, CONTENT_TYPE_LATEST
from routes.health_check_route import register_health_check_route

log = LoggerApp()
dbConn = DataBase()
app = Flask(__name__)
bcrypt.init_app(app)
socketInstance = SockerService(app)
socketio = socketInstance.getSocketInstanceServer()
app.secret_key = os.getenv('SECRET_SESSION')
api = Api(app, prefix="/api", default_mediatype='application/json', catch_all_404s=True)

init_db(app)
init_migrate(app)
log.initLoggerInstance()
socketInstance.register_all_sockets()

if not dbConn.connect():
    dbConn.disconnect() 

@app.route('/')
def getAllMethods():
    pass

#Routes section
register_auth_user(api)
register_role_route(api)
register_user_routes(api);
register_post_routes(api);
register_comment_route(api);
register_health_check_route(api);

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
def handle_exception(e):
    response = {
        "error": "Internal Server Error",
        "message": str(e),
        "status": 500
    }
    return jsonify(response), 500


