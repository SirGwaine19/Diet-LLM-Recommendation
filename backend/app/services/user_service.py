"""User service for profile and goal operations."""
from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserGoalsUpdate, UserUpdate


def update_user_profile(db: Session, user: User, data: UserUpdate) -> User:
    """Update user profile with provided data."""
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def update_user_goals(db: Session, user: User, data: UserGoalsUpdate) -> User:
    """Update user goals with provided data."""
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def get_user_profile(db: Session, user_id: int) -> Optional[User]:
    """Get user profile by ID."""
    return db.query(User).filter(User.id == user_id).first()
