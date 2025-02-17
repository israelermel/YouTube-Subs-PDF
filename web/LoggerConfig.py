import logging
from logging.handlers import RotatingFileHandler
import os

class LoggerConfig:
    def __init__(self, env_var='ENVIRONMENT'):
        self.env = os.getenv(env_var, 'DEBUG')
        self.configure_logging()

    def configure_logging(self):
        log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_handler = RotatingFileHandler('web.log', maxBytes=1000000, backupCount=3)
        log_handler.setFormatter(log_formatter)

        if self.env == 'PRODUCTION':
            log_handler.setLevel(logging.INFO)
            logging.getLogger().setLevel(logging.INFO)
        else:
            log_handler.setLevel(logging.DEBUG)
            logging.getLogger().setLevel(logging.DEBUG)

        logging.getLogger().addHandler(log_handler)