from app.providers.mock_dashboard_provider import MockDashboardProvider
from app.schemas.common import DashboardEnvelope, FTTHMaturityIndexEnvelope


class DashboardService:
    def __init__(self, provider: MockDashboardProvider) -> None:
        self.provider = provider

    def get_dashboard(self, dashboard: str) -> DashboardEnvelope:
        return DashboardEnvelope.model_validate(self.provider.get(dashboard))

    def get_ftth_maturity_index_dashboard(self) -> FTTHMaturityIndexEnvelope:
        return FTTHMaturityIndexEnvelope.model_validate(self.provider.get("ftth_maturity_index"))
