"""User management API routes."""
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserGoalsUpdate, UserResponse, UserUpdate
from app.services.user_service import update_user_goals, update_user_profile

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Get current user profile."""
    return current_user


@router.put("/me", response_model=UserResponse)
def update_me(
    data: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """Update current user profile."""
    return update_user_profile(db, current_user, data)


@router.get("/me/goals")
def get_goals(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Get current user goals."""
    return {
        "daily_calorie_target": current_user.daily_calorie_target,
        "protein_target_g": current_user.protein_target_g,
        "carb_target_g": current_user.carb_target_g,
        "fat_target_g": current_user.fat_target_g,
    }


@router.put("/me/goals")
def put_goals(
    data: UserGoalsUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """Update current user goals."""
    return update_user_goals(db, current_user, data)
