"""API v1 router - imports all route modules and includes sub-routers with auth where needed."""
from fastapi import APIRouter, Depends

from app.api.v1 import auth, meals, recommendations, users
from app.core.dependencies import get_current_user

api_router = APIRouter()

# Auth routes: register and login are public; /me requires auth (handled in route)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Protected routes: all require authentication
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)],
)
api_router.include_router(
    meals.router,
    prefix="/meals",
    tags=["meals"],
    dependencies=[Depends(get_current_user)],
)
api_router.include_router(
    recommendations.router,
    prefix="/recommendations",
    tags=["recommendations"],
    dependencies=[Depends(get_current_user)],
)
