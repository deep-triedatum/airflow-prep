from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow v2",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "email": ["deepsenchowa1@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": True,
    "max_active_runs": 1,
}

with DAG(
    dag_id="email_alert_on_failure",
    start_date= datetime(2026, 1, 1),
    default_args=default_args,
    schedule= "@daily",
    catchup=False
) as dag:
    
    task1 = BashOperator(
        task_id="task1",
        bash_command="echo 'Task 1 completed successfully!'"
    )

    task2 = BashOperator(
        task_id="task2",
        bash_command="ls /nonexistent"  # This command will fail
    )

    task3 = BashOperator(
        task_id="task3",
        bash_command="echo 'Task 3 completed successfully!'"
    )

    task1 >> task2 >> task3