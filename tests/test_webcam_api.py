from fastapi.testclient import TestClient
from main import app
from fastapi.responses import StreamingResponse

client = TestClient(app)

def test_api_webcam_root_route():
   response = client.get('/api/webcam')
   assert response.status_code == 200
   assert response.json()['message'] == 'The webcam object recognition server is up and running'

def test_api_webcam_start_route():
   response = client.get('/api/webcam/start')
   assert response.status_code == 200
   assert response.json()['message'] == 'Webcam started successfully!'

def test_api_webcam_stop_route():
   response = client.get('/api/webcam/stop')
   assert response.status_code == 200
   assert response.json()['message'] == 'Webcam stoped successfully!'

def test_api_webcam_status_route():
   response = client.get('/api/webcam/status')
   assert response.status_code == 200
   assert 'is_active' in response.json()

def test_api_webcam_stream_route():
   response = client.get('/api/webcam/stream')
   assert response.status_code == 200
