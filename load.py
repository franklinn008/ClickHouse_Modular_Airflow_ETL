import pandas as pd

def load_csv_to_postgres(csv_file_path, table_name,engine,schema):
    '''
    Loads data from csv file  to pandas and then to a postgres DB table

    Parameters:
    - csv_file_path(str): path to csv file
    - engine (sqlalchemy.engine): an SQL Alchemy engine object
    - schema(str): a postgre DB Schema

    '''
    df = pd.read_csv(csv_file_path)
    df.to_sql(table_name,con=engine, if_exists= 'replace', index=False, schema=schema)

    print(f'{len(df)} rows successfully loaded to the postgres DB')