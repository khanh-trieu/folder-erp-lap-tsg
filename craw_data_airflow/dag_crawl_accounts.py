from datetime import timedelta
from textwrap import dedent
from airflow.models import Variable
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
from datetime import datetime, timedelta, timezone
# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['khanh.trieu@tsg.net.vn'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'start_date':days_ago(2),
    # 'retry_delay': timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
with DAG(
        'dag_crawl_accounts_2',
        default_args=default_args,
        description='Crawl company to cổng thông tin doanh nghiệp!',
        schedule_interval=Variable.get("schedule_interval_crwal_accounts"),
        tags=['crawl company'],

) as dag:
    dag.doc_md = __doc__
    templated_command = dedent(
        '''
         '''
    )
    t1 = BashOperator(
        task_id='templated',
        depends_on_past=False,
        bash_command=Variable.get("command_run_api_crawl_account"),
        params={'my_param': 'param có thể sử dụng'},
    )
