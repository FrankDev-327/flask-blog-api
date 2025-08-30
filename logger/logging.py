import os
import logging

class LoggerApp():
    def __init__(self):
        self.loggerInfo = logging.getLogger(__name__)
        self.loggerError = logging.getLogger(__name__)
        if os.getenv('ENV_APP') == 'development':
            logging.basicConfig(filename='api.log', filemode="w", format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        
    def initLoggerInstance(self):
        if os.getenv('ENV_APP') == 'development':
            FileOutputHandlerError = logging.FileHandler('error-logs.log')
            FileOutputHandler = logging.FileHandler('info-logs.log')
            
            self.loggerInfo.addHandler(FileOutputHandler)
            self.loggerError.addHandler(FileOutputHandlerError)
 
    def logInfoServer(self, infoText):
        if os.getenv('ENV_APP') == 'development':
            self.loggerInfo.info(infoText)
        
    def logErrorInfo(self, infoToLog):
        if os.getenv('ENV_APP') == 'development':
            self.loggerError.error(infoToLog)