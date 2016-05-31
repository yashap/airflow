from settings.job_properties import *
from operators.lambda_operator import LambdaOperator
from operators.s3_sensor import S3TimestampedSensor
from airflow import DAG

from datetime import timedelta, datetime


# DAG
daily_etls = DAG(
    dag_id='daily_etls',
    schedule_interval=timedelta(days=1),
    concurrency=4,
    # start_date=datetime(2016, 2, 22),
    start_date=DAG_START,
    default_args=DEFAULT_ARGS
)

# Nodes
s3_sensor = S3TimestampedSensor(
    task_id='s3_sensor',
    s3_bucket=S3_BUCKET,
    s3_prefix=S3_PREFIX,
    dag=daily_etls
)

etl_load_events = LambdaOperator(
    task_id='etl_load_events',
    lambda_function_name='etl-load-events',
    dag=daily_etls
)

etl_organization_stats = LambdaOperator(
    task_id='etl_organization_stats',
    lambda_function_name='etl-organization-stats',
    dag=daily_etls
)

# Edges
etl_load_events.set_upstream(s3_sensor)
etl_organization_stats.set_upstream(etl_load_events)
