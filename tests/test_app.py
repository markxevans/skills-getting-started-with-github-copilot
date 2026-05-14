from urllib.parse import quote

from src.app import activities


def test_get_activities(client):
    # Arrange
    expected_participants = ["michael@mergington.edu", "daniel@mergington.edu"]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["participants"] == expected_participants
    assert data["Chess Club"]["max_participants"] == 12


def test_signup_adds_participant(client):
    # Arrange
    email = "newstudent@mergington.edu"
    activity_name = quote("Chess Club")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={quote(email)}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    refreshed = client.get("/activities").json()
    assert email in refreshed["Chess Club"]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    email = "michael@mergington.edu"
    activity_name = quote("Chess Club")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={quote(email)}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant(client):
    # Arrange
    email = "michael@mergington.edu"
    activity_name = quote("Chess Club")

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={quote(email)}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"

    refreshed = client.get("/activities").json()
    assert email not in refreshed["Chess Club"]["participants"]


def test_remove_missing_participant_returns_404(client):
    # Arrange
    email = "missing@mergington.edu"
    activity_name = quote("Chess Club")

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={quote(email)}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
