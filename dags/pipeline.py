import sys
sys.path.insert(0, '/mnt/c/Users/27533/Desktop/job_warehouse')

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from load_obs import load_ods
from transform_dwd import transform_dwd
from transform_dws import transform_dws
from transform_ads import transform_ads

with DAG(
    dag_id='job_warehouse_pipeline',
    start_date=datetime(2026, 6, 1),
    schedule='@daily',
    catchup=False,
) as dag:

    t1 = PythonOperator(task_id='load_ods',       python_callable=load_ods)
    t2 = PythonOperator(task_id='transform_dwd',  python_callable=transform_dwd)
    t3 = PythonOperator(task_id='transform_dws',  python_callable=transform_dws)
    t4 = PythonOperator(task_id='transform_ads',  python_callable=transform_ads)

    t1 >> t2 >> t3 >> t4
