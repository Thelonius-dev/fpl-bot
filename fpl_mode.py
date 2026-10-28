
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder

# 1. Load saved data — no downloads
history_df = pd.read_csv(r"E:/Visual Code/FPL/fpl_history.csv")
historical_df = pd.read_csv(r"E:/Visual Code/FPL/fpl_historical_cleaned.csv")

# 2. Sort historical matches
historical_df["kickoff_time"] = pd.to_datetime(
    historical_df["kickoff_time"], errors="coerce"
)
history_df["kickoff_time"] = pd.to_datetime(
    history_df["kickoff_time"], errors="coerce"
)

historical_df = historical_df.sort_values(
    ["season", "element", "kickoff_time"]
).copy()

# 3. Create features using only earlier matches
group = historical_df.groupby(["season", "element"])

for stat in [
    "total_points", "minutes", "goals_scored",
    "assists", "bonus", "clean_sheets", "saves"
]:
    historical_df[f"previous_{stat}_avg"] = group[stat].transform(
        lambda s: s.shift(1).expanding().mean()
    )

features = [
    "previous_total_points_avg",
    "previous_minutes_avg",
    "previous_goals_scored_avg",
    "previous_assists_avg",
    "previous_bonus_avg",
    "previous_clean_sheets_avg",
    "previous_saves_avg",
    "value",
    "was_home",
    "position",
    "opponent_team",
    "round",
]

target = "total_points"

# 4. Prepare data and remove rows without previous history
data = historical_df.dropna(
    subset=features + [target, "kickoff_time"]
).copy()

# Encode categorical columns consistently
position_encoder = LabelEncoder()
team_encoder = LabelEncoder()

data["position"] = position_encoder.fit_transform(
    data["position"].astype(str)
)
data["opponent_team"] = team_encoder.fit_transform(
    data["opponent_team"].astype(str)
)

# 5. Split by time: train on earlier seasons, test on 2025/26
train = data[data["season"] != "2025-26"].copy()
test = data[data["season"] == "2025-26"].copy()

X_train = train[features]
y_train = train[target]
X_test = test[features]
y_test = test[target]

# 6. Train model
model = RandomForestRegressor(
    n_estimators=100,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# 7. Evaluate on the held-out season
predictions = model.predict(X_test)

print("\n--- MODEL EVALUATION ---")
print("Training rows:", len(train))
print("Test rows:", len(test))
print("Mean absolute error:", round(mean_absolute_error(y_test, predictions), 3))

# 8. Show which features matter most
importance = pd.Series(
    model.feature_importances_, index=features
).sort_values(ascending=False)

print("\n--- FEATURE IMPORTANCE ---")
print(importance.round(3))

print("\nModel trained and evaluated successfully.")
