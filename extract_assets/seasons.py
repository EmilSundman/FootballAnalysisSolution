#%% Import
import pandas as pd
from get_request import make_request
from database_commands import create_snowflake_engine, insert_query

#%% Set variables
# For retrieving data
ENDPOINT = "leagues"
params = {}

# For loading data to Snowflake
table_name = "seasons"
schema = "RAW"
if_exists_method = "replace"

#%% Define functions
def convert_to_df(json_result):
    list_records = []
    for each in json_result["response"]:
        dict_records = {}
        dict_records.update({"leagueid": each["league"]["id"]})

        ## Loop through seasons
        for each_season in each["seasons"]:
            dict_records.update({"year": each_season["year"]})
            dict_records.update({"startdate": each_season["start"]})
            dict_records.update({"enddate": each_season["end"]})
            dict_records.update({"iscurrent": each_season["current"]})
            dict_records.update(
                {"fixtureevents": each_season["coverage"]["fixtures"]["events"]}
            )
            dict_records.update(
                {"fixturelineups": each_season["coverage"]["fixtures"]["lineups"]}
            )
            dict_records.update(
                {
                    "fixturestatistics": each_season["coverage"]["fixtures"][
                        "statistics_fixtures"
                    ]
                }
            )
            dict_records.update(
                {
                    "fixtureplayerstatistics": each_season["coverage"]["fixtures"][
                        "statistics_players"
                    ]
                }
            )
            dict_records.update({"standings": each_season["coverage"]["standings"]})
            dict_records.update({"players": each_season["coverage"]["players"]})
            dict_records.update({"topscorers": each_season["coverage"]["top_scorers"]})
            dict_records.update({"topassists": each_season["coverage"]["top_assists"]})
            dict_records.update({"topcards": each_season["coverage"]["top_cards"]})
            dict_records.update({"injuries": each_season["coverage"]["injuries"]})
            dict_records.update({"predictions": each_season["coverage"]["predictions"]})
            dict_records.update({"odds": each_season["coverage"]["odds"]})

            list_records.append(dict_records.copy())
    ## Create a dataframe
    df_seasons = pd.DataFrame(list_records)
    return df_seasons


#%% Send request
leagues_json = make_request(endpoint=ENDPOINT, params=params)

#%% Convert to dataframe
df_seasons = convert_to_df(leagues_json)

#%% Inspect results
print(df_seasons.head(2).to_markdown())

#%% Insert to database
engine = create_snowflake_engine()
insert_query(
    dataframe=df_seasons,
    engine=engine,
    table_name=table_name,
    schema=schema,
    if_exists_method=if_exists_method,
)

# %%
