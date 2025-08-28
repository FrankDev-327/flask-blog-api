import os
from app import app
from logger.logging import LoggerApp
from dotenv import load_dotenv

load_dotenv()
logger = LoggerApp();

if __name__ == '__main__':
    logger.logInfo('server starting...');
    app.run(host=os.getenv('HOST'), port=os.getenv('PORT'), debug=True)