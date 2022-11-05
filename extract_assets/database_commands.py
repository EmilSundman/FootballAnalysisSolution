# %% import libs
import os
import pandas as pd
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

user = os.getenv("SNOWFLAKE_USER")
password = os.getenv("SNOWFLAKE_PASSWORD")
account = os.getenv("SNOWFLAKE_ACCOUNT")
warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
database = "FOOTBALL"


def create_snowflake_engine():
    connect = create_engine(
        URL(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            schema="RAW",
        )
    )

    engine = connect.connect()
    return engine


def insert_query(
    dataframe: pd.DataFrame, engine, table_name: str, schema: str, if_exists_method: str
) -> str:
    # Create a connection
    # conn = engine.connect()

    dataframe.columns = dataframe.columns.str.replace("%", "percentage")
    dataframe.columns = dataframe.columns.str.replace(" ", "")
    dataframe.columns = dataframe.columns.str.upper()

    # Converting all columns to lower case for consistent handling in snowflake
    # Perform query and return results
    dataframe.to_sql(
        table_name, engine, schema, if_exists=if_exists_method, index=False
    )

    records_dataframe = dataframe.shape[0]

    records_inserted = pd.read_sql(
        f"SELECT count(*) FROM {schema}.{table_name}", engine
    ).iat[0, 0]
    # Close connection
    # conn.close()

    Output = f"""Dataframe contained {records_dataframe} records. {records_inserted} have been inserted. 
    """
    return Output


def select_query(query, engine):
    # Create a connection
    conn = engine.connect()
    # Perform query and return results
    df_result = pd.read_sql(query, conn)
    # Close connection
    conn.close()
    return df_result


#%%
