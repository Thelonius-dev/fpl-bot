
import pandas as pd

# Load current-season data
history_df = pd.read_csv(
    r"E:/Visual Code/FPL/fpl_history.csv"
)

# Historical seasons to download
seasons = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]

historical_data = []

for season in seasons:
    print(f"Downloading {season}...")

    url = (
        "https://raw.githubusercontent.com/vaastav/"
        f"Fantasy-Premier-League/master/data/{season}/gws/merged_gw.csv"
    )

    season_df = pd.read_csv(url)
    season_df["season"] = season
    historical_data.append(season_df)

# Combine all seasons
historical_df = pd.concat(historical_data, ignore_index=True)

# Remove unnecessary or duplicate columns
columns_to_drop = [
    "GW",
    "xP",
    "mng_clean_sheets",
    "mng_draw",
    "mng_goals_scored",
    "mng_loss",
    "mng_underdog_draw",
    "mng_underdog_win",
    "mng_win",
]

historical_df = historical_df.drop(
    columns=columns_to_drop,
    errors="ignore"
)

# Save cleaned historical data
historical_df.to_csv(
    r"E:/Visual Code/FPL/fpl_historical_cleaned.csv",
    index=False
)

# Confirm everything worked
print("\nCurrent season shape:", history_df.shape)
print("Historical data shape:", historical_df.shape)
print("\nRows per season:")
print(historical_df["season"].value_counts().sort_index())
print("\nSaved cleaned historical data successfully!")
