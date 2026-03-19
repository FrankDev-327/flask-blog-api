import logging


class LoggerApp:
    def __init__(self):
        self.loggerInfo = logging.getLogger(__name__)
        self.loggerError = logging.getLogger(__name__)
        logging.basicConfig(
            filename="api.log",
            filemode="w",
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.INFO,
            )

    def initLoggerInstance(self):
        FileOutputHandlerError = logging.FileHandler("error-logs.log")
        FileOutputHandler = logging.FileHandler("info-logs.log")

        self.loggerInfo.addHandler(FileOutputHandler)
        self.loggerError.addHandler(FileOutputHandlerError)

    def logInfoServer(self, infoText):
        self.loggerInfo.info(infoText)

    def logErrorInfo(self, infoToLog):
        self.loggerError.error(infoToLog)
