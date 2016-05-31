from airflow.configuration import conf

from datetime import timedelta, datetime

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
