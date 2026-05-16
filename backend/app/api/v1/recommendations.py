"""Recommendation API routes."""
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.recommendation import Recommendation
from app.models.user import User
from app.schemas.recommendation import RecommendationFeedback, RecommendationResponse
from app.services.recommendation_service import generate_daily_summary

router = APIRouter()


@router.get("/daily", response_model=RecommendationResponse | None)
def get_daily(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """Get today's daily summary if it exists."""
    today = date.today()
    rec = (
        db.query(Recommendation)
        .filter(
            Recommendation.user_id == current_user.id,
            Recommendation.type == "daily",
            func.date(Recommendation.generated_at) == today,
        )
        .order_by(Recommendation.generated_at.desc())
        .first()
    )
    if rec:
        return rec
    return None


@router.post("/generate", response_model=RecommendationResponse)
def generate(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """Manually trigger daily summary generation."""
    rec = generate_daily_summary(db, current_user, date.today())
    return rec


@router.post("/{recommendation_id}/feedback")
def feedback(
    recommendation_id: int,
    data: RecommendationFeedback,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """Record user feedback on a recommendation."""
    rec = (
        db.query(Recommendation)
        .filter(
            Recommendation.id == recommendation_id,
            Recommendation.user_id == current_user.id,
        )
        .first()
    )
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    rec.user_feedback = data.feedback
    db.commit()
    return {"ok": True}
