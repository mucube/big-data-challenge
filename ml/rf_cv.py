import pandas as pd
import numpy as np

from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.ensemble import RandomForestRegressor
from sklearn.utils import resample

import pickle

df = pd.read_csv("../training/final_data.csv")

X = df[[
    "HarvestYear",
    "MWMT", "MCMT", "MAT", "MAP",
    "Potassium_g_kg_0-20_m", "Nitrogen_g_kg_0-20_m",
    "Phosphorus_g_kg_0-20_m", "OrganicCarbon_g_kg_0-20_m",
]]

y = df["YieldTonHa"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

rf = RandomForestRegressor(random_state=0)

cv_params = {'max_depth': [None, 10, 20], 
             'min_samples_leaf': [1,2,3],
             'min_samples_split': [2,5,10],
             'max_features': ["sqrt", "log2", None],
             'n_estimators': [300, 400, 500, 600]
             }

rf_cv = GridSearchCV(rf, cv_params, scoring='r2', cv=5, n_jobs=4)

rf_cv.fit(X_train,y_train)

with open("object.pkl", "wb") as f:
    pickle.dump(rf_cv, f)