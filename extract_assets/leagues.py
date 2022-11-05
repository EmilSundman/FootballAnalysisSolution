#%% Import
import pandas as pd
from get_request import make_request
from database_commands import create_snowflake_engine, insert_query

#%% Set variables
# For retrieving data
ENDPOINT = "leagues"
params = {}

# For loading data to Snowflake
table_name = "leagues"
schema = "RAW"
if_exists_method = "replace"

#%% Define functions
def convert_to_df(json_result: dict) -> pd.DataFrame:
    list_records = []
    for each in json_result["response"]:
        dict_records = {}
        dict_records.update({"id": each["league"]["id"]})
        dict_records.update({"name": each["league"]["name"]})
        dict_records.update({"type": each["league"]["type"]})
        dict_records.update({"logomedia": each["league"]["logo"]})
        dict_records.update({"country": each["country"]["name"]})
        dict_records.update({"countrycode": each["country"]["code"]})
        dict_records.update({"countryflagmedia": each["country"]["flag"]})

        list_records.append(dict_records.copy())
    ## Create a dataframe
    df_leagues = pd.DataFrame(list_records)
    return df_leagues


#%% Send request
leagues_json = make_request(endpoint=ENDPOINT, params=params)

#%% Convert to dataframe
df_leagues = convert_to_df(leagues_json)

#%% Inspect results
print(df_leagues.head(2).to_markdown())

#%% Insert to database
engine = create_snowflake_engine()
insert_query(
    dataframe=df_leagues,
    engine=engine,
    table_name=table_name,
    schema=schema,
    if_exists_method=if_exists_method,
)

# %%
