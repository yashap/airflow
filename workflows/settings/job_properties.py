from airflow.configuration import conf

from datetime import timedelta, datetime
import json

def days_ago(days):
    now = datetime.now() - timedelta(days=days)
    return datetime(now.year, now.month, now.day)

def split_and_trim(value):
    return [s.strip() for s in value.split(',') if s.strip()]

DAG_START = datetime(2016, 2, 22)
S3_BUCKET = 'sodp'
S3_PREFIX = 'talk'

DEFAULT_ARGS = {
    'owner': 'airflow',
    'depends_on_past': True,
    'email': split_and_trim(conf.get('app_specific', 'email_to')),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(seconds=10),
    'poke_interval': 30,
}

def context_to_datepart(context):
    """
    Creates a partial S3 path based on an Airflow job context

    :param context: a dictionary with details about the job run, where 'tomorrow_ds' is a string holding the day after
                    the job run, in YYYY-MM-DD format
    :return: a partial S3 path
    """
    return context['tomorrow_ds'].replace('-', '/')


def context_to_payload(context):
    """
    Creates a payload used to run an AWS Lambda function, based on an Airflow job context

    :param context: a dictionary with details about the job run, where 'ds' is a string holding the day of the job run,
                    in YYYY-MM-DD format
    :return: a payload used to run an AWS Lambda function
    """
    return json.dumps({'runDate': context['ds']})
