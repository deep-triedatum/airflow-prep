from datetime import datetime, timedelta
import time

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args={
    "email" : ["deep.senchowa@triedatum.com"]
}

def slow_job():
    time.sleep(60)
    print("Slow job complete!")

def sla_miss_alart(dag, task_list):
    print(f"SLA missed in {dag.dag_id}: {task_list}")

with DAG(
    dag_id="sla_miss_alart_v1",
    start_date=datetime(2026,1,1),
    schedule="*/5 * * * *",
    sla_miss_callback=sla_miss_alart,
    default_args=default_args,
    catchup=False    
) as dag:
    task1= PythonOperator(
        task_id="slow_job",
        python_callable=slow_job,
        sla=timedelta(seconds=30) 
    )
