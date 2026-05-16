"""Nutrition service for food matching and nutrient calculation."""
from typing import Optional

from sqlalchemy.orm import Session

from app.models.food import Food
from app.models.meal_item import MealItem


def search_food(db: Session, query: str, limit: int = 5) -> list[Food]:
    """Search nutrition database for food items by name (fuzzy matching)."""
    q = f"%{query.lower()}%"
    return db.query(Food).filter(Food.name.ilike(q)).limit(limit).all()


def match_food_item(db: Session, food_name: str) -> Optional[Food]:
    """Match a parsed food name to the nutrition database. Returns best match or None."""
    name = (food_name or "").strip().lower()
    if not name:
        return None
    # Try full name first
    results = search_food(db, name, limit=3)
    if results:
        return results[0]
    # Try first word (e.g. "scrambled eggs" -> "eggs")
    first_word = name.split()[0] if name else ""
    if first_word:
        results = search_food(db, first_word, limit=3)
        if results:
            return results[0]
    # Try singular/plural: add or remove trailing 's'
    if name.endswith("s") and len(name) > 1:
        results = search_food(db, name[:-1], limit=3)
    else:
        results = search_food(db, name + "s", limit=3)
    if results:
        return results[0]
    return None


# When unit means "number of servings", we use quantity as multiplier (1 serving ≈ 100g).
_SERVING_UNITS = (
    "cup", "cups", "bowl", "bowls", "serving", "servings",
    "portion", "portions", "slice", "slices", "piece", "pieces",
    "item", "items", "pizza", "pizzas",
)


def calculate_nutrients_for_item(
    food: Food, quantity: float, unit: Optional[str] = None
) -> dict:
    """Calculate nutrients for a food item given quantity.
    - If unit is grams/g: factor = quantity/100 (grams to 100g scale).
    - If unit is a serving-type (slice, piece, bowl, etc.) or missing: factor = quantity (number of 100g servings).
    """
    unit_lower = (unit or "").strip().lower()
    if unit_lower in ("g", "gram", "grams", "gr"):
        factor = quantity / 100.0
    elif unit_lower in _SERVING_UNITS or not unit_lower:
        # No unit or "2 pizza", "2 slices" → quantity is number of servings (1 serving ≈ 100g)
        factor = max(0.1, quantity)
    else:
        # Other units (e.g. ml, tbsp): treat as approximate servings
        factor = max(0.1, quantity)
    return {
        "calories": (food.calories_per_100g or 0) * factor,
        "protein_g": (food.protein_per_100g or 0) * factor,
        "carbs_g": (food.carbs_per_100g or 0) * factor,
        "fat_g": (food.fat_per_100g or 0) * factor,
        "fiber_g": (food.fiber_per_100g or 0) * factor,
        "sodium_mg": (food.sodium_per_100g_mg or 0) * factor,
    }


# Fallback per-serving estimates when a food is not in the database (so we don't show 0)
_DEFAULT_PER_SERVING = {
    "calories": 80.0,
    "protein_g": 4.0,
    "carbs_g": 10.0,
    "fat_g": 2.0,
    "fiber_g": 1.0,
    "sodium_mg": 50.0,
}


def calculate_meal_nutrients(db: Session, meal_items: list[MealItem]) -> dict:
    """Aggregate nutrients for a list of meal items. Uses fallback estimates when food not in DB."""
    total = {
        "calories": 0.0,
        "protein_g": 0.0,
        "carbs_g": 0.0,
        "fat_g": 0.0,
        "fiber_g": 0.0,
        "sodium_mg": 0.0,
    }
    for item in meal_items:
        food = db.get(Food, item.normalized_food_id) if item.normalized_food_id else None
        if food:
            nutrients = calculate_nutrients_for_item(
                food, item.quantity, item.unit
            )
            for k in total:
                total[k] += nutrients.get(k, 0)
        else:
            # No match in DB: use a rough per-serving estimate so totals aren't zero
            qty = max(0.1, float(item.quantity or 1.0))
            for k in total:
                total[k] += _DEFAULT_PER_SERVING.get(k, 0) * qty
    return total
