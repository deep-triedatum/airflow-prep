from datetime import datetime

from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.operators.python import PythonOperator

def process_response(response):
    list_of_users = []
    for user in response["users"]:
        new_user = {
            "id": user.get("id"),
            "name": " ".join(filter(None,[user.get("firstName"), user.get("maidenName"), user.get("lastName")])),
            "email": user.get("email")
        }
        list_of_users.append(new_user)
    
    return list_of_users


with DAG(
    dag_id = "get_users",
    start_date=datetime(2026,1,1),
    schedule=None,
    catchup=False,
    tags=["api","users","example"]    
) as dag:
        
    call_api = HttpOperator(
        task_id= "get_users",
        method= "GET",
        http_conn_id= "user_api_conn",
        endpoint= "/users",
        response_filter=lambda response: response.json(),
        response_check=lambda response: response.status_code == 200,
        log_response=True
    )
    
    list_users = PythonOperator(
        task_id="filter_users",
        python_callable=process_response,
        op_kwargs={"response": call_api.output},
        show_return_value_in_logs=True
    )
    
    
    