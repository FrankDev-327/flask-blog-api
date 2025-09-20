import os
from flask_cors import CORS
from app import app, socketio
from dotenv import load_dotenv
from logger.logging import LoggerApp


CORS(app)
load_dotenv()
logger = LoggerApp();

if __name__ == '__main__':
    logger.logInfoServer('server starting...');
    socketio.run(host=os.getenv('HOST'), port=os.getenv('PORT'), debug=True)