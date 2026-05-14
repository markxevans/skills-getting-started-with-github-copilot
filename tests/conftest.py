import copy

from fastapi.testclient import TestClient
import pytest

from src.app import app, activities

_original_activities = copy.deepcopy(activities)

@pytest.fixture
def client():
    client = TestClient(app)
    yield client
    activities.clear()
    activities.update(copy.deepcopy(_original_activities))
