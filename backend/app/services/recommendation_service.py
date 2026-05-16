"""Recommendation service for daily summaries and diet coaching."""
from datetime import date, timedelta
from typing import Any

from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.meal import Meal
from app.models.nutrient import NutrientAggregate
from app.models.recommendation import Recommendation
from app.models.user import User

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def get_user_history_summary(db: Session, user: User, days: int = 7) -> dict[str, Any]:
    """Aggregate last N days of meals and nutrients."""
    start = date.today() - timedelta(days=days)
    aggregates = (
        db.query(NutrientAggregate)
        .filter(
            NutrientAggregate.user_id == user.id,
            NutrientAggregate.date >= start,
        )
        .all()
    )
    daily_totals = {}
    for agg in aggregates:
        d = agg.date.isoformat()
        if d not in daily_totals:
            daily_totals[d] = {
                "calories": 0, "protein_g": 0, "carbs_g": 0,
                "fat_g": 0, "meals": 0,
            }
        daily_totals[d]["calories"] += agg.calories or 0
        daily_totals[d]["protein_g"] += agg.protein_g or 0
        daily_totals[d]["carbs_g"] += agg.carbs_g or 0
        daily_totals[d]["fat_g"] += agg.fat_g or 0
        daily_totals[d]["meals"] += 1
    return {"daily_totals": daily_totals, "days": days}


def calculate_daily_stats(db: Session, user: User, target_date: date) -> dict:
    """Compute daily nutrition totals for a specific date."""
    aggregates = (
        db.query(NutrientAggregate)
        .filter(
            NutrientAggregate.user_id == user.id,
            NutrientAggregate.date == target_date,
        )
        .all()
    )
    total = {
        "calories": 0.0, "protein_g": 0.0, "carbs_g": 0.0,
        "fat_g": 0.0, "meals_count": 0,
    }
    for agg in aggregates:
        total["calories"] += agg.calories or 0
        total["protein_g"] += agg.protein_g or 0
        total["carbs_g"] += agg.carbs_g or 0
        total["fat_g"] += agg.fat_g or 0
        total["meals_count"] += 1
    return total


def generate_daily_summary(
    db: Session, user: User, target_date: date | None = None
) -> Recommendation:
    """Use LLM to create a daily nutrition summary and suggestions."""
    target_date = target_date or date.today()
    stats = calculate_daily_stats(db, user, target_date)
    history = get_user_history_summary(db, user, days=7)

    profile = f"""
User: {user.full_name or 'User'}
Age: {user.age}, Sex: {user.sex}
Height: {user.height_cm} cm, Weight: {user.weight_kg} kg
Activity: {user.activity_level}
Goals: {user.daily_calorie_target} cal/day, {user.protein_target_g}g protein, {user.carb_target_g}g carbs, {user.fat_target_g}g fat
Dietary: {user.dietary_preferences}, Allergies: {user.allergies}
"""
    prompt = f"""You are a supportive, non-judgmental diet coach. Generate a brief daily summary for the user.

{profile}

Today's intake ({target_date}):
- Calories: {stats['calories']:.0f}
- Protein: {stats['protein_g']:.1f}g
- Carbs: {stats['carbs_g']:.1f}g
- Fat: {stats['fat_g']:.1f}g
- Meals logged: {stats['meals_count']}

Recent history (last 7 days): {history['daily_totals']}

Write a concise summary in exactly 4-5 lines (not paragraphs):
- Line 1: Brief positive note on today's intake
- Line 2-3: Quick comparison to goals
- Line 4-5: One actionable suggestion for tomorrow

Keep it warm and encouraging. Never shame. Be brief and direct.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    content = response.choices[0].message.content

    rec = Recommendation(
        user_id=user.id,
        type="daily",
        content=content,
        extra_metadata={
            "date": target_date.isoformat(),
            "stats": stats,
        },
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec
