from helpers import get_client
from helpers import get_postgres_engine
from extract import fetch_data
from load import load_csv_to_postgres

client = get_client()
query = 'select * from tripdata limit 10'
engine = get_postgres_engine() 

fetch_data(client=client,query=query)
load_csv_to_postgres('tripdata.csv','tripdata',engine,'STG')

