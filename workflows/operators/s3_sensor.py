from airflow.operators.sensors import BaseSensorOperator
from airflow.utils import apply_defaults
import boto3


class S3DatepartSensor(BaseSensorOperator):

    @apply_defaults
    def __init__(self, context_to_datepart, s3_bucket, s3_prefix, *args, **kwargs):
        super(S3DatepartSensor, self).__init__(*args, **kwargs)
        self.context_to_datepart = context_to_datepart
        self.s3_bucket = s3_bucket
        self.s3_prefix = s3_prefix
        self.s3_client = boto3.client('s3')

    def poke(self, context):
        datepart = self.context_to_datepart(context)
        prefix_to_check = '{prefix}/{datepart}'.format(
            prefix=self.s3_prefix,
            datepart=datepart
        )

        s3_objects = self.s3_client.list_objects(Bucket=self.s3_bucket, Prefix=prefix_to_check)

        return True if s3_objects.get('Contents') else False
