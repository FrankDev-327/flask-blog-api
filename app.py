import os
import models
import logging
from flask_restful import Api
from flask import Flask, jsonify, request
from db_connection.data_base import DataBase
from werkzeug.exceptions import HTTPException
from routes.user_route import register_user_routes
from routes.post_route import register_post_routes
from routes.comment_route import register_comment_route
from routes.health_check_route import register_health_check_route
from connection import init_db, db, init_migrate 

app = Flask(__name__)
dbConn = DataBase()
api = Api(app, prefix="/api", default_mediatype='application/json', catch_all_404s=True)
app.secret_key = os.getenv('SECRET_SESSION')

init_db(app)
init_migrate(app)

if not dbConn.connect():
    dbConn.disconnect() 

if os.getenv('ENV_APP') == 'development':
    logging.basicConfig(filename='myapp.log', level=logging.DEBUG)

@app.route('/')
def getAllMethods():
    pass

register_user_routes(api);
register_post_routes(api);
register_comment_route(api);
register_health_check_route(api);

# Catch all HTTP errors (4xx, 5xx)
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    response = {
        "error": e.name,       # e.g. "Not Found"
        "message": e.description,
        "status": e.code
    }
    return jsonify(response), e.code


# Catch non-HTTP exceptions (uncaught errors)
@app.errorhandler(Exception)
def handle_exception(e):
    response = {
        "error": "Internal Server Error",
        "message": str(e),  # safe for all exceptions
        "status": 500
    }
    return jsonify(response), 500


