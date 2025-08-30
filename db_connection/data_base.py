import os
from logger.logging import LoggerApp
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

class DataBase:
    def __init__(self):
        self.db_url = os.getenv('DB_CONN')
        self.engine = None
        self.logger = LoggerApp()

    def connect(self):
        try:
            self.engine = create_engine(self.db_url)
            self.engine.connect()
            self.logger.logInfoServer("Database connection established.")
            print("Database connection established.")
            return True
        except OperationalError as e:
            self.logger.logErrorInfo(f"Error connecting to the database: {e}")
            print(f"Error connecting to the database: {e}")
            return False

    def disconnect(self):
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self.logger.logInfoServer("Database connection closed.")
            print("Database connection closed.")
        else:
            self.logger.logInfoServer("No active database connection to close.")
            print("No active database connection to close.")
            return {'message': 'User not found'}, 404

    def getUrlConnection(self):
        return self.db_url