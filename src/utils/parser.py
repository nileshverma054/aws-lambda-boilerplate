import json


class LambdaParser:
    @staticmethod
    def sqs(*args, **kwargs):
        message = args[0]
        payload = message.get("Records")[0].get("body")
        payload = json.loads(payload)
        return payload

    @staticmethod
    def api(*args, **kwargs):
        request = args[0]
        body = request.get("body")
        request["body"] = json.loads(body) if body else {}
        return request

    @staticmethod
    def function_url(*args, **kwargs):
        return args[0]
