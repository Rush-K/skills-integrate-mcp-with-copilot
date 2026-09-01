from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_request_membership_adds_student_to_pending_list():
    email = "pending.student@mergington.edu"
    response = client.post("/activities/Chess Club/request?email=" + email)

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "pending"
    assert email in client.get("/activities").json()["Chess Club"]["pending_members"]


def test_approve_membership_moves_student_into_participants():
    email = "approved.student@mergington.edu"
    client.post("/activities/Programming Class/request?email=" + email)

    response = client.post("/activities/Programming Class/approve?email=" + email)

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "approved"
    activities = client.get("/activities").json()
    assert email in activities["Programming Class"]["participants"]
    assert email not in activities["Programming Class"]["pending_members"]
