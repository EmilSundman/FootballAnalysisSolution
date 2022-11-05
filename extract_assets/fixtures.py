#%% Import
import pandas as pd
from get_request import make_request
from database_commands import create_snowflake_engine, insert_query

#%% Set variables
# For retrieving data
ENDPOINT = "fixtures"
leagues_to_load = [
    "39",  # Premier League
    # "61",  # Ligue 1
    # "78",  # Bundesliga
]
seasons_to_load = ["2022"]
params = {}

# For loading data to Snowflake
table_name = "fixtures"
schema = "RAW"
if_exists_method = "replace"

#%% Define functions
def convert_to_df(json_result):
    list_records = []
    for each in json_result["response"]:
        dict_records = {}
        dict_records.update({"Id": each["fixture"]["id"]})
        dict_records.update({"Referee": each["fixture"]["referee"]})
        dict_records.update({"DateTimeUTC": each["fixture"]["date"]})
        dict_records.update({"VenueId": each["fixture"]["venue"]["id"]})
        dict_records.update({"VenueName": each["fixture"]["venue"]["name"]})
        dict_records.update({"VenueCity": each["fixture"]["venue"]["city"]})
        dict_records.update({"LeagueId": each["league"]["id"]})
        dict_records.update({"LeagueName": each["league"]["name"]})
        dict_records.update({"LeagueCountry": each["league"]["country"]})
        dict_records.update({"LeagueLogoMedia": each["league"]["logo"]})
        dict_records.update({"LeagueFlagMedia": each["league"]["flag"]})
        dict_records.update({"Season": each["league"]["season"]})
        dict_records.update({"Round": each["league"]["round"]})
        dict_records.update({"HomeTeamId": each["teams"]["home"]["id"]})
        dict_records.update({"HomeTeamName": each["teams"]["home"]["name"]})
        dict_records.update({"HomeTeamLogo": each["teams"]["home"]["logo"]})
        dict_records.update({"HomeTeamGoals": each["goals"]["home"]})
        dict_records.update({"AwayTeamId": each["teams"]["away"]["id"]})
        dict_records.update({"AwayTeamName": each["teams"]["away"]["name"]})
        dict_records.update({"AwayTeamLogo": each["teams"]["away"]["logo"]})
        dict_records.update({"AwayTeamGoals": each["goals"]["away"]})
        dict_records.update({"MatchStatus": each["fixture"]["status"]["short"]})
        dict_records.update({"Elapsed": each["fixture"]["status"]["elapsed"]})

        list_records.append(dict_records.copy())
    ## Create a dataframe
    df_fixtures = pd.DataFrame(list_records)
    return df_fixtures


#%% Send request
# Loop through leagues and seasons
for leagueId in leagues_to_load:
    for season in seasons_to_load:
        params = {"league": leagueId, "season": season}
        fixtures_json = make_request(endpoint=ENDPOINT, params=params)
        df_fixtures = convert_to_df(fixtures_json)
        engine = create_snowflake_engine()
        insert_query(
            dataframe=df_fixtures,
            engine=engine,
            table_name=table_name,
            schema=schema,
            if_exists_method=if_exists_method,
        )


#%% Convert to dataframe
# df_fixtures = convert_to_df(fixtures_json)

# #%% Inspect results
# print(df_fixtures.head(2).to_markdown())

# #%% Insert to database
# engine = create_snowflake_engine()
# insert_query(
#     dataframe=df_fixtures,
#     engine=engine,
#     table_name=table_name,
#     schema=schema,
#     if_exists_method=if_exists_method,
# )

# %%
