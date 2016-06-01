from settings.job_properties import *
from operators.lambda_operator import LambdaOperator
from operators.s3_sensor import S3DatepartSensor
from airflow import DAG

from datetime import timedelta


# DAG
daily_etls = DAG(
    dag_id='daily_etls',
    schedule_interval=timedelta(days=1),
    concurrency=4,
    start_date=DAG_START,
    default_args=DEFAULT_ARGS
)


# Nodes
s3_sensor = S3DatepartSensor(
    task_id='s3_sensor',
    context_to_datepart=context_to_datepart,
    s3_bucket=S3_BUCKET,
    s3_prefix=S3_PREFIX,
    dag=daily_etls
)

etl_load_events = LambdaOperator(
    task_id='etl_load_events',
    context_to_payload=context_to_payload,
    lambda_function_name='etl-load-events',
    dag=daily_etls
)

etl_organization_stats = LambdaOperator(
    task_id='etl_organization_stats',
    context_to_payload=context_to_payload,
    lambda_function_name='etl-organization-stats',
    dag=daily_etls
)


# Edges
etl_load_events.set_upstream(s3_sensor)
etl_organization_stats.set_upstream(etl_load_events)
