import os
import pandas as pd
import numpy as np

def integrate_sources():
    derived_dir = 'data/derived'
    processed_dir = 'data/processed'
    os.makedirs(processed_dir, exist_ok=True)

    # Load cleaned files
    df_h = pd.read_csv(os.path.join(derived_dir, 'cleaned_health.csv')) if os.path.exists(os.path.join(derived_dir, 'cleaned_health.csv')) else pd.DataFrame()
    df_rf = pd.read_csv(os.path.join(derived_dir, 'cleaned_rainfall.csv')) if os.path.exists(os.path.join(derived_dir, 'cleaned_rainfall.csv')) else pd.DataFrame()
    df_wq = pd.read_csv(os.path.join(derived_dir, 'cleaned_water_quality.csv')) if os.path.exists(os.path.join(derived_dir, 'cleaned_water_quality.csv')) else pd.DataFrame()
    df_geo = pd.read_csv(os.path.join(processed_dir, 'geography_mapping.csv')) if os.path.exists(os.path.join(processed_dir, 'geography_mapping.csv')) else pd.DataFrame()

    # Geo lookup dictionary
    geo_map = {}
    if not df_geo.empty:
        for _, row in df_geo.iterrows():
            geo_map[(row['state'], str(row['source_name']))] = row['canonical_name']

    integrated_rows = []

    # 1. Process Real Water Quality Records (2024)
    if not df_wq.empty:
        latest_rf = df_rf[df_rf['YEAR'] == 2021].iloc[0] if not df_rf.empty and 2021 in df_rf['YEAR'].values else None
        latest_h_total_2021 = df_h['No. of Cases Reported - 2021'].sum() if not df_h.empty else np.nan

        for idx, row in df_wq.iterrows():
            state = str(row.get('State_UT', '')).strip()
            dist_raw = str(row.get('District', '')).strip()
            dist_canonical = geo_map.get((state, dist_raw), dist_raw.title())

            rec = {
                'record_id': f"REAL_WQ_{row.get('S_No', idx)}",
                'state': state,
                'district': dist_canonical,
                'block_taluka': row.get('Block_Taluka', 'N/A'),
                'station_location': row.get('Station_Location', 'N/A'),
                'longitude': row.get('Longitude', np.nan),
                'latitude': row.get('Latitude', np.nan),
                'year': int(row.get('Year', 2024)),
                'month': 'Pre-Monsoon',
                'season': 'Pre-Monsoon',
                
                # Water parameters
                'ph': row.get('pH', np.nan),
                'ec_us_cm': row.get('EC_uS_cm', np.nan),
                'tds_mg_l': row.get('TDS_mg_L', np.nan),
                'cl_mg_l': row.get('Cl_mg_L', np.nan),
                'no3_mg_l': row.get('NO3_mg_L', np.nan),
                'so4_mg_l': row.get('SO4_mg_L', np.nan),
                'f_mg_l': row.get('F_mg_L', np.nan),
                'total_hardness_mg_l': row.get('Total_Hardness_mg_L', np.nan),
                'fe_mg_l': row.get('Fe_mg_L', np.nan),
                'as_ppb': row.get('As_ppb', np.nan),
                'u_ppb': row.get('U_ppb', np.nan),

                # Rainfall parameters (national series reference)
                'rainfall_mm': latest_rf['JUN-SEP'] if latest_rf is not None else np.nan,
                'rainfall_source': 'IMD All-India Monsoon Series' if latest_rf is not None else 'UNAVAILABLE',
                'rainfall_year': 2021 if latest_rf is not None else np.nan,

                # Health parameters (national reported reference)
                'health_value': latest_h_total_2021,
                'health_indicator': 'National Reported Water-Borne Disease Total',
                'health_source': 'Rajya Sabha Unstarred Question No. 557' if not df_h.empty else 'UNAVAILABLE',
                'health_year': 2021 if not df_h.empty else np.nan,

                'water_source': 'CGWB Ground Water Quality Data (2024)',
                'water_year': 2024,

                'data_availability_status': 'PARTIAL' if latest_rf is not None else 'WATER_ONLY',
                'data_type': 'REAL_PUBLIC_SOURCE'
            }
            integrated_rows.append(rec)

    # 2. Process Historical Rainfall Records (1901-2021)
    if not df_rf.empty:
        for idx, row in df_rf.iterrows():
            year_val = int(row['YEAR'])
            rec = {
                'record_id': f"REAL_RF_{year_val}",
                'state': 'All-India',
                'district': 'All-India Average',
                'block_taluka': 'N/A',
                'station_location': 'All-India Sub-Divisional Grid',
                'longitude': np.nan,
                'latitude': np.nan,
                'year': year_val,
                'month': 'Monsoon (JUN-SEP)',
                'season': 'Monsoon',
                'ph': np.nan, 'ec_us_cm': np.nan, 'tds_mg_l': np.nan, 'cl_mg_l': np.nan,
                'no3_mg_l': np.nan, 'so4_mg_l': np.nan, 'f_mg_l': np.nan,
                'total_hardness_mg_l': np.nan, 'fe_mg_l': np.nan, 'as_ppb': np.nan, 'u_ppb': np.nan,
                'rainfall_mm': row['JUN-SEP'],
                'rainfall_source': 'IMD All-India Monsoon Series (1901-2021)',
                'rainfall_year': year_val,
                'health_value': np.nan,
                'health_indicator': 'N/A',
                'health_source': 'UNAVAILABLE',
                'health_year': np.nan,
                'water_source': 'UNAVAILABLE',
                'water_year': np.nan,
                'data_availability_status': 'RAINFALL_ONLY',
                'data_type': 'REAL_PUBLIC_SOURCE'
            }
            integrated_rows.append(rec)

    # 3. Process Rajya Sabha Health Records (2019-2021)
    if not df_h.empty:
        for year in [2019, 2020, 2021]:
            col_name = f"No. of Cases Reported - {year}"
            if col_name in df_h.columns:
                total_cases = df_h[col_name].sum()
                rec = {
                    'record_id': f"REAL_HLTH_{year}",
                    'state': 'India',
                    'district': 'National Aggregate',
                    'block_taluka': 'N/A',
                    'station_location': 'Ministry of Health & Family Welfare',
                    'longitude': np.nan,
                    'latitude': np.nan,
                    'year': year,
                    'month': 'Annual',
                    'season': 'Annual',
                    'ph': np.nan, 'ec_us_cm': np.nan, 'tds_mg_l': np.nan, 'cl_mg_l': np.nan,
                    'no3_mg_l': np.nan, 'so4_mg_l': np.nan, 'f_mg_l': np.nan,
                    'total_hardness_mg_l': np.nan, 'fe_mg_l': np.nan, 'as_ppb': np.nan, 'u_ppb': np.nan,
                    'rainfall_mm': np.nan,
                    'rainfall_source': 'UNAVAILABLE',
                    'rainfall_year': np.nan,
                    'health_value': total_cases,
                    'health_indicator': 'Total Water-Borne Disease Cases (ADD, Cholera, Hepatitis, Leptospirosis)',
                    'health_source': 'Rajya Sabha Unstarred Question No. 557',
                    'health_year': year,
                    'water_source': 'UNAVAILABLE',
                    'water_year': np.nan,
                    'data_availability_status': 'HEALTH_ONLY',
                    'data_type': 'REAL_PUBLIC_SOURCE'
                }
                integrated_rows.append(rec)

    df_integrated = pd.DataFrame(integrated_rows)
    real_csv_path = os.path.join(processed_dir, 'JalRakshak_Integrated_Dataset.csv')
    df_integrated.to_csv(real_csv_path, index=False)
    print(f"Integrated dataset generated with {len(df_integrated)} real public records in:\n  - {real_csv_path}")

    # 4. Generate Synthetic Demo Dataset (500 records)
    generate_synthetic_demo_dataset(processed_dir)

