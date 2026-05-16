"""Meal schemas."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class MealItemCreate(BaseModel):
    """Parsed meal item from LLM."""

    food_name: str
    quantity: float = 1.0
    unit: Optional[str] = None
    portion_size_category: Optional[str] = None
    preparation_method: Optional[str] = None
    confidence_score: Optional[float] = None


class MealCreate(BaseModel):
    """Schema for creating a meal from parsed text."""

    meal_type: Optional[str] = None
    items: List[MealItemCreate]


class MealLogRequest(BaseModel):
    """Request to log a meal via text."""

    text: str
    meal_type: Optional[str] = None


class MealItemResponse(BaseModel):
    """Meal item in response."""

    id: int
    food_name: str
    quantity: float
    unit: Optional[str] = None
    portion_size_category: Optional[str] = None
    preparation_method: Optional[str] = None

    class Config:
        from_attributes = True


class MealResponse(BaseModel):
    """Meal response schema."""

    id: int
    user_id: int
    timestamp: datetime
    meal_type: Optional[str] = None
    source: str
    items: List[MealItemResponse] = []
    calories: Optional[float] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None

    class Config:
        from_attributes = True
