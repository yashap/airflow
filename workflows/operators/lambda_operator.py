from airflow.operators import BaseOperator
from airflow.utils import apply_defaults
from airflow.exceptions import AirflowException
import boto3

import logging
import json
import base64


class LambdaOperator(BaseOperator):

    @apply_defaults
    def __init__(self, context_to_payload, lambda_function_name, *args, **kwargs):
        super(LambdaOperator, self).__init__(*args, **kwargs)
        self.context_to_payload = context_to_payload
        self.lambda_function_name = lambda_function_name
        self.lambda_client = boto3.client('lambda')

    def execute(self, context):
        request_payload = self.context_to_payload(context)

        logging.info('Making the following request against AWS Lambda %s' % request_payload)

        response = self.lambda_client.invoke(
            FunctionName=self.lambda_function_name,
            InvocationType='RequestResponse',
            Payload=bytearray(request_payload),
            LogType='Tail'
        )

        response_log_tail = base64.b64decode(response.get('LogResult'))
        response_payload = json.loads(response.get('Payload').read())
        response_code = response_payload.get('code')

        log_msg_logs = 'Tail of logs from AWS Lambda:\n{logs}'.format(logs=response_log_tail)
        log_msg_payload = 'Response payload from AWS Lambda:\n{resp}'.format(resp=response_payload)

        if response_code == 200:
            logging.info(log_msg_logs)
            logging.info(log_msg_payload)
            return response_code
        else:
            logging.error(log_msg_logs)
            logging.error(log_msg_payload)
            raise AirflowException('Lambda invoke failed')
