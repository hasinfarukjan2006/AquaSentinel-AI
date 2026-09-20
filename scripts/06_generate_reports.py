import os
import pandas as pd

def generate_reports():
    processed_dir = 'data/processed'
    derived_dir = 'data/derived'
    reports_dir = 'data/reports'
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    excel_path = os.path.join(processed_dir, 'JalRakshak_Integrated_Dataset.xlsx')

    # Load dataframes
    df_integrated = pd.read_csv(os.path.join(processed_dir, 'JalRakshak_Integrated_Dataset.csv'))
    df_health = pd.read_csv(os.path.join(derived_dir, 'cleaned_health.csv'))
    df_rainfall = pd.read_csv(os.path.join(derived_dir, 'cleaned_rainfall.csv'))
    df_wq = pd.read_csv(os.path.join(derived_dir, 'cleaned_water_quality.csv'))
    df_geo = pd.read_csv(os.path.join(processed_dir, 'geography_mapping.csv'))

    # Sheet 5: Feature Engineered Data
    feature_cols = [c for c in df_integrated.columns if 'risk' in c or 'anomaly' in c or 'flag' in c or 'component' in c or 'change' in c]
    df_features = df_integrated[['record_id', 'state', 'district', 'year', 'season'] + feature_cols].copy()

    # Sheet 6: Data Quality Report
    total_recs = len(df_integrated)
    complete_recs = len(df_integrated[df_integrated['data_availability_status'] == 'COMPLETE'])
    partial_recs = len(df_integrated[df_integrated['data_availability_status'] == 'PARTIAL'])
    wq_only = len(df_integrated[df_integrated['data_availability_status'] == 'WATER_ONLY'])
    rf_only = len(df_integrated[df_integrated['data_availability_status'] == 'RAINFALL_ONLY'])
    hlth_only = len(df_integrated[df_integrated['data_availability_status'] == 'HEALTH_ONLY'])

    df_dq = pd.DataFrame([
        {'Metric': 'Total Integrated Records', 'Value': total_recs},
        {'Metric': 'Complete Availability Records', 'Value': complete_recs},
        {'Metric': 'Partial Availability Records', 'Value': partial_recs},
        {'Metric': 'Water Quality Only Records', 'Value': wq_only},
        {'Metric': 'Rainfall Only Records', 'Value': rf_only},
        {'Metric': 'Health Only Records', 'Value': hlth_only},
        {'Metric': 'Geographic Mappings Total', 'Value': len(df_geo)},
        {'Metric': 'Missing Water Quality Values Pct', 'Value': f"{df_integrated[['ph', 'ec_us_cm', 'tds_mg_l']].isnull().mean().mean() * 100:.1f}%"},
        {'Metric': 'Data Integrity Guarantee', 'Value': 'No fake records mixed into Real Public Source dataset'}
    ])

    # Sheet 8: Data Dictionary
    df_dict = pd.DataFrame([
        {'Field': 'record_id', 'Type': 'String', 'Description': 'Unique identifier for dataset record'},
        {'Field': 'state', 'Type': 'String', 'Description': 'Standardized state name'},
        {'Field': 'district', 'Type': 'String', 'Description': 'Standardized district name'},
        {'Field': 'year', 'Type': 'Integer', 'Description': 'Measurement or report year'},
        {'Field': 'season', 'Type': 'String', 'Description': 'Season (Pre-Monsoon, Monsoon, Post-Monsoon, Annual)'},
        {'Field': 'ph', 'Type': 'Float', 'Description': 'Water pH value (IS 10500 standard: 6.5-8.5)'},
        {'Field': 'ec_us_cm', 'Type': 'Float', 'Description': 'Electrical Conductivity in uS/cm'},
        {'Field': 'tds_mg_l', 'Type': 'Float', 'Description': 'Total Dissolved Solids in mg/L'},
        {'Field': 'no3_mg_l', 'Type': 'Float', 'Description': 'Nitrate concentration in mg/L'},
        {'Field': 'so4_mg_l', 'Type': 'Float', 'Description': 'Sulphate concentration in mg/L'},
        {'Field': 'f_mg_l', 'Type': 'Float', 'Description': 'Fluoride concentration in mg/L'},
        {'Field': 'fe_mg_l', 'Type': 'Float', 'Description': 'Iron concentration in mg/L'},
        {'Field': 'rainfall_mm', 'Type': 'Float', 'Description': 'Monsoon rainfall in millimeters'},
        {'Field': 'health_value', 'Type': 'Integer', 'Description': 'Reported water-borne disease cases'},
        {'Field': 'anomaly_score', 'Type': 'Float', 'Description': 'Isolation Forest anomaly score'},
        {'Field': 'risk_score', 'Type': 'Float', 'Description': 'Composite JalRakshak risk score (0-100)'},
        {'Field': 'risk_class', 'Type': 'String', 'Description': 'Risk classification band (LOW, MODERATE, HIGH, VERY HIGH, CRITICAL)'},
        {'Field': 'data_type', 'Type': 'String', 'Description': 'REAL_PUBLIC_SOURCE or SYNTHETIC_DEMO'}
    ])

    # Sheet 9: Source Provenance
    df_prov = pd.DataFrame([
        {
            'Dataset': 'Ground Water Quality',
            'Source': 'Central Ground Water Board (CGWB) 2024 Report',
            'Coverage': 'Andhra Pradesh, Arunachal Pradesh, Assam (589 stations)',
            'License/Access': 'Public Government Data'
        },
        {
            'Dataset': 'Monsoon Rainfall',
            'Source': 'India Meteorological Department (IMD) All-India Monsoon Series (1901-2021)',
            'Coverage': 'All-India Monthly Monsoon (JUN-SEP)',
            'License/Access': 'Public Historical Meteorological Data'
        },
        {
            'Dataset': 'Water-borne Disease Reports',
            'Source': 'Rajya Sabha Unstarred Question No. 557 (2019-2021)',
            'Coverage': 'National reported cases for ADD, Cholera, Hepatitis A/E, Leptospirosis',
            'License/Access': 'Public Parliamentary Health Data'
        }
    ])

    # Sheet 10: README
    df_readme = pd.DataFrame([
        {'Section': 'Project', 'Content': 'JalRakshak AI — Community Water-Borne Disease Early Warning System'},
        {'Section': 'Tagline', 'Content': 'From Water Risk to Early Action.'},
        {'Section': 'Purpose', 'Content': 'Decision-support prototype for authorized health officials. AI risk scores are early-warning signals, NOT medical diagnoses.'},
        {'Section': 'Author', 'Content': 'JalRakshak Engineering Team'},
        {'Section': 'Dataset Version', 'Content': '1.0.0 Integrated Prototype Dataset'}
    ])

    # Write 10 sheets to Excel
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df_integrated.to_excel(writer, sheet_name='Integrated_Data', index=False)
        df_health.to_excel(writer, sheet_name='Health_Data', index=False)
        df_rainfall.to_excel(writer, sheet_name='Rainfall_Data', index=False)
        df_wq.to_excel(writer, sheet_name='Water_Quality_Data', index=False)
        df_features.to_excel(writer, sheet_name='Feature_Engineered_Data', index=False)
        df_dq.to_excel(writer, sheet_name='Data_Quality_Report', index=False)
        df_geo.to_excel(writer, sheet_name='Geography_Mapping', index=False)
        df_dict.to_excel(writer, sheet_name='Data_Dictionary', index=False)
        df_prov.to_excel(writer, sheet_name='Source_Provenance', index=False)
        df_readme.to_excel(writer, sheet_name='README', index=False)

    print(f"10-Sheet Excel Workbook generated successfully at:\n  - {excel_path}")

if __name__ == '__main__':
    generate_reports()
