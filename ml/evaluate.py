import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import (
    precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
)
from ml.model_config import DATA_DIR, MODEL_DIR, REPORT_DIR
from ml.preprocess import Preprocessor
from ml.features import prepare_ml_features

def evaluate_models():
    demo_path = os.path.join(DATA_DIR, 'JalRakshak_Synthetic_Demo_Dataset.csv')
    real_path = os.path.join(DATA_DIR, 'JalRakshak_Integrated_Dataset.csv')

    df_demo = pd.read_csv(demo_path) if os.path.exists(demo_path) else pd.DataFrame()
    df_real = pd.read_csv(real_path) if os.path.exists(real_path) else pd.DataFrame()

    preprocessor = Preprocessor.load()
    rf_clf = joblib.load(os.path.join(MODEL_DIR, 'random_forest.joblib'))
    lr_clf = joblib.load(os.path.join(MODEL_DIR, 'logistic_regression.joblib'))

    eval_results = {}
    csv_rows = []

    # 1. Evaluation on Synthetic Demo Dataset
    if not df_demo.empty:
        df_demo_prep = prepare_ml_features(df_demo)
        X_demo = preprocessor.transform(df_demo_prep)
        y_demo = df_demo_prep['is_high_risk'].values

        y_pred_rf = rf_clf.predict(X_demo)
        y_prob_rf = rf_clf.predict_proba(X_demo)[:, 1]

        y_pred_lr = lr_clf.predict(X_demo)
        y_prob_lr = lr_clf.predict_proba(X_demo)[:, 1]

        cm_rf = confusion_matrix(y_demo, y_pred_rf).tolist()
        cm_lr = confusion_matrix(y_demo, y_pred_lr).tolist()

        eval_results['Synthetic_Demo_Dataset_Evaluation'] = {
            'dataset': 'Synthetic Demo Dataset',
            'sample_count': len(y_demo),
            'high_risk_positive_samples': int(y_demo.sum()),
            'random_forest': {
                'precision': round(float(precision_score(y_demo, y_pred_rf, zero_division=0)), 4),
                'recall': round(float(recall_score(y_demo, y_pred_rf, zero_division=0)), 4),
                'f1_score': round(float(f1_score(y_demo, y_pred_rf, zero_division=0)), 4),
                'roc_auc': round(float(roc_auc_score(y_demo, y_prob_rf)), 4),
                'confusion_matrix': cm_rf
            },
            'logistic_regression': {
                'precision': round(float(precision_score(y_demo, y_pred_lr, zero_division=0)), 4),
                'recall': round(float(recall_score(y_demo, y_pred_lr, zero_division=0)), 4),
                'f1_score': round(float(f1_score(y_demo, y_pred_lr, zero_division=0)), 4),
                'roc_auc': round(float(roc_auc_score(y_demo, y_prob_lr)), 4),
                'confusion_matrix': cm_lr
            }
        }

        csv_rows.append({
            'Model': 'Random Forest Classifier',
            'Dataset': 'Synthetic Demo Dataset',
            'Precision': round(float(precision_score(y_demo, y_pred_rf, zero_division=0)), 4),
            'Recall': round(float(recall_score(y_demo, y_pred_rf, zero_division=0)), 4),
            'F1_Score': round(float(f1_score(y_demo, y_pred_rf, zero_division=0)), 4),
            'ROC_AUC': round(float(roc_auc_score(y_demo, y_prob_rf)), 4),
            'Status': 'Valid Supervised Metric'
        })
        csv_rows.append({
            'Model': 'Logistic Regression Baseline',
            'Dataset': 'Synthetic Demo Dataset',
            'Precision': round(float(precision_score(y_demo, y_pred_lr, zero_division=0)), 4),
            'Recall': round(float(recall_score(y_demo, y_pred_lr, zero_division=0)), 4),
            'F1_Score': round(float(f1_score(y_demo, y_pred_lr, zero_division=0)), 4),
            'ROC_AUC': round(float(roc_auc_score(y_demo, y_prob_lr)), 4),
            'Status': 'Valid Supervised Metric'
        })

    # 2. Evaluation on Real Public Source Dataset
    eval_results['Real_Public_Source_Evaluation'] = {
        'dataset': 'JalRakshak Real Integrated Public Dataset',
        'sample_count': len(df_real),
        'status_message': 'Insufficient labelled data for reliable supervised model evaluation.',
        'explanation': 'Real national public health data source (Rajya Sabha AU 557) provides annual national aggregates rather than district-level confirmed epidemic ground-truth labels. Supervised metrics are reserved for synthetic demo mode to maintain strict technical honesty.'
    }

    csv_rows.append({
        'Model': 'All Models',
        'Dataset': 'Real Public Source Dataset',
        'Precision': 'N/A',
        'Recall': 'N/A',
        'F1_Score': 'N/A',
        'ROC_AUC': 'N/A',
        'Status': 'Insufficient labelled data for reliable supervised model evaluation'
    })

    json_path = os.path.join(REPORT_DIR, 'model_evaluation.json')
    csv_path = os.path.join(REPORT_DIR, 'model_evaluation.csv')

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(eval_results, f, indent=2)

    pd.DataFrame(csv_rows).to_csv(csv_path, index=False)
    print(f"Model evaluation reports generated at:\n  - {json_path}\n  - {csv_path}")

if __name__ == '__main__':
    evaluate_models()
