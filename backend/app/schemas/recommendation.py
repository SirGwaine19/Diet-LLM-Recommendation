"""Recommendation schemas."""
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class RecommendationCreate(BaseModel):
    """Schema for creating a recommendation."""

    type: str
    content: str
    metadata: Optional[dict[str, Any]] = None


class RecommendationResponse(BaseModel):
    """Recommendation response schema."""

    id: int
    user_id: int
    type: str
    content: str
    generated_at: datetime
    user_feedback: Optional[str] = None

    class Config:
        from_attributes = True


class RecommendationFeedback(BaseModel):
    """User feedback on a recommendation."""

    feedback: str
