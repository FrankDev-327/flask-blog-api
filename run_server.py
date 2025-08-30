import os
from app import app
from flask_cors import CORS
from logger.logging import LoggerApp
from dotenv import load_dotenv

load_dotenv()
CORS(app)
logger = LoggerApp();

if __name__ == '__main__':
    logger.logInfoServer('server starting...');
    app.run(host=os.getenv('HOST'), port=os.getenv('PORT'), debug=True)