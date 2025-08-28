import os
import logging

class LoggerApp():
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def mainLogger():
        logging.basicConfig(filename='myapp.log', level=logging.INFO)

    def logInfo(self, infoToLog):
        self.logger.info(infoToLog)