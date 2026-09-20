import os
import sqlite3
import pandas as pd
import numpy as np

DB_PATH = os.path.join(os.path.dirname(__file__), 'jalrakshak.db')
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
PROCESSED_DIR = os.path.join(BASE_DIR, 'Data', 'processed')
DERIVED_DIR = os.path.join(BASE_DIR, 'Data', 'derived')

def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop existing tables
    cursor.executescript("""
    DROP TABLE IF EXISTS locations;
    DROP TABLE IF EXISTS health_records;
    DROP TABLE IF EXISTS rainfall_records;
    DROP TABLE IF EXISTS water_quality_records;
    DROP TABLE IF EXISTS risk_scores;
    DROP TABLE IF EXISTS alerts;
    DROP TABLE IF EXISTS data_sources;
    DROP TABLE IF EXISTS model_runs;

    CREATE TABLE locations (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        state TEXT NOT NULL,
        district TEXT NOT NULL,
        block_taluka TEXT,
        station_location TEXT,
        latitude REAL,
        longitude REAL,
        UNIQUE(state, district, station_location)
    );

    CREATE TABLE health_records (
        record_id TEXT PRIMARY KEY,
        location_id INTEGER,
        state TEXT,
        district TEXT,
        year INTEGER,
        month TEXT,
        health_value REAL,
        health_indicator TEXT,
        health_source TEXT,
        data_type TEXT,
        FOREIGN KEY(location_id) REFERENCES locations(location_id)
    );

    CREATE TABLE rainfall_records (
        record_id TEXT PRIMARY KEY,
        location_id INTEGER,
        state TEXT,
        district TEXT,
        year INTEGER,
        month TEXT,
        season TEXT,
        rainfall_mm REAL,
        rainfall_anomaly REAL,
        rainfall_source TEXT,
        data_type TEXT,
        FOREIGN KEY(location_id) REFERENCES locations(location_id)
    );

    CREATE TABLE water_quality_records (
        record_id TEXT PRIMARY KEY,
        location_id INTEGER,
        state TEXT,
        district TEXT,
        block_taluka TEXT,
        station_location TEXT,
        year INTEGER,
        season TEXT,
        latitude REAL,
        longitude REAL,
        ph REAL,
        ec_us_cm REAL,
        tds_mg_l REAL,
        cl_mg_l REAL,
        no3_mg_l REAL,
        so4_mg_l REAL,
        f_mg_l REAL,
        total_hardness_mg_l REAL,
        fe_mg_l REAL,
        as_ppb REAL,
        u_ppb REAL,
        water_source TEXT,
        data_type TEXT,
        FOREIGN KEY(location_id) REFERENCES locations(location_id)
    );

    CREATE TABLE risk_scores (
        risk_id INTEGER PRIMARY KEY AUTOINCREMENT,
        record_id TEXT UNIQUE,
        location_id INTEGER,
        state TEXT,
        district TEXT,
        year INTEGER,
        month TEXT,
        season TEXT,
        risk_score REAL,
        risk_class TEXT,
        health_component REAL,
        water_component REAL,
        env_component REAL,
        hist_component REAL,
        vuln_component REAL,
        abnormal_component REAL,
        anomaly_score REAL,
        abnormal_pattern_flag INTEGER,
        data_availability_status TEXT,
        data_type TEXT,
        FOREIGN KEY(location_id) REFERENCES locations(location_id)
    );

    CREATE TABLE alerts (
        alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id INTEGER,
        state TEXT,
        district TEXT,
        alert_level TEXT,
        risk_score REAL,
        title TEXT,
        reason TEXT,
        recommended_action TEXT,
        created_at TEXT,
        data_type TEXT,
        FOREIGN KEY(location_id) REFERENCES locations(location_id)
    );

    CREATE TABLE data_sources (
        source_id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_name TEXT,
        provider TEXT,
        coverage TEXT,
        last_updated TEXT,
        record_count INTEGER
    );

    CREATE TABLE model_runs (
        run_id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT,
        run_timestamp TEXT,
        dataset_used TEXT,
        sample_count INTEGER,
        status TEXT
    );

    -- Indexes for performance
    CREATE INDEX idx_locations_state ON locations(state);
    CREATE INDEX idx_locations_district ON locations(district);
    CREATE INDEX idx_risk_scores_state ON risk_scores(state);
    CREATE INDEX idx_risk_scores_district ON risk_scores(district);
    CREATE INDEX idx_risk_scores_year ON risk_scores(year);
    CREATE INDEX idx_risk_scores_data_type ON risk_scores(data_type);
    CREATE INDEX idx_wq_data_type ON water_quality_records(data_type);
    CREATE INDEX idx_rf_data_type ON rainfall_records(data_type);
    CREATE INDEX idx_hlth_data_type ON health_records(data_type);
    """)

    conn.commit()

    # -------------------------------------------------------------
    # 1. Load Locations and Integrated Risk Records
    # -------------------------------------------------------------
    real_integrated_csv = os.path.join(PROCESSED_DIR, 'JalRakshak_Integrated_Dataset.csv')
    demo_csv = os.path.join(PROCESSED_DIR, 'synthetic_demo_dataset.csv')

    dfs_to_load = []
    if os.path.exists(real_integrated_csv):
        dfs_to_load.append(pd.read_csv(real_integrated_csv))
    if os.path.exists(demo_csv):
        dfs_to_load.append(pd.read_csv(demo_csv))

    if dfs_to_load:
        df_all = pd.concat(dfs_to_load, ignore_index=True)
        
        # Populate locations table
        loc_df = df_all[['state', 'district', 'block_taluka', 'station_location', 'latitude', 'longitude']].drop_duplicates(subset=['state', 'district', 'station_location'])
        
        loc_rows_to_insert = [
            (
                r['state'], r['district'], 
                None if pd.isna(r['block_taluka']) else str(r['block_taluka']), 
                None if pd.isna(r['station_location']) else str(r['station_location']), 
                None if pd.isna(r['latitude']) else float(r['latitude']), 
                None if pd.isna(r['longitude']) else float(r['longitude'])
            )
            for _, r in loc_df.iterrows()
        ]

        cursor.executemany("""
        INSERT OR IGNORE INTO locations (state, district, block_taluka, station_location, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?)
        """, loc_rows_to_insert)
        conn.commit()

        # Map locations
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        loc_rows = cur.execute("SELECT location_id, state, district, station_location FROM locations").fetchall()
        loc_map = {(r['state'], r['district'], r['station_location']): r['location_id'] for r in loc_rows}

        risk_rows = []
        alert_rows = []

        for idx, row in df_all.iterrows():
            loc_id = loc_map.get((row['state'], row['district'], row['station_location']))
            rec_id = str(row['record_id'])
            st = str(row['state'])
            dt = str(row['district'])
            yr = int(row['year']) if pd.notna(row['year']) else 2024
            mth = str(row.get('month', 'N/A')) if pd.notna(row.get('month')) else 'N/A'
            sea = str(row.get('season', 'N/A')) if pd.notna(row.get('season')) else 'N/A'
            r_score = float(row['risk_score']) if pd.notna(row.get('risk_score')) else 35.0
            r_class = str(row['risk_class']) if pd.notna(row.get('risk_class')) else 'MODERATE'
            dtype = str(row.get('data_type', 'REAL_PUBLIC_SOURCE')) if pd.notna(row.get('data_type')) else 'REAL_PUBLIC_SOURCE'

            risk_rows.append((
                rec_id, loc_id, st, dt, yr, mth, sea, r_score, r_class,
                float(row.get('health_risk_component', 0.2)) if pd.notna(row.get('health_risk_component')) else 0.2,
                float(row.get('water_risk_component', 0.2)) if pd.notna(row.get('water_risk_component')) else 0.2,
                float(row.get('env_risk_component', 0.2)) if pd.notna(row.get('env_risk_component')) else 0.2,
                float(row.get('hist_risk_component', 0.2)) if pd.notna(row.get('hist_risk_component')) else 0.2,
                float(row.get('vuln_risk_component', 0.2)) if pd.notna(row.get('vuln_risk_component')) else 0.2,
                float(row.get('abnormal_risk_component', 0.1)) if pd.notna(row.get('abnormal_risk_component')) else 0.1,
                float(row.get('anomaly_score', 0.0)) if pd.notna(row.get('anomaly_score')) else 0.0,
                int(row.get('abnormal_pattern_flag', 0)) if pd.notna(row.get('abnormal_pattern_flag')) else 0,
                str(row.get('data_availability_status', 'PARTIAL')) if pd.notna(row.get('data_availability_status')) else 'PARTIAL',
                dtype
            ))

            if r_score >= 45.0:
                alert_level = 'HIGH' if r_score >= 47.0 else 'MODERATE'
                alert_rows.append((
                    loc_id, st, dt, alert_level, r_score,
                    f"Elevated Risk Signal in {dt}",
                    f"Multiple environmental and health indicators in {dt} show elevated risk values (Score: {r_score}).",
                    "Local health officer verification recommended. Check ground water samples and community reports.",
                    f"{yr}-07-15", dtype
                ))

        cur.executemany("""
        INSERT OR IGNORE INTO risk_scores (
            record_id, location_id, state, district, year, month, season,
            risk_score, risk_class, health_component, water_component,
            env_component, hist_component, vuln_component, abnormal_component,
            anomaly_score, abnormal_pattern_flag, data_availability_status, data_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, risk_rows)

        cur.executemany("""
        INSERT INTO alerts (
            location_id, state, district, alert_level, risk_score,
            title, reason, recommended_action, created_at, data_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, alert_rows)

    # -------------------------------------------------------------
    # 2. Load CGWB Water Quality Source Dataset (589 records)
    # -------------------------------------------------------------
    wq_csv = os.path.join(DERIVED_DIR, 'cleaned_water_quality.csv')
    if os.path.exists(wq_csv):
        df_wq = pd.read_csv(wq_csv)
        wq_rows = []
        for idx, row in df_wq.iterrows():
            rec_id = f"WQ_2024_{row.get('S_No', idx)}"
            st = str(row.get('State_UT', 'Andhra Pradesh'))
            dt = str(row.get('District', 'Unknown'))
            blk = str(row.get('Block_Taluka', '')) if pd.notna(row.get('Block_Taluka')) else None
            stn = str(row.get('Station_Location', '')) if pd.notna(row.get('Station_Location')) else dt
            lat = float(row['Latitude']) if pd.notna(row.get('Latitude')) else None
            lng = float(row['Longitude']) if pd.notna(row.get('Longitude')) else None
            
            loc_id = loc_map.get((st, dt, stn))

            wq_rows.append((
                rec_id, loc_id, st, dt, blk, stn,
                int(row.get('Year', 2024)), str(row.get('Season', 'Pre-Monsoon')),
                lat, lng,
                float(row['pH']) if pd.notna(row.get('pH')) else None,
                float(row['EC_uS_cm']) if pd.notna(row.get('EC_uS_cm')) else None,
                float(row['TDS_mg_L']) if pd.notna(row.get('TDS_mg_L')) else None,
                float(row['Cl_mg_L']) if pd.notna(row.get('Cl_mg_L')) else None,
                float(row['NO3_mg_L']) if pd.notna(row.get('NO3_mg_L')) else None,
                float(row['SO4_mg_L']) if pd.notna(row.get('SO4_mg_L')) else None,
                float(row['F_mg_L']) if pd.notna(row.get('F_mg_L')) else None,
                float(row['Total_Hardness_mg_L']) if pd.notna(row.get('Total_Hardness_mg_L')) else None,
                float(row['Fe_mg_L']) if pd.notna(row.get('Fe_mg_L')) else None,
                float(row['As_ppb']) if pd.notna(row.get('As_ppb')) else None,
                float(row['U_ppb']) if pd.notna(row.get('U_ppb')) else None,
                str(row.get('Data_Source', 'Central Ground Water Board (CGWB 2024)')),
                'REAL_PUBLIC_SOURCE'
            ))

        cur.executemany("""
        INSERT OR IGNORE INTO water_quality_records (
            record_id, location_id, state, district, block_taluka, station_location,
            year, season, latitude, longitude, ph, ec_us_cm, tds_mg_l, cl_mg_l,
            no3_mg_l, so4_mg_l, f_mg_l, total_hardness_mg_l, fe_mg_l, as_ppb, u_ppb,
            water_source, data_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, wq_rows)

    # -------------------------------------------------------------
    # 3. Load IMD Rainfall Source Dataset (121 records)
    # -------------------------------------------------------------
    rf_csv = os.path.join(DERIVED_DIR, 'cleaned_rainfall.csv')
    if os.path.exists(rf_csv):
        df_rf = pd.read_csv(rf_csv)
        rf_rows = []
        mean_rf = df_rf['JUN-SEP'].mean()
        std_rf = df_rf['JUN-SEP'].std()
        
        for idx, row in df_rf.iterrows():
            yr = int(row['YEAR'])
            val = float(row['JUN-SEP']) if pd.notna(row.get('JUN-SEP')) else 0.0
            anomaly = (val - mean_rf) / std_rf if std_rf else 0.0

            rf_rows.append((
                f"RF_IMD_{yr}", None, 'All-India', 'All-India Monsoon Series',
                yr, 'JUN-SEP', 'Monsoon', val, round(anomaly, 2),
                'India Meteorological Department (IMD 1901-2021)',
                'REAL_PUBLIC_SOURCE'
            ))

        cur.executemany("""
        INSERT OR IGNORE INTO rainfall_records (
            record_id, location_id, state, district, year, month, season,
            rainfall_mm, rainfall_anomaly, rainfall_source, data_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, rf_rows)

    # -------------------------------------------------------------
    # 4. Load MoHFW / Rajya Sabha Health Source Dataset
    # -------------------------------------------------------------
    hlth_csv = os.path.join(DERIVED_DIR, 'cleaned_health.csv')
    if os.path.exists(hlth_csv):
        df_hlth = pd.read_csv(hlth_csv)
        hlth_rows = []
        for idx, row in df_hlth.iterrows():
            disease = str(row['Water-borne diseases'])
            for yr in [2019, 2020, 2021]:
                col_name = f"No. of Cases Reported - {yr}"
                if col_name in row and pd.notna(row[col_name]):
                    cases = float(row[col_name])
                    hlth_rows.append((
                        f"HLTH_RS_{yr}_{idx}", None, 'All-India', 'National Aggregate',
                        yr, 'Annual', cases, disease,
                        'Ministry of Health & Family Welfare (Rajya Sabha Question No. 557)',
                        'REAL_PUBLIC_SOURCE'
                    ))

        cur.executemany("""
        INSERT OR IGNORE INTO health_records (
            record_id, location_id, state, district, year, month,
            health_value, health_indicator, health_source, data_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, hlth_rows)

    # Seed data_sources metadata table
    cur.executescript("""
    INSERT OR IGNORE INTO data_sources (source_id, dataset_name, provider, coverage, last_updated, record_count) VALUES
    (1, 'CGWB Ground Water Quality 2024', 'Central Ground Water Board', '589 Stations (AP, Assam, Arunachal)', '2024-06-30', 589),
    (2, 'IMD All-India Monsoon Series', 'India Meteorological Department', '1901-2021 Monthly Monsoon', '2021-12-31', 121),
    (3, 'Rajya Sabha Disease Question No. 557', 'Ministry of Health & Family Welfare', 'National Aggregate (2019-2021)', '2021-12-31', 5),
    (4, 'AquaSentinel Integrated Risk Dataset', 'JalRakshak AI Pipeline', '713 Real Integrated Records', '2024-09-20', 713);
    """)

    conn.commit()
    print("Database initialized cleanly with all source datasets (Water Quality, Rainfall, Health, Risk Scores).")
    conn.close()

def ensure_db_initialized():
    """Checks if database table risk_scores and water_quality_records exist and have records."""
    try:
        if not os.path.exists(DB_PATH):
            print("Database file missing. Initializing database...")
            init_database()
            return

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM water_quality_records")
        wq_cnt = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM risk_scores")
        risk_cnt = cur.fetchone()[0]
        conn.close()
        
        if wq_cnt == 0 or risk_cnt == 0:
            print("Database source tables empty. Seeding database...")
            init_database()
    except Exception as e:
        print(f"Database check failed ({e}). Initializing database...")
        init_database()

if __name__ == '__main__':
    init_database()
