import pandas as pd
from datetime import datetime,timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


def load_csv_to_snowflake( table_name,engine,schema):
    '''
    Loads data from csv file  to pandas and then to a postgres DB table

    Parameters:
    - engine (sqlalchemy.engine): an SQL Alchemy engine object
    - schema(str): a postgre DB Schema

    '''
    df = pd.read_csv('./dags/modules/raw_files/tripdata.csv')
    df.to_sql(table_name,con=engine, if_exists= 'replace', index=False, schema=schema)

    print(f'{len(df)} rows successfully loaded to the postgres DB')

def exec_procedure(engine):
     #executing stored procedure
    session= sessionmaker(bind=engine)
    session = session()
    session.execute('call "STG".agg_trip_data()')
    session.commit()

    print('Stored Procedure executed successfully')
