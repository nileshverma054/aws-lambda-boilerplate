import logging
from config import BaseConfig
from pythonjsonlogger import jsonlogger


class GlobalVars(object):
    """ class holding app global variables """

    def __init__(self):
        self.request_id = ''


log_format = '%(request_id)s - %(asctime)s - %(levelname)s - %(component)s - %(message)s'
g_vars = GlobalVars()


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = g_vars.request_id
        return True


class ComponentFilter(logging.Filter):
    def filter(self, record):
        record.component = BaseConfig.APP_NAME
        return True


def get_logger(name):
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)

    logger = logging.getLogger(name)
    logger.addFilter(RequestIdFilter())
    logger.addFilter(ComponentFilter())
    logger.setLevel(BaseConfig.LOG_LEVEL)

    stream_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(log_format)
    formatter = logging.Formatter(log_format)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


log = get_logger(BaseConfig.APP_NAME)
