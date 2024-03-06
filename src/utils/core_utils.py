import json
from utils.logger import log
from config import BaseConfig
import boto3


def get_sqs_client():
    return boto3.client('sqs', region_name=BaseConfig.AWS_REGION)


def send_to_sqs(queue_name, payload, delay=0):
    log.info(f"inside send_to_sqs with: queue_name: {queue_name}, "
             f"delay: {delay}")
    status = False
    try:
        sqs_client = get_sqs_client()
        queue_url = sqs_client.get_queue_url(QueueName=queue_name)
        queue_url = queue_url.get("QueueUrl") if queue_url else None
        log.debug(f"SQS queue url: {queue_url}")
        if not queue_url:
            log.error("Could not find Queue URL from SQS")
            return False
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(payload),
            DelaySeconds=delay
        )
        log.info(f"SQS response: {response}")
        if response and response.get("ResponseMetadata",
                                     {}).get("HTTPStatusCode") == 200:
            log.info(f"Message sent to SQS successfully. "
                     f"Message Id: {response.get('MessageId')}")
            status = True
        else:
            log.error("Failed to submit request to SQS")
    except Exception as e:
        log.exception(f"exception while sending message to SQS: {e}")
    return status
