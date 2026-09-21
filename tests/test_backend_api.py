import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_api_health(client):
    res = client.get('/api/health')
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'healthy'
    assert 'AquaSentinel' in data['service']

def test_api_summary(client):
    res = client.get('/api/summary?data_type=SYNTHETIC_DEMO')
    assert res.status_code == 200
    data = res.get_json()
    assert 'monitored_locations' in data
    assert 'risk_distribution' in data

def test_api_locations(client):
    res = client.get('/api/locations?data_type=SYNTHETIC_DEMO')
    assert res.status_code == 200
    data = res.get_json()
    assert 'locations' in data
    assert len(data['locations']) > 0

def test_api_risk(client):
    res = client.get('/api/risk?data_type=SYNTHETIC_DEMO&limit=10')
    assert res.status_code == 200
    data = res.get_json()
    assert 'records' in data
    assert len(data['records']) <= 10

def test_api_risk_predict(client):
    payload = {
        'ph': 7.8, 'ec_us_cm': 1200.0, 'tds_mg_l': 600.0, 'cl_mg_l': 200.0,
        'no3_mg_l': 55.0, 'so4_mg_l': 150.0, 'f_mg_l': 1.8, 'total_hardness_mg_l': 320.0,
        'fe_mg_l': 0.8, 'rainfall_mm': 420.0, 'health_value': 120
    }
    res = client.post('/api/risk/predict', json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert 'predicted_risk_score' in data
    assert 'predicted_risk_class' in data

def test_api_water_quality_real(client):
    res = client.get('/api/water-quality?data_type=REAL_PUBLIC_SOURCE')
    assert res.status_code == 200
    data = res.get_json()
    assert data['data_type'] == 'REAL_PUBLIC_SOURCE'
    assert data['count'] > 0
    assert len(data['records']) == data['count']

def test_api_rainfall_real(client):
    res = client.get('/api/rainfall?data_type=REAL_PUBLIC_SOURCE')
    assert res.status_code == 200
    data = res.get_json()
    assert data['data_type'] == 'REAL_PUBLIC_SOURCE'
    assert data['count'] > 0
    assert len(data['records']) == data['count']

def test_api_health_incidents_real(client):
    res = client.get('/api/health-incidents?data_type=REAL_PUBLIC_SOURCE')
    assert res.status_code == 200
    data = res.get_json()
    assert data['data_type'] == 'REAL_PUBLIC_SOURCE'
    assert data['count'] > 0

def test_api_data_explorer_real(client):
    res = client.get('/api/data-explorer?data_type=REAL_PUBLIC_SOURCE')
    assert res.status_code == 200
    data = res.get_json()
    assert data['data_type'] == 'REAL_PUBLIC_SOURCE'
    assert data['count'] > 0
    record = data['records'][0]
    assert 'source' in record
    assert 'provenance' in record
    assert 'available_variables' in record

def test_api_risk_monitoring_real(client):
    res = client.get('/api/risk-monitoring?data_type=REAL_PUBLIC_SOURCE')
    assert res.status_code == 200
    data = res.get_json()
    assert data['data_type'] == 'REAL_PUBLIC_SOURCE'
    assert data['count'] > 0

def test_api_data_status(client):
    res = client.get('/api/data-status')
    assert res.status_code == 200
    data = res.get_json()
    assert data['database'] == 'healthy'
    assert data['status'] == 'healthy'
    assert data['real_public_source_records'] > 0
    assert data['water_quality_records'] == 589
    assert data['rainfall_records'] == 121
    assert data['health_records'] == 15
    assert data['risk_records'] == 713
    assert data['locations'] > 0

