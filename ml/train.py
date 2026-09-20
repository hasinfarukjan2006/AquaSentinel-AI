import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from ml.model_config import (
    DATA_DIR, MODEL_DIR, FEATURE_COLS, TARGET_COL,
    LOGISTIC_PARAMS, RANDOM_FOREST_PARAMS, ISOLATION_FOREST_PARAMS
)
from ml.preprocess import Preprocessor
from ml.features import prepare_ml_features

def train_models():
    demo_path = os.path.join(DATA_DIR, 'JalRakshak_Synthetic_Demo_Dataset.csv')
    real_path = os.path.join(DATA_DIR, 'JalRakshak_Integrated_Dataset.csv')

    if os.path.exists(demo_path):
        df_demo = pd.read_csv(demo_path)
    else:
        raise FileNotFoundError("Synthetic demo dataset not found for training!")

    df_prepared = prepare_ml_features(df_demo)

    preprocessor = Preprocessor()
    X = preprocessor.fit_transform(df_prepared)
    y = df_prepared['is_high_risk'].values
    preprocessor.save()

    # 1. Logistic Regression Baseline
    log_reg = LogisticRegression(**LOGISTIC_PARAMS)
    log_reg.fit(X, y)
    joblib.dump(log_reg, os.path.join(MODEL_DIR, 'logistic_regression.joblib'))
    print("Trained Logistic Regression baseline model.")

    # 2. Random Forest Classifier
    rf_clf = RandomForestClassifier(**RANDOM_FOREST_PARAMS)
    rf_clf.fit(X, y)
    joblib.dump(rf_clf, os.path.join(MODEL_DIR, 'random_forest.joblib'))
    print("Trained Random Forest classification model.")

    # 3. Isolation Forest Anomaly Detector
    iso_forest = IsolationForest(**ISOLATION_FOREST_PARAMS)
    iso_forest.fit(X)
    joblib.dump(iso_forest, os.path.join(MODEL_DIR, 'isolation_forest.joblib'))
    print("Trained Isolation Forest anomaly detection model.")

if __name__ == '__main__':
    train_models()
