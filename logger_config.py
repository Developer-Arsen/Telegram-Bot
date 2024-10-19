# logger_config.py
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

def setup_logger():
    log_folder = 'logs'
    
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_filename = os.path.join(log_folder, f"{datetime.now().strftime('%Y-%m-%d')}_error_log.log")
    logger = logging.getLogger("my_logger")
    
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=5)
    handler.setLevel(logging.INFO)  

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s\n')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
