from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.task_group import TaskGroup

from dotenv import load_dotenv
from modules.extract import fetch_data
from modules.load import load_csv_to_snowflake, exec_procedure
from modules.helpers import get_client, get_snowflake_engine

#getting client and engine
engine = get_snowflake_engine()
client = get_client()

#adding arguments
default_args = {
    'owner': 'Ifeanyi_DArTech_Org',
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
    'clickhouse_etl_dag',
    default_args = default_args,
    description = 'This is a pipeline to move clickhouse tripdata to snowflakes',
    schedule_interval='0 0 * * *',  # Check crontab.guru
    catchup= False
) as dag:
    
    #define starting start 1
    start_task = DummyOperator(
        task_id = 'Start_Pipeline'
    )


    #define extracting task 1
    extract_task = PythonOperator(
        task_id  = 'extract',
        python_callable= fetch_data,
        op_kwargs = {'client':client , 'engine': engine}
    )


    #define loading to staging task 2
    with TaskGroup (group_id = 'loading_task') as loadtasks:
        staging_load_task = PythonOperator(
            task_id  = 'stg_load',
            python_callable= load_csv_to_snowflake,
            op_kwargs = {'table_name':'tripdata' , 'engine': engine, 'schema':'STG'}
        )
        
        #define loading to production task 3
        prodload_task = PythonOperator(
            task_id  = 'edw_load',
            python_callable= exec_procedure,
            op_kwargs = {'engine': engine}
        )
        staging_load_task>>prodload_task

    #define ending end 2
    end_task  = DummyOperator(
        task_id = 'end_pipeline'
    )


#setting dependencies
start_task>> extract_task >>loadtasks>> end_task 