import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import joblib
import pandas as pd
import numpy as np
from ml.model_config import MODEL_DIR, FEATURE_COLS
from ml.preprocess import Preprocessor

class RiskPredictor:
    def __init__(self):
        self.preprocessor = Preprocessor.load()
        self.log_reg = joblib.load(os.path.join(MODEL_DIR, 'logistic_regression.joblib'))
        self.random_forest = joblib.load(os.path.join(MODEL_DIR, 'random_forest.joblib'))
        self.iso_forest = joblib.load(os.path.join(MODEL_DIR, 'isolation_forest.joblib'))

    def predict_record(self, record_dict):
        df_single = pd.DataFrame([record_dict])
        X = self.preprocessor.transform(df_single)
        
        prob_rf = float(self.random_forest.predict_proba(X)[0][1])
        prob_lr = float(self.log_reg.predict_proba(X)[0][1])
        iso_pred = int(self.iso_forest.predict(X)[0])
        iso_score = float(-self.iso_forest.decision_function(X)[0])

        risk_score_pred = round(prob_rf * 100.0, 1)
        
        if risk_score_pred <= 30.0:
            risk_class = 'LOW'
        elif risk_score_pred <= 50.0:
            risk_class = 'MODERATE'
        elif risk_score_pred <= 70.0:
            risk_class = 'HIGH'
        elif risk_score_pred <= 85.0:
            risk_class = 'VERY HIGH'
        else:
            risk_class = 'CRITICAL'

        return {
            'predicted_risk_score': risk_score_pred,
            'predicted_risk_class': risk_class,
            'rf_high_risk_probability': round(prob_rf, 4),
            'lr_high_risk_probability': round(prob_lr, 4),
            'anomaly_score': round(iso_score, 4),
            'is_abnormal_pattern': bool(iso_pred == -1),
            'model_type': 'Random Forest Prototype Classifier',
            'disclaimer': 'Prototype model prediction — decision-support signal only.'
        }
