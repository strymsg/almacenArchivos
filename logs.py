import logging
import logging.handlers
import sys

class Logger:
    def __init__(self, logger):
        self.logger = logger

    def write(self, message, level=logging.INFO):
        message = message.rstrip()
        if message != '':
            self.logger.log(level, message)

def initLogs(logFile, logLevel=logging.INFO, debug=False):
    # Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
    # Give the logger a unique name (good practice)
    logger = logging.getLogger(__name__)
    # Set the log level to LOG_LEVEL
    logger.setLevel(logLevel)
    # Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
    handler = logging.handlers.TimedRotatingFileHandler(logFile, when="midnight", backupCount=3)
    # Format each log message like this
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    # Attach the formatter to the handler
    handler.setFormatter(formatter)
    # Attach the handler to the logger
    logger.addHandler(handler)

    if not debug:
        lgr = Logger(logger)
        # sys.stdout = MyLogger(logger, logging.INFO)
        sys.stdout = lgr
        # Replace stderr with logging to file at ERROR level
        sys.stderr = lgr
