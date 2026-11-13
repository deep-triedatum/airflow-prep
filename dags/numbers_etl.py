from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator


def extract():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def transform(numbers):
    return [n * n for n in numbers if n % 2 == 0]


def load(squares):
    print(f"Loaded {len(squares)} values: {squares}")


with DAG(
    dag_id="numbers_etl",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["etl", "example"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_numbers",
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id="square_even_numbers",
        python_callable=transform,
        op_kwargs={"numbers": extract_task.output},
    )

    load_task = PythonOperator(
        task_id="load_squares",
        python_callable=load,
        op_kwargs={"squares": transform_task.output},
    )
