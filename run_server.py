import os
from app import app, socketio
from flask_cors import CORS
from logger.logging import LoggerApp
from dotenv import load_dotenv
from services.prometheus_service import PrometheusService

load_dotenv()
CORS(app)
logger = LoggerApp();
prom_service = PrometheusService()

if __name__ == '__main__':
    logger.logInfoServer('server starting...');
    socketio.run(host=os.getenv('HOST'), port=os.getenv('PORT'), debug=True)