"""Nutrient aggregate model."""
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class NutrientAggregate(Base):
    """Aggregated nutrients per meal or per day."""

    __tablename__ = "nutrient_aggregates"

    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)

    calories = Column(Float, nullable=True, default=0)
    protein_g = Column(Float, nullable=True, default=0)
    carbs_g = Column(Float, nullable=True, default=0)
    fat_g = Column(Float, nullable=True, default=0)
    fiber_g = Column(Float, nullable=True, default=0)
    sodium_mg = Column(Float, nullable=True, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    meal = relationship("Meal", back_populates="nutrient_aggregate")
