"""User model."""
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, JSON, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    """User account and profile."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)

    age = Column(Integer, nullable=True)
    sex = Column(String, nullable=True)
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    target_weight_kg = Column(Float, nullable=True)
    activity_level = Column(String, nullable=True)

    dietary_preferences = Column(JSON, default=list)
    allergies = Column(JSON, default=list)
    cultural_preferences = Column(JSON, default=list)

    daily_calorie_target = Column(Integer, nullable=True)
    protein_target_g = Column(Float, nullable=True)
    carb_target_g = Column(Float, nullable=True)
    fat_target_g = Column(Float, nullable=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship(
        "Recommendation", back_populates="user", cascade="all, delete-orphan"
    )
