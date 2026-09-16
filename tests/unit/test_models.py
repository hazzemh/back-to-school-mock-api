import json
from pathlib import Path
from app.schemas.common import DashboardEnvelope


def test_all_source_fixtures_validate():
    data_dir = Path(__file__).resolve().parents[2] / "app" / "mock_data"
    for filename in ["service_assurance.json", "complaint_intelligence.json", "service_operations.json"]:
        DashboardEnvelope.model_validate_json((data_dir / filename).read_text(encoding="utf-8"))
