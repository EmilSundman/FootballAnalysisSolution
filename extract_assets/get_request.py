# %% import libs
import requests
import os

#%% define variables
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"
HEADERS = {
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
    "X-RapidAPI-Key": os.getenv("API-FOOTBALL-KEY"),
}


# call API to retrieve data and return JSON-response
def make_request(endpoint: str, params: dict) -> dict:
    """
    Send requests to a given endpoint and a set of parameters.
    """
    url = f"{BASE_URL}/{endpoint}"
    print(url)
    response = requests.request(
        "GET",
        url,
        headers=HEADERS,
        params=params,
    )
    response_json = response.json()
    if response.status_code != 200:
        print(f"{response.status_code}. For parameter: {params}")
        return
    elif len(response_json["response"]) == 0:
        print(f"Empty response. For parameter: {params}")
        return
    else:
        return response_json
