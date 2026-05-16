"""Meal model."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Meal(Base):
    """Logged meal record."""

    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    meal_type = Column(String, nullable=True)
    source = Column(String, nullable=False, default="text")

    user = relationship("User", back_populates="meals")
    meal_items = relationship("MealItem", back_populates="meal", cascade="all, delete-orphan")
    nutrient_aggregate = relationship(
        "NutrientAggregate",
        back_populates="meal",
        uselist=False,
        cascade="all, delete-orphan",
    )
