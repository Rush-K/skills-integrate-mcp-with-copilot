from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_list_clubs_returns_directory_data():
    response = client.get("/clubs")

    assert response.status_code == 200
    clubs = response.json()
    assert isinstance(clubs, list)
    assert len(clubs) >= 3
    assert all("name" in club and "category" in club and "tags" in club for club in clubs)


def test_get_club_detail_returns_profile_fields():
    response = client.get("/clubs/Chess%20Club")

    assert response.status_code == 200
    club = response.json()
    assert club["name"] == "Chess Club"
    assert club["category"] == "Academic"
    assert "Strategy" in club["tags"]
    assert "leader" in club


def test_filter_clubs_by_category():
    response = client.get("/clubs?category=STEM")

    assert response.status_code == 200
    clubs = response.json()
    assert len(clubs) > 0
    assert all(club["category"] == "STEM" for club in clubs)