def generate_synthetic_demo_dataset(processed_dir):
    np.random.seed(42)
    demo_locations = [
        ('Tamil Nadu', 'Salem', 11.6643, 78.1460),
        ('Tamil Nadu', 'Chennai', 13.0827, 80.2707),
        ('Tamil Nadu', 'Coimbatore', 11.0168, 76.9558),
        ('Tamil Nadu', 'Madurai', 9.9252, 78.1198),
        ('Tamil Nadu', 'Tiruchirappalli', 10.7905, 78.7047),
        ('Andhra Pradesh', 'Visakhapatnam', 17.6868, 83.2185),
        ('Andhra Pradesh', 'Vijayawada', 16.5062, 80.6480),
        ('Andhra Pradesh', 'Guntur', 16.3067, 80.4365),
        ('Andhra Pradesh', 'Anantapur', 14.6819, 77.6006),
        ('Assam', 'Kamrup Metropolitan', 26.1445, 91.7362),
        ('Assam', 'Cachar', 24.8333, 92.7789),
        ('Arunachal Pradesh', 'Papum Pare', 27.1000, 93.6200),
        ('Kerala', 'Wayanad', 11.6854, 76.1320),
        ('Karnataka', 'Raichur', 16.2076, 77.3463),
        ('Maharashtra', 'Latur', 18.4088, 76.5604)
    ]

    seasons = ['Pre-Monsoon', 'Monsoon', 'Post-Monsoon']
    years = [2022, 2023, 2024]
    
    demo_rows = []
    rec_counter = 1

    for i in range(520):
        loc = demo_locations[i % len(demo_locations)]
        state, dist, lat_base, lon_base = loc
        year = years[i % len(years)]
        season = seasons[(i // len(years)) % len(seasons)]
        
        # Add slight jitter to lat/lon for stations
        lat = round(lat_base + np.random.uniform(-0.05, 0.05), 4)
        lon = round(lon_base + np.random.uniform(-0.05, 0.05), 4)

        # Baseline parameters with seasonal variations
        is_monsoon = (season == 'Monsoon')
        ph = round(float(np.random.normal(7.2, 0.4)), 2)
        ec = round(float(np.random.normal(1200, 350)), 1)
        tds = round(float(ec * 0.65), 1)
        no3 = round(float(np.random.gamma(shape=2, scale=12)), 1)
        cl = round(float(np.random.normal(180, 50)), 1)
        so4 = round(float(np.random.normal(120, 35)), 1)
        f = round(float(np.random.uniform(0.3, 1.8)), 2)
        hardness = round(float(np.random.normal(280, 75)), 1)
        fe = round(float(np.random.exponential(0.3)), 2)
        as_ppb = round(float(np.random.exponential(2.5)), 2)
        u_ppb = round(float(np.random.exponential(3.0)), 2)

        # Rainfall
        if is_monsoon:
            rf = round(float(np.random.normal(320, 90)), 1)
        else:
            rf = round(float(np.random.normal(45, 20)), 1)
        
        # Health cases
        base_cases = np.random.randint(15, 120)
        if dist in ['Salem', 'Kamrup Metropolitan'] and is_monsoon:
            # Simulate a elevated pattern in demo dataset for Salem/Kamrup in monsoon
            rf += 180.0
            no3 += 35.0
            base_cases += 110

        demo_rows.append({
            'record_id': f"DEMO_REC_{rec_counter:04d}",
            'state': state,
            'district': dist,
            'block_taluka': f"{dist} Central",
            'station_location': f"{dist} Station-{ (rec_counter % 5) + 1 }",
            'longitude': lon,
            'latitude': lat,
            'year': year,
            'month': 'July' if is_monsoon else ('May' if season == 'Pre-Monsoon' else 'November'),
            'season': season,
            'ph': ph,
            'ec_us_cm': ec,
            'tds_mg_l': tds,
            'cl_mg_l': cl,
            'no3_mg_l': no3,
            'so4_mg_l': so4,
            'f_mg_l': f,
            'total_hardness_mg_l': hardness,
            'fe_mg_l': fe,
            'as_ppb': as_ppb,
            'u_ppb': u_ppb,
            'rainfall_mm': rf,
            'rainfall_source': 'Synthetic Environmental Simulation',
            'rainfall_year': year,
            'health_value': base_cases,
            'health_indicator': 'Reported Diarrheal/Gastrointestinal Cases',
            'health_source': 'Synthetic Community Health Registry',
            'health_year': year,
            'water_source': 'Synthetic Ground Water Monitoring',
            'water_year': year,
            'data_availability_status': 'COMPLETE',
            'data_type': 'SYNTHETIC_DEMO'
        })
        rec_counter += 1

    df_demo = pd.DataFrame(demo_rows)
    demo_csv_path1 = os.path.join(processed_dir, 'JalRakshak_Synthetic_Demo_Dataset.csv')
    demo_csv_path2 = os.path.join(processed_dir, 'synthetic_demo_dataset.csv')
    df_demo.to_csv(demo_csv_path1, index=False)
    df_demo.to_csv(demo_csv_path2, index=False)
    print(f"Synthetic demo dataset generated with {len(df_demo)} records in:\n  - {demo_csv_path1}\n  - {demo_csv_path2}")

if __name__ == '__main__':
    integrate_sources()
