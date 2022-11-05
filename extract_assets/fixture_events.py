#%% Import
import pandas as pd
import time
from get_request import make_request
from database_commands import create_snowflake_engine, insert_query, select_query

#%% Set variables
# For retrieving data
ENDPOINT = "fixtures/events"
leagues_to_load = [
    "39",  # Premier League
    # "61",  # Ligue 1
    # "78",  # Bundesliga
]
seasons_to_load = ["2022"]
params = {}
match_status = "FT"
seconds_between_requests = 2.1
# For loading data to Snowflake
table_name = "fixtureevents"
schema = "RAW"
if_exists_method = "append"

#%% Define functions
def convert_to_df(json_result):
    list_records = []
    for element in json_result:
        fixture_id = element["parameters"]["fixture"]
        for each in element["response"]:
            dict_records = {}
            dict_records.update({"fixtureid": fixture_id})
            dict_records.update({"teamid": each["team"]["id"]})
            dict_records.update({"type": each["type"]})
            dict_records.update({"detail": each["detail"]})
            dict_records.update({"comments": each["comments"]})
            dict_records.update({"minute": each["time"]["elapsed"]})
            dict_records.update({"timeextra": each["time"]["extra"]})
            dict_records.update({"mainplayerid": each["player"]["id"]})
            dict_records.update({"secondaryplayerid": each["assist"]["id"]})

            list_records.append(dict_records.copy())
    ## Create a dataframe
    df_fixture_events = pd.DataFrame(list_records)
    return df_fixture_events


#%% Query for fixtureIds
leagues = ",".join(leagues_to_load)
seasons = ",".join(seasons_to_load)
query_get_fixtures = f"""
select distinct id as fixtureid 
from FOOTBALL.RAW.fixtures 
where leagueid in ({leagues}) and season in ({seasons}) and matchstatus = '{match_status}'
and id not in (select fixtureid from FOOTBALL.RAW.{table_name})"""
df_fixture_to_get = select_query(
    query=query_get_fixtures,
    engine=create_snowflake_engine(),
)

#%% See FixtureId dataframe
print(df_fixture_to_get.head(5).to_markdown())

#%% Send request
# Loop through fixtures
fixtures_json = []
for index, row in df_fixture_to_get.iterrows():
    params = {"fixture": row["fixtureid"]}
    req_json = make_request(endpoint=ENDPOINT, params=params)
    if req_json:
        fixtures_json.append(req_json.copy())
    print(f"{index+1}/{df_fixture_to_get.shape[0]} processed")
    time.sleep(seconds_between_requests)
df_fixture_events = convert_to_df(fixtures_json)
engine = create_snowflake_engine()
insert_query(
    dataframe=df_fixture_events,
    engine=engine,
    table_name=table_name,
    schema=schema,
    if_exists_method=if_exists_method,
)


#%%
engine = create_snowflake_engine()
insert_query(
    dataframe=df_fixture_events,
    engine=engine,
    table_name=table_name,
    schema=schema,
    if_exists_method=if_exists_method,
)
