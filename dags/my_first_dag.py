from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy_operator import DummyOperator




#adding arguments
default_args = {
    'owner': 'DArTech',
    'depends_on_past': False,
    'start_date': datetime(year=2024,month=7,day=7),
    'email':'franklinnwosu008@gmail.com',
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': None,
    'retry_delay': timedelta(minutes=1)
   
}

#Instantiate DAG
with DAG(
    'my_first_dag',
    default_args = default_args,
    description = 'This is a demo dag for learning',
    schedule_interval='* 2 * * *',  # Check crontab.guru
    catchup= False
) as dag:
    
    #define task 1
    start_task = DummyOperator(
        task_id = 'Start_Pipeline'
    )



    #define task 3
    end_task  = DummyOperator(
        task_id = 'end_pipeline'
    )


#setting dependencies
start_task >> end_task 