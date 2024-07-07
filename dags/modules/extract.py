import pandas as pd
from datetime import datetime,timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

#function to get data
def fetch_data(client,engine):
     '''
    fetches query results from clickhouse database and writes to a csv file
    
    parameters: 
    -clickhouse_connect.client
    -query (A SQL select query)
    
    Returns: None
    '''
     
     #executing stored procedure
     session = sessionmaker(bind=engine)
     session = session()
     result= session.execute('select max(pickup_date) from "STG".tripdata')
     max_date = result.fetchone()[0]
     session.close()

     ##getting the new date
     new_date = (datetime.strptime(max_date,'%Y-%m-%d') + timedelta(days=1)).date()
     print(max_date)

     #query to execute
     query = f'''
        select pickup_date,vendor_id,passenger_count, trip_distance,payment_type, fare_amount, tip_amount 
        from tripdata
        where pickup_date = toDate('{max_date}') + 1
        '''
     
     #execute the query
     output = client.query(query)
     rows = output.result_rows
     cols = output.column_names

     #close the cient
     client.close()

     #write to pandas df and csv
     df = pd.DataFrame(rows,columns=cols)
     df.to_csv('./dags/modules/raw_files/tripdata.csv', index=False)

     print(f'{len(df)} rows successfully extracted for {new_date} ')

    