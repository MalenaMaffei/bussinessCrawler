import logging
import sys

class Logger:
    def __init__(self, logName):
        formatter = logging.Formatter("%(asctime)s  [%(levelname)-5.5s]  %(message)s")
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # file handler
        f_handler = logging.FileHandler(f'{logName}.log')
        f_handler.setLevel(logging.DEBUG)
        f_handler.setFormatter(formatter)

        # stream handler
        c_handler = logging.StreamHandler(sys.stdout)
        c_handler.setFormatter(formatter)
        c_handler.setLevel(logging.INFO)

        # add the handlers to the logger
        logger.addHandler(f_handler)
        logger.addHandler(c_handler)

        self.logger = logger

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)