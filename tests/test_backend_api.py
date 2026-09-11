from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def restore_activities_state():
    original = deepcopy(activities)
    yield
    activities.clear()
    activities.update(deepcopy(original))


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_list_activities_returns_the_expected_activity_collection(client):
    # Arrange
    # No special setup needed; we rely on the in-memory data model.

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "Programming Class" in payload
    assert "Gym Class" in payload


def test_signup_adds_the_email_to_the_requested_activity_participants(client):
    # Arrange
    email = "teststudent@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_signup_rejects_a_student_already_registered_for_the_activity(client):
    # Arrange
    email = "michael@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    payload = response.json()
    assert payload["detail"] == "Student already signed up for this activity"


def test_unregister_removes_the_email_from_the_requested_activity_participants(client):
    # Arrange
    email = "michael@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]
