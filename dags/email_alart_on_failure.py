from datetime import datetime, timedelta

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator


default_args = {
    "owner": "airflow v3",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "email": ["deep.senchowa@triedatum.com"],
    "email_on_failure": True,
    "email_on_retry": True,
}

with DAG(
    dag_id="email_alert_on_failure",
    start_date=datetime(2026, 1, 1),
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    max_active_runs=1,          
) as dag:

    task1 = BashOperator(
        task_id="task1",
        bash_command="echo 'Task 1 completed successfully!'",
    )

    task2 = BashOperator(
        task_id="task2",
        bash_command="ls /nonexistent", 
    )

    task3 = BashOperator(
        task_id="task3",
        bash_command="echo 'Task 3 completed successfully!'",
    )

    task1 >> task2 >> task3
