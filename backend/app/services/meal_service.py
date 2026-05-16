"""Meal service - orchestrates LLM parsing, nutrition matching, and storage."""
from datetime import date

from sqlalchemy.orm import Session

from app.models.meal import Meal
from app.models.meal_item import MealItem
from app.models.nutrient import NutrientAggregate
from app.models.user import User
from app.schemas.meal import MealItemCreate
from app.services.llm_service import parse_meal_text
from app.services.nutrition_service import (
    calculate_meal_nutrients,
    match_food_item,
)


def log_meal_from_text(
    db: Session, user: User, text: str, meal_type: str | None = None
) -> Meal:
    """Parse text with LLM, match to nutrition DB, and save meal."""
    parsed = parse_meal_text(text)
    meal_type = meal_type or parsed.get("meal_type")
    items_data = parsed.get("items", [])

    meal = Meal(user_id=user.id, meal_type=meal_type, source="text")
    db.add(meal)
    db.flush()

    for item_data in items_data:
        item = MealItem(
            meal_id=meal.id,
            food_name=item_data.get("food_name", "unknown"),
            quantity=item_data.get("quantity", 1.0),
            unit=item_data.get("unit"),
            portion_size_category=item_data.get("portion_size_category"),
            preparation_method=item_data.get("preparation_method"),
            confidence_score=item_data.get("confidence_score"),
        )
        food = match_food_item(db, item.food_name)
        if food:
            item.normalized_food_id = food.id
        db.add(item)

    db.flush()

    items = db.query(MealItem).filter(MealItem.meal_id == meal.id).all()
    nutrients = calculate_meal_nutrients(db, items)

    agg = NutrientAggregate(
        meal_id=meal.id,
        user_id=user.id,
        date=date.today(),
        calories=nutrients["calories"],
        protein_g=nutrients["protein_g"],
        carbs_g=nutrients["carbs_g"],
        fat_g=nutrients["fat_g"],
        fiber_g=nutrients["fiber_g"],
        sodium_mg=nutrients["sodium_mg"],
    )
    db.add(agg)

    db.commit()
    db.refresh(meal)
    return meal
