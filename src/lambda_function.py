from utils.logger import log
from utils.parser import LambdaParser
from utils.decorators import lambda_handler, api_handler


@lambda_handler(parser=LambdaParser.sqs)
def sqs_lambda(payload):
    log.info(f"payalod received to sqs: {payload}")
    return {"message": "request received to sqs lambda successfully!"}


@api_handler
def api_lambda(payload):
    log.info(f"payalod received to api: {payload}")
    return 200, {"message": "request received to api lambda successfully!"}


@lambda_handler(parser=LambdaParser.function_url)
def function_url_lambda(payload):
    log.info(f"payalod received to function_url_lambda: {payload}")
    return {"message": "request received to function url lambda successfully!"}
