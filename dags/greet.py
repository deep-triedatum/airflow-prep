from datetime import datetime

from airflow.decorators import dag, task
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator





with DAG(
    dag_id="greeting_dag",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    @task(
        task_id="print_greeting",
    )
    def print_greeting(user):
        print(f"Hello {user}!, Welcome to Airflow DAGs!")
    
    print_greeting("Developer")