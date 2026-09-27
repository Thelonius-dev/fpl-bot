import requests
import pandas as pd

history_df = pd.read_csv(r"E:/Visual Code/FPL/fpl_history.csv")

print(history_df.shape)

#so rn we have the 26/27 seasons data, now for the previous season (we can get rid of all the ugly code cuz we now just read the csv file)

seasons = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]

historical_data = []

for season in seasons:

    url = f"https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/{season}/gws/merged_gw.csv"

    season_data = pd.read_csv(url)

    historical_data.append(season_data)

  #  print(season, season_data.shape)

historical_df = pd.concat(historical_data, ignore_index=True)

print(historical_df.shape)

historical_df.to_csv("fpl_historical.csv", index=False)

