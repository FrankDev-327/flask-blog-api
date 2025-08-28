# connection.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from db_connection.data_base import DataBase

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    database = DataBase()
    app.config['SQLALCHEMY_DATABASE_URI'] = database.getUrlConnection()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "echo": False,
    }
    
    db.init_app(app)
    
def init_migrate(app):
    migrate.init_app(app, db)
