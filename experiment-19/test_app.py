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
    assert 'GitHub Actions' in json_data['message']
    assert 'version' in json_data

def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'UP'
    assert json_data['service'] == 'flask-cd-github-actions'

def test_calc_add_endpoint(client):
    response = client.get('/api/calc/add/10/25')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['operation'] == 'addition'
    assert json_data['result'] == 35

def test_calc_multiply_endpoint(client):
    response = client.get('/api/calc/multiply/6/7')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['operation'] == 'multiplication'
    assert json_data['result'] == 42
