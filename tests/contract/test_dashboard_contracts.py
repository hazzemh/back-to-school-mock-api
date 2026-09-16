import json
from pathlib import Path

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
DATA_DIR = Path(__file__).resolve().parents[2] / "app" / "mock_data"

CASES = [
    ("service_assurance.json", "/api/ExternalService/get_back_to_school_service_assurance_dashboard_payload", 4),
    ("complaint_intelligence.json", "/api/ExternalService/get_back_to_school_complaint_intelligence_dashboard_payload", 7),
    ("service_operations.json", "/api/ExternalService/get_back_to_school_service_operations_dashboard_payload", 7),
]


def assert_same_shape(expected, actual, path="$"):
    assert type(expected) is type(actual), f"type mismatch at {path}: {type(expected).__name__} != {type(actual).__name__}"
    if isinstance(expected, dict):
        assert set(expected) == set(actual), f"key mismatch at {path}: {set(expected) ^ set(actual)}"
        for key in expected:
            assert_same_shape(expected[key], actual[key], f"{path}.{key}")
    elif isinstance(expected, list):
        assert len(expected) == len(actual), f"list length mismatch at {path}"
        for idx, (e, a) in enumerate(zip(expected, actual)):
            assert_same_shape(e, a, f"{path}[{idx}]")


def test_dashboard_contracts_match_supplied_samples():
    for filename, url, expected_sections in CASES:
        source = json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))
        response = client.get(url)
        assert response.status_code == 200
        body = response.json()
        assert body["StatusCode"] == 200
        assert body["Messages"] is None
        assert body["DataCount"] == 0
        assert len(body["Data"]["returned_data"]["sections"]) == expected_sections
        assert_same_shape(source, body)


def test_snapshot_is_stable_inside_refresh_bucket():
    url = CASES[0][1]
    a = client.get(url).json()
    b = client.get(url).json()
    assert a == b
