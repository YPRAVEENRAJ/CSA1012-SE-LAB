import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'success'
    assert 'message' in json_data
    assert json_data['version'] == '1.0.0'

def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'UP'
    assert json_data['service'] == 'flask-cicd-pipeline'

def test_calc_add_endpoint(client):
    response = client.get('/api/calc/add/10/25')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['operation'] == 'addition'
    assert json_data['result'] == 35
