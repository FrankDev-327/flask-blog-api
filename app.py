import os
from flask_restful import Api
from logger.logging import LoggerApp
from flask import Flask, jsonify
from db_connection.data_base import DataBase
from werkzeug.exceptions import HTTPException
from routes.user_route import register_user_routes
from routes.post_route import register_post_routes
from routes.comment_route import register_comment_route
from routes.health_check_route import register_health_check_route
from connection import init_db, init_migrate 

log = LoggerApp()
dbConn = DataBase()
app = Flask(__name__)
api = Api(app, prefix="/api", default_mediatype='application/json', catch_all_404s=True)
app.secret_key = os.getenv('SECRET_SESSION')

init_db(app)
init_migrate(app)
log.initLoggerInstance()

if not dbConn.connect():
    dbConn.disconnect() 

@app.route('/')
def getAllMethods():
    pass

#Routes section
register_user_routes(api);
register_post_routes(api);
register_comment_route(api);
register_health_check_route(api);

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


