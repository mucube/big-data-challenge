import pickle
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

with open("rf_spam_filtered.pkl", "rb") as f:
    search = pickle.load(f)

best_params = search.best_params_

df = pd.read_csv("../training/final_data_with_spam_only_2010_2017_2020.csv")

X = df[[
    "HarvestYear",
    "MWMT", "MCMT", "MAT", "MAP",
    "Potassium_g_kg_0-20_m", "Nitrogen_g_kg_0-20_m",
    "Phosphorus_g_kg_0-20_m", "OrganicCarbon_g_kg_0-20_m",
    'irr'
]]

y = df["YieldTonHa"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

final_rf = RandomForestRegressor(**search.best_params_)
final_rf.fit(X_train, y_train)


# Test predictions
y_pred = final_rf.predict(X_test)

# Metrics
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"Test R²: {r2:.3f}")
print(f"Test RMSE: {rmse:.3f}")