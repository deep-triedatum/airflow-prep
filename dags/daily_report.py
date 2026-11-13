from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def build_report(run_date):
    print(f"Daily report for {run_date}: all systems OK")


with DAG(
    dag_id="daily_report",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["report", "example"]
) as dag:

    check_disk = BashOperator(
        task_id="check_disk",
        bash_command="df -h / | tail -1"
    )

    report = PythonOperator(
        task_id="build_report",
        python_callable=build_report,
        op_kwargs={"run_date": "{{ ds }}"}
    )

    done = BashOperator(
        task_id="notify_done",
        bash_command="echo 'Report finished for {{ ds }}'"
    )

    check_disk >> report >> done
