import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import argparse

def setup_logger():
    log_date = datetime.now().strftime("%Y_%m_%d")
    logger_name = "<INSERT_LOGGER_NAME>_" + log_date
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    handler = TimedRotatingFileHandler(
        filename=f"{'app'}.log",
        when='midnight',
        interval=1,
        backupCount=7
    )
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger



def parse_args():
    parser = argparse.ArgumentParser(description="Program description")
    parser.add_argument('--log', choices=['debug', 'info', 'warning', 'error', 'critical'], default='info',
                        help='Set the logging level')
    # Template for additional arguments:
    # parser.add_argument('--param', required=False, type=str, help='Description')
    # Add more arguments as needed
    return parser.parse_args()


