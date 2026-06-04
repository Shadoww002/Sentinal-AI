from fastapi.testclient import TestClient
from backend.api.main import app
#creating the client 

client = TestClient(app)

def test_obvious_false_claim():
    response = client.post("/api/v1/verify", json={"text": "The moon is made entirely of green cheese and was discovered by a mouse."})
    assert response.status_code == 200
    data = response.json()
    # Expect the system to either find contradiction or remain unverified
    assert data["overall_verdict"] in ["Misleading/False", "Unverified"]
