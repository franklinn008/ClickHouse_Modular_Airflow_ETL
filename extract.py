import pandas as pd

#function to get data
def fetch_data(client, query):
     '''
    fetches query results from clickhouse database and writes to a csv file
    
    parameters: 
    -clickhouse_connect.client
    -query (A SQL select query)
    
    Returns: None
    '''
     
     #execute the query
     result = client.query(query)
     rows = result.result_rows
     cols = result.column_names

     #close the cient
     client.close()

     #write to pandas df and csv
     df = pd.DataFrame(rows,columns=cols)
     df.to_csv('tripdata.csv', index=False)

     print(f'{len(df)} rows successfully extracted')