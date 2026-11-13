from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

def print_greeting(user):
    print(f"Hello {user}!, Welcome to Airflow DAGs!")
    
with DAG(
    dag_id="greeting_dag",
    start_date=datetime(2026,1,1),
    schedule=None,
    catchup=False,
    tags=["greeting","example"]
) as dag:
    
    task1= PythonOperator(
        task_id="task-1",
        python_callable=print_greeting,
        op_kwargs={"user":"Developer"}
    )
