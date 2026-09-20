import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), 'jalrakshak.db')
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')

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
        year INTEGER,
        season TEXT,
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

    -- Indexes for high performance
    CREATE INDEX idx_locations_state ON locations(state);
    CREATE INDEX idx_locations_district ON locations(district);
    CREATE INDEX idx_risk_scores_state ON risk_scores(state);
    CREATE INDEX idx_risk_scores_district ON risk_scores(district);
    CREATE INDEX idx_risk_scores_year ON risk_scores(year);
    CREATE INDEX idx_risk_scores_month ON risk_scores(month);
    CREATE INDEX idx_risk_scores_loc_id ON risk_scores(location_id);
    """)

    conn.commit()

    # Load data into DB
    real_csv = os.path.join(PROCESSED_DIR, 'JalRakshak_Integrated_Dataset.csv')
    demo_csv = os.path.join(PROCESSED_DIR, 'synthetic_demo_dataset.csv')

    dfs_to_load = []
    if os.path.exists(real_csv):
        dfs_to_load.append(pd.read_csv(real_csv))
    if os.path.exists(demo_csv):
        dfs_to_load.append(pd.read_csv(demo_csv))

    if dfs_to_load:
        df_all = pd.concat(dfs_to_load, ignore_index=True)
        
        # Populate locations safely
        loc_df = df_all[['state', 'district', 'block_taluka', 'station_location', 'latitude', 'longitude']].drop_duplicates(subset=['state', 'district', 'station_location'])
        
        loc_rows_to_insert = [
            (r['state'], r['district'], r['block_taluka'], r['station_location'], r['latitude'], r['longitude'])
            for _, r in loc_df.iterrows()
        ]

        cursor.executemany("""
        INSERT OR IGNORE INTO locations (state, district, block_taluka, station_location, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?)
        """, loc_rows_to_insert)
        conn.commit()

        # Map location_id
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
            mth = str(row.get('month', 'N/A'))
            sea = str(row.get('season', 'N/A'))
            r_score = float(row['risk_score']) if pd.notna(row.get('risk_score')) else 35.0
            r_class = str(row['risk_class']) if pd.notna(row.get('risk_class')) else 'MODERATE'
            dtype = str(row.get('data_type', 'REAL_PUBLIC_SOURCE'))

            risk_rows.append((
                rec_id, loc_id, st, dt, yr, mth, sea, r_score, r_class,
                float(row.get('health_risk_component', 0.2)),
                float(row.get('water_risk_component', 0.2)),
                float(row.get('env_risk_component', 0.2)),
                float(row.get('hist_risk_component', 0.2)),
                float(row.get('vuln_risk_component', 0.2)),
                float(row.get('abnormal_risk_component', 0.1)),
                float(row.get('anomaly_score', 0.0)),
                int(row.get('abnormal_pattern_flag', 0)),
                str(row.get('data_availability_status', 'PARTIAL')),
                dtype
            ))

            if r_score >= 70.0:
                alert_level = 'CRITICAL' if r_score >= 86.0 else ('VERY HIGH' if r_score >= 71.0 else 'HIGH')
                alert_rows.append((
                    loc_id, st, dt, alert_level, r_score,
                    f"Elevated Risk Signal in {dt}",
                    f"Multiple environmental and health indicators in {dt} show abnormal patterns (Score: {r_score}).",
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

        # Seed data sources
        cur.executescript("""
        INSERT INTO data_sources (dataset_name, provider, coverage, last_updated, record_count) VALUES
        ('CGWB Ground Water Quality 2024', 'Central Ground Water Board', '589 Stations (AP, Assam, Arunachal)', '2024-06-30', 589),
        ('IMD All-India Monsoon Series', 'India Meteorological Department', '1901-2021 Monthly Monsoon', '2021-12-31', 121),
        ('Rajya Sabha Disease Question No. 557', 'Ministry of Health & Family Welfare', 'National Aggregate (2019-2021)', '2021-12-31', 5);
        """)

        conn.commit()
        print(f"Database initialized cleanly with {len(risk_rows)} risk score records and {len(alert_rows)} alerts.")

    conn.close()

if __name__ == '__main__':
    init_database()
