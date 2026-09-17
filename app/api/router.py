from fastapi import APIRouter

from app.api.routes import auth, chat, dashboards, health, users

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(dashboards.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(chat.router)

