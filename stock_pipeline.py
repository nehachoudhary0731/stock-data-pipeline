from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append("/opt/airflow/scripts")
from fetch_stock_data import fetch_and_store_stock_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'stock_data_pipeline',
    default_args=default_args,
    description='Fetch and store stock data',
    schedule_interval='@hourly',
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    fetch_and_store = PythonOperator(
        task_id='fetch_and_store_stock_data',
        python_callable=fetch_and_store_stock_data,
    )

    fetch_and_store