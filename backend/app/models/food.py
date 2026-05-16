"""Food model for nutrition database."""
from sqlalchemy import Column, Float, Integer, String

from app.core.database import Base


class Food(Base):
    """Nutrition database food entry."""

    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)

    calories_per_100g = Column(Float, nullable=True, default=0)
    protein_per_100g = Column(Float, nullable=True, default=0)
    carbs_per_100g = Column(Float, nullable=True, default=0)
    fat_per_100g = Column(Float, nullable=True, default=0)
    fiber_per_100g = Column(Float, nullable=True, default=0)
    sodium_per_100g_mg = Column(Float, nullable=True, default=0)
