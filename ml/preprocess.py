import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import joblib
import os
from ml.model_config import FEATURE_COLS, MODEL_DIR

class Preprocessor:
    def __init__(self):
        self.imputer = SimpleImputer(strategy='median')
        self.scaler = StandardScaler()
        self.is_fitted = False

    def fit_transform(self, df):
        df_feat = df[FEATURE_COLS].copy()
        X_imp = self.imputer.fit_transform(df_feat)
        X_scaled = self.scaler.fit_transform(X_imp)
        self.is_fitted = True
        return X_scaled

    def transform(self, df):
        df_feat = df[FEATURE_COLS].copy()
        X_imp = self.imputer.transform(df_feat)
        X_scaled = self.scaler.transform(X_imp)
        return X_scaled

    def save(self, filepath=None):
        if filepath is None:
            filepath = os.path.join(MODEL_DIR, 'preprocessor.joblib')
        joblib.dump(self, filepath)

    @staticmethod
    def load(filepath=None):
        if filepath is None:
            filepath = os.path.join(MODEL_DIR, 'preprocessor.joblib')
        return joblib.load(filepath)
