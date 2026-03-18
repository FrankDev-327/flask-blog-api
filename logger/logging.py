import logging


class LoggerApp:
    def __init__(self):
        self.loggerInfo = logging.getLogger('loggerInfo')
        self.loggerError = logging.getLogger('loggerError')
        logging.basicConfig(
            filename="api.log",
            filemode="w",
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.INFO,
        )

    def initLoggerInstance(self):
        FileOutputHandlerError = logging.FileHandler("logs/error-logs.log")
        FileOutputHandler = logging.FileHandler("logs/info-logs.log")

        self.loggerInfo.addHandler(FileOutputHandler)
        self.loggerError.addHandler(FileOutputHandlerError)

    def logInfoServer(self, infoText):
        self.loggerInfo.info(infoText)

    def logErrorInfo(self, infoToLog):
        self.loggerError.error(infoToLog)
