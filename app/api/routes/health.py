from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Liveness")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@router.get("/ready", summary="Readiness")
def ready() -> dict[str, str]:
    return {"status": "ready"}
