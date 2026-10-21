from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'online'

def test_api_import():
    assert app is not None
    assert len(app.routes) > 0
