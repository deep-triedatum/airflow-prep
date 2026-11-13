
from datetime import datetime, timedelta
import time

from airflow.sdk import DAG, task
from airflow.sdk.definitions.callback import AsyncCallback
from airflow.sdk.definitions.deadline import DeadlineAlert, DeadlineReference
from plugins.deadline_alerts import send_deadline_email
from airflow.providers.standard.operators.python import PythonOperator

ALERT_EMAIL = ["deep.senchowa@triedatum.com"]



with DAG(
    dag_id="sla_miss_alart_v1",
    start_date=datetime(2026, 1, 1),
    schedule="*/5 * * * *",
    catchup=False,
    deadline=DeadlineAlert(
        reference=DeadlineReference.DAGRUN_QUEUED_AT,   # clock starts when the run is queued
        interval=timedelta(seconds=30),
        callback=AsyncCallback(
            send_deadline_email,
            kwargs={
                "to": ALERT_EMAIL,
                "subject": "[airflow] Deadline missed: {dag_id}",
                "html_content": "Run <b>{run_id}</b> of <b>{dag_id}</b> did not finish within its deadline.",
            },
        ),
    ),
) as dag:
    @task(
        task_id="slow_task",
    )
    def slow_job():
        time.sleep(60)
        print("Slow job complete!")
    
    slow_job()