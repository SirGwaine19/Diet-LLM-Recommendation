"""LLM service for meal text parsing."""
import json
from typing import Any

from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

MEAL_PARSE_PROMPT = """You are a meal logging assistant. Extract structured meal data from the user's message.

Rules:
- Extract each food item with: food_name, quantity, unit (e.g., grams, cups, slices), portion_size_category (small/medium/large if unclear), preparation_method (fried, baked, grilled, etc. if mentioned)
- Set confidence_score (0-1) for each item based on how confident you are
- Infer meal_type (breakfast/lunch/dinner/snack) if possible from context
- Never invent or fabricate nutrients - only output food names and portions
- Return valid JSON only, no markdown or extra text

Output format:
{
  "meal_type": "lunch",
  "items": [
    {
      "food_name": "chicken biryani",
      "quantity": 1,
      "unit": "bowl",
      "portion_size_category": "medium",
      "preparation_method": null,
      "confidence_score": 0.9
    }
  ]
}

User message: """


def parse_meal_text(text: str) -> dict[str, Any]:
    """Parse free-form meal text into structured data using LLM."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You extract structured meal data. Return only valid JSON."},
            {"role": "user", "content": MEAL_PARSE_PROMPT + text},
        ],
        temperature=0.2,
    )
    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    return json.loads(content)
