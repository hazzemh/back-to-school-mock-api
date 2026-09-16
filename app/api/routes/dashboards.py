from fastapi import APIRouter, Depends

from app.api.dependencies import get_dashboard_service
from app.schemas.common import DashboardEnvelope, FTTHMaturityIndexEnvelope
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/api/ExternalService", tags=["Dashboard APIs"])


@router.get(
    "/get_back_to_school_service_assurance_dashboard_payload",
    response_model=DashboardEnvelope,
    summary="B2S1 Service Assurance Dashboard",
    description="Mock-compatible implementation of the supplied B2S1 dashboard payload contract.",
)
def service_assurance(service: DashboardService = Depends(get_dashboard_service)) -> DashboardEnvelope:
    return service.get_dashboard("service_assurance")


@router.get(
    "/get_back_to_school_complaint_intelligence_dashboard_payload",
    response_model=DashboardEnvelope,
    summary="B2S2 Complaint Intelligence Dashboard",
    description="Mock-compatible implementation of the supplied B2S2 dashboard payload contract.",
)
def complaint_intelligence(service: DashboardService = Depends(get_dashboard_service)) -> DashboardEnvelope:
    return service.get_dashboard("complaint_intelligence")


@router.get(
    "/get_back_to_school_service_operations_dashboard_payload",
    response_model=DashboardEnvelope,
    summary="B2S3 Service Operations Dashboard",
    description="Mock-compatible implementation of the supplied B2S3 dashboard payload contract.",
)
def service_operations(service: DashboardService = Depends(get_dashboard_service)) -> DashboardEnvelope:
    return service.get_dashboard("service_operations")


@router.get(
    "/get_back_to_school_ftth_maturity_index_dashboard_payload",
    response_model=FTTHMaturityIndexEnvelope,
    summary="B2S4 FTTH Maturity Index Dashboard",
    description="Mock-compatible implementation of the supplied FTTH Maturity Index dashboard payload contract.",
)
def ftth_maturity_index(service: DashboardService = Depends(get_dashboard_service)) -> FTTHMaturityIndexEnvelope:
    return service.get_ftth_maturity_index_dashboard()
