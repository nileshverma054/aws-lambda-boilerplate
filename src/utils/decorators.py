import json
import time
from uuid import uuid4
from functools import wraps
from utils.logger import log, g_vars
from utils.parser import LambdaParser


def lambda_handler(parser):
    """
    A decorator that formats Lambda requests and responses.
    """
    def handler(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            ts = time.time()
            log.debug(f"lambda handler {fn.__name__} invoked with "
                      f"args: {args} and kwargs: {kwargs}")
            response = None
            try:
                payload = parser(*args, **kwargs)
                log.info(f"payload: {payload}")
                g_vars.request_id = payload.get("request_id")
                if not g_vars.request_id:
                    g_vars.request_id = str(uuid4())
                    log.info(f"could not find request_id in message body.. "
                             f"generated new request_id: {g_vars.request_id}")
                result = fn(payload)
                if type(result) is dict:
                    result["request_id"] = g_vars.request_id
                else:
                    result = {
                        "request_id": g_vars.request_id,
                        "message": result
                    }
                response = {
                    "status_code": 200,
                    "body": result
                    }
                log.info(f"function {fn.__name__} response: {response}")
            except Exception as e:
                log.exception(f"unknown exception in lambda_handler: {e}")
                response = {
                    "status_code": 500,
                    "body": {
                        "request_id": g_vars.request_id,
                        "message": 'something went wrong'
                        }
                    }
            finally:
                log.info(f'function {fn.__name__} completed '
                         f'in {(time.time() - ts):2.4f}s')
                return response
        return wrapper
    return handler


def api_handler(fn):
    """
    A decorator function to format API requests and responses.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        ts = time.time()
        log.debug(f"lambda handler {fn.__name__} invoked with "
                  f"args: {args} and kwargs: {kwargs}")
        response = {
            "headers": {
                "Content-Type": "application/json",
                }
            }
        try:
            payload = LambdaParser.api(*args, **kwargs)
            log.info(f"payload: {payload}")
            g_vars.request_id = payload.get("body", {}).get("request_id") \
                or payload.get("headers", {}).get("X-Request-Id")
            if not g_vars.request_id:
                g_vars.request_id = str(uuid4())
                log.info(f"could not find request_id in message body.. "
                         f"generated new request_id: {g_vars.request_id}")
            status_code, body = fn(payload)
            body["request_id"] = g_vars.request_id
            response.update(
               statusCode=status_code,
               body=json.dumps(body)
            )
            log.info(f"function {fn.__name__} response: {response}")
        except Exception as e:
            log.exception(f"unknown exception in api_handler: {e}")
            response.update(
               statusCode=500,
               body=json.dumps({
                   "request_id": g_vars.request_id,
                   "message": 'something went wrong'
               })
            )
        finally:
            log.info(f'function {fn.__name__} completed '
                     f'in {(time.time() - ts):2.4f}s')
            return response
    return wrapper
