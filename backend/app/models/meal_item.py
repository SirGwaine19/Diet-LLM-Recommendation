"""Meal item model."""
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class MealItem(Base):
    """Individual food item within a meal."""

    __tablename__ = "meal_items"

    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    food_name = Column(String, nullable=False)
    normalized_food_id = Column(Integer, ForeignKey("foods.id"), nullable=True)
    quantity = Column(Float, nullable=False, default=1.0)
    unit = Column(String, nullable=True)

    portion_size_category = Column(String, nullable=True)
    preparation_method = Column(String, nullable=True)
    confidence_score = Column(Float, nullable=True)

    meal = relationship("Meal", back_populates="meal_items")
