"""Meal logging API routes."""
import logging
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

logger = logging.getLogger(__name__)
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.meal import Meal
from app.models.user import User
from app.schemas.meal import MealLogRequest, MealResponse
from app.services.meal_service import log_meal_from_text

router = APIRouter()


@router.post("/log", response_model=MealResponse)
def log_meal(
    data: MealLogRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """Log a meal from free-form text."""
    try:
        meal = log_meal_from_text(db, current_user, data.text, data.meal_type)
    except Exception as e:
        logger.exception("Meal log failed: %s", e)
        err_msg = str(e).strip() or "Unknown error"
        if "insufficient_quota" in err_msg.lower() or "429" in err_msg:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="OpenAI quota exceeded. Add billing at https://platform.openai.com/account/billing to use meal logging.",
            ) from e
        if "openai" in err_msg.lower() or "api_key" in err_msg.lower() or "authentication" in err_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Meal parsing failed: check OPENAI_API_KEY in backend/.env and that the key is valid.",
            ) from e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Meal logging failed: {err_msg}",
        ) from e
    nutrient = meal.nutrient_aggregate
    return MealResponse(
        id=meal.id,
        user_id=meal.user_id,
        timestamp=meal.timestamp,
        meal_type=meal.meal_type,
        source=meal.source,
        items=[
            {
                "id": i.id,
                "food_name": i.food_name,
                "quantity": i.quantity,
                "unit": i.unit,
                "portion_size_category": i.portion_size_category,
                "preparation_method": i.preparation_method,
            }
            for i in meal.meal_items
        ],
        calories=nutrient.calories if nutrient else None,
        protein_g=nutrient.protein_g if nutrient else None,
        carbs_g=nutrient.carbs_g if nutrient else None,
        fat_g=nutrient.fat_g if nutrient else None,
    )


@router.get("", response_model=list[MealResponse])
def get_meals(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    limit: int = 50,
    start_date: date | None = None,
    end_date: date | None = None,
):
    """Get current user's meal history."""
    query = db.query(Meal).filter(Meal.user_id == current_user.id)
    if start_date:
        query = query.filter(func.date(Meal.timestamp) >= start_date)
    if end_date:
        query = query.filter(func.date(Meal.timestamp) <= end_date)

    meals = query.order_by(Meal.timestamp.desc()).limit(limit).all()
    return [
        MealResponse(
            id=m.id,
            user_id=m.user_id,
            timestamp=m.timestamp,
            meal_type=m.meal_type,
            source=m.source,
            items=[
                {
                    "id": i.id,
                    "food_name": i.food_name,
                    "quantity": i.quantity,
                    "unit": i.unit,
                    "portion_size_category": i.portion_size_category,
                    "preparation_method": i.preparation_method,
                }
                for i in m.meal_items
            ],
            calories=m.nutrient_aggregate.calories if m.nutrient_aggregate else None,
            protein_g=m.nutrient_aggregate.protein_g if m.nutrient_aggregate else None,
            carbs_g=m.nutrient_aggregate.carbs_g if m.nutrient_aggregate else None,
            fat_g=m.nutrient_aggregate.fat_g if m.nutrient_aggregate else None,
        )
        for m in meals
    ]


@router.get("/{meal_id}", response_model=MealResponse)
def get_meal(
    meal_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """Get a specific meal by ID."""
    meal = db.query(Meal).filter(Meal.id == meal_id, Meal.user_id == current_user.id).first()
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")
    nutrient = meal.nutrient_aggregate
    return MealResponse(
        id=meal.id,
        user_id=meal.user_id,
        timestamp=meal.timestamp,
        meal_type=meal.meal_type,
        source=meal.source,
        items=[
            {
                "id": i.id,
                "food_name": i.food_name,
                "quantity": i.quantity,
                "unit": i.unit,
                "portion_size_category": i.portion_size_category,
                "preparation_method": i.preparation_method,
            }
            for i in meal.meal_items
        ],
        calories=nutrient.calories if nutrient else None,
        protein_g=nutrient.protein_g if nutrient else None,
        carbs_g=nutrient.carbs_g if nutrient else None,
        fat_g=nutrient.fat_g if nutrient else None,
    )


@router.delete("/{meal_id}")
def delete_meal(
    meal_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """Delete a meal."""
    meal = db.query(Meal).filter(Meal.id == meal_id, Meal.user_id == current_user.id).first()
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")
    db.delete(meal)
    db.commit()
    return {"ok": True}
