import sqlalchemy
from sqlalchemy import create_engine
import clickhouse_connect
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

def get_snowflake_engine():
    '''
    Construct a SQLAlchemy engine object for a Snowflake DB from environment variables.

    Parameters:
        None

    Returns:
        sqlalchemy.engine.Engine: The SQLAlchemy engine object.
    '''
    engine = create_engine(
        "snowflake://{user}:{password}@{account_identifier}/{database}/{schema}?warehouse={warehouse}".format(
            user=os.getenv('sn_user'),
            password=os.getenv('sn_password'),
            account_identifier=os.getenv('sn_account_identifier'),
            database=os.getenv('sn_database'),
            schema=os.getenv('sn_schema'),
            warehouse=os.getenv('sn_warehouse')
        )
    )
    return engine


