import os


class BaseConfig(object):
    APP_NAME = os.environ.get("APP_NAME", "lambda-function")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")
    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
