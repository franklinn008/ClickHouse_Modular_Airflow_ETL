import sqlalchemy
import clickhouse_connect
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(override=True)

def get_client():
    '''
    Connect to the ClickHouse database using parameters from a .env file.

    Parameters:
        None

    Returns:
        clickhouse_connect.Client: A database client object.
    '''
    # Getting credentials
    host = os.getenv('ch_host')
    port = os.getenv('ch_port')
    user = os.getenv('ch_user')
    password = os.getenv('ch_password')

    # Connect to the database
    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=user,
        password=password,
        secure=True
    )

    return client

def get_postgres_engine():
    '''
    Construct a SQLAlchemy engine object for a PostgreSQL DB from environment variables.

    Parameters:
        None

    Returns:
        sqlalchemy.engine.Engine: The SQLAlchemy engine object.
    '''
    engine = create_engine(
        "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}".format(
            user=os.getenv('pg_user'),
            password=os.getenv('pg_password'),
            host=os.getenv('pg_host'),
            port=os.getenv('pg_port'),
            dbname=os.getenv('pg_dbname')
        )
    )
    return engine

# Example usage
#if __name__ == "__main__":
    #engine = get_postgres_engine()
    #print("PostgreSQL engine created:", engine)
    #client = get_client()
    #print("ClickHouse client created:", client)
