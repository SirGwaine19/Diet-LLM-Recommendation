"""Seed common foods into the nutrition database."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.food import Food
from app.core.database import Base

engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)

COMMON_FOODS = [
    # Grains & staples
    {"name": "rice", "calories_per_100g": 130, "protein_per_100g": 2.7, "carbs_per_100g": 28, "fat_per_100g": 0.3, "fiber_per_100g": 0.4, "sodium_per_100g_mg": 1},
    {"name": "bread", "calories_per_100g": 265, "protein_per_100g": 9, "carbs_per_100g": 49, "fat_per_100g": 3.2, "fiber_per_100g": 2.7, "sodium_per_100g_mg": 491},
    {"name": "toast", "calories_per_100g": 265, "protein_per_100g": 9, "carbs_per_100g": 49, "fat_per_100g": 3.2, "fiber_per_100g": 2.7, "sodium_per_100g_mg": 491},
    {"name": "pasta", "calories_per_100g": 131, "protein_per_100g": 5, "carbs_per_100g": 25, "fat_per_100g": 1.1, "fiber_per_100g": 1.8, "sodium_per_100g_mg": 6},
    {"name": "oats", "calories_per_100g": 389, "protein_per_100g": 17, "carbs_per_100g": 66, "fat_per_100g": 7, "fiber_per_100g": 11, "sodium_per_100g_mg": 2},
    {"name": "chapati", "calories_per_100g": 297, "protein_per_100g": 11, "carbs_per_100g": 46, "fat_per_100g": 7.5, "fiber_per_100g": 4.9, "sodium_per_100g_mg": 409},
    {"name": "roti", "calories_per_100g": 297, "protein_per_100g": 11, "carbs_per_100g": 46, "fat_per_100g": 7.5, "fiber_per_100g": 4.9, "sodium_per_100g_mg": 409},
    {"name": "paratha", "calories_per_100g": 326, "protein_per_100g": 6.4, "carbs_per_100g": 46, "fat_per_100g": 14, "fiber_per_100g": 2.2, "sodium_per_100g_mg": 452},
    {"name": "idli", "calories_per_100g": 106, "protein_per_100g": 3.5, "carbs_per_100g": 21, "fat_per_100g": 0.4, "fiber_per_100g": 1.2, "sodium_per_100g_mg": 398},
    {"name": "dosa", "calories_per_100g": 168, "protein_per_100g": 4.2, "carbs_per_100g": 27, "fat_per_100g": 4.9, "fiber_per_100g": 1.3, "sodium_per_100g_mg": 273},
    {"name": "upma", "calories_per_100g": 140, "protein_per_100g": 3.2, "carbs_per_100g": 22, "fat_per_100g": 4.5, "fiber_per_100g": 1.1, "sodium_per_100g_mg": 350},
    # Proteins
    {"name": "chicken breast", "calories_per_100g": 165, "protein_per_100g": 31, "carbs_per_100g": 0, "fat_per_100g": 3.6, "fiber_per_100g": 0, "sodium_per_100g_mg": 74},
    {"name": "chicken", "calories_per_100g": 165, "protein_per_100g": 31, "carbs_per_100g": 0, "fat_per_100g": 3.6, "fiber_per_100g": 0, "sodium_per_100g_mg": 74},
    {"name": "fish", "calories_per_100g": 120, "protein_per_100g": 20, "carbs_per_100g": 0, "fat_per_100g": 4, "fiber_per_100g": 0, "sodium_per_100g_mg": 60},
    {"name": "salmon", "calories_per_100g": 208, "protein_per_100g": 20, "carbs_per_100g": 0, "fat_per_100g": 13, "fiber_per_100g": 0, "sodium_per_100g_mg": 59},
    {"name": "paneer", "calories_per_100g": 265, "protein_per_100g": 18, "carbs_per_100g": 3.5, "fat_per_100g": 20, "fiber_per_100g": 0, "sodium_per_100g_mg": 16},
    {"name": "tofu", "calories_per_100g": 76, "protein_per_100g": 8, "carbs_per_100g": 1.9, "fat_per_100g": 4.8, "fiber_per_100g": 0.3, "sodium_per_100g_mg": 7},
    {"name": "dal", "calories_per_100g": 116, "protein_per_100g": 9, "carbs_per_100g": 20, "fat_per_100g": 0.4, "fiber_per_100g": 7.9, "sodium_per_100g_mg": 2},
    {"name": "lentils", "calories_per_100g": 116, "protein_per_100g": 9, "carbs_per_100g": 20, "fat_per_100g": 0.4, "fiber_per_100g": 7.9, "sodium_per_100g_mg": 2},
    {"name": "sambar", "calories_per_100g": 75, "protein_per_100g": 3.5, "carbs_per_100g": 11, "fat_per_100g": 2, "fiber_per_100g": 2.2, "sodium_per_100g_mg": 450},
    {"name": "beef", "calories_per_100g": 250, "protein_per_100g": 26, "carbs_per_100g": 0, "fat_per_100g": 15, "fiber_per_100g": 0, "sodium_per_100g_mg": 72},
    {"name": "lamb", "calories_per_100g": 294, "protein_per_100g": 25, "carbs_per_100g": 0, "fat_per_100g": 21, "fiber_per_100g": 0, "sodium_per_100g_mg": 72},
    {"name": "prawns", "calories_per_100g": 99, "protein_per_100g": 24, "carbs_per_100g": 0.2, "fat_per_100g": 0.3, "fiber_per_100g": 0, "sodium_per_100g_mg": 111},
    {"name": "shrimp", "calories_per_100g": 99, "protein_per_100g": 24, "carbs_per_100g": 0.2, "fat_per_100g": 0.3, "fiber_per_100g": 0, "sodium_per_100g_mg": 111},
    # Dairy & fats
    {"name": "butter", "calories_per_100g": 717, "protein_per_100g": 0.9, "carbs_per_100g": 0.1, "fat_per_100g": 81, "fiber_per_100g": 0, "sodium_per_100g_mg": 11},
    {"name": "milk", "calories_per_100g": 42, "protein_per_100g": 3.4, "carbs_per_100g": 5, "fat_per_100g": 1, "fiber_per_100g": 0, "sodium_per_100g_mg": 44},
    {"name": "yogurt", "calories_per_100g": 59, "protein_per_100g": 10, "carbs_per_100g": 3.6, "fat_per_100g": 0.4, "fiber_per_100g": 0, "sodium_per_100g_mg": 36},
    {"name": "curd", "calories_per_100g": 59, "protein_per_100g": 10, "carbs_per_100g": 3.6, "fat_per_100g": 0.4, "fiber_per_100g": 0, "sodium_per_100g_mg": 36},
    {"name": "cheese", "calories_per_100g": 402, "protein_per_100g": 25, "carbs_per_100g": 1.3, "fat_per_100g": 33, "fiber_per_100g": 0, "sodium_per_100g_mg": 621},
    {"name": "ghee", "calories_per_100g": 900, "protein_per_100g": 0, "carbs_per_100g": 0, "fat_per_100g": 100, "fiber_per_100g": 0, "sodium_per_100g_mg": 0},
    # Eggs
    {"name": "eggs", "calories_per_100g": 155, "protein_per_100g": 13, "carbs_per_100g": 1.1, "fat_per_100g": 11, "fiber_per_100g": 0, "sodium_per_100g_mg": 124},
    {"name": "egg", "calories_per_100g": 155, "protein_per_100g": 13, "carbs_per_100g": 1.1, "fat_per_100g": 11, "fiber_per_100g": 0, "sodium_per_100g_mg": 124},
    # Fruits
    {"name": "apple", "calories_per_100g": 52, "protein_per_100g": 0.3, "carbs_per_100g": 14, "fat_per_100g": 0.2, "fiber_per_100g": 2.4, "sodium_per_100g_mg": 1},
    {"name": "banana", "calories_per_100g": 89, "protein_per_100g": 1.1, "carbs_per_100g": 23, "fat_per_100g": 0.3, "fiber_per_100g": 2.6, "sodium_per_100g_mg": 1},
    {"name": "orange", "calories_per_100g": 47, "protein_per_100g": 0.9, "carbs_per_100g": 12, "fat_per_100g": 0.1, "fiber_per_100g": 2.4, "sodium_per_100g_mg": 0},
    {"name": "orange juice", "calories_per_100g": 45, "protein_per_100g": 0.7, "carbs_per_100g": 10, "fat_per_100g": 0.2, "fiber_per_100g": 0.2, "sodium_per_100g_mg": 1},
    {"name": "mango", "calories_per_100g": 60, "protein_per_100g": 0.8, "carbs_per_100g": 15, "fat_per_100g": 0.4, "fiber_per_100g": 1.6, "sodium_per_100g_mg": 1},
    {"name": "grapes", "calories_per_100g": 69, "protein_per_100g": 0.7, "carbs_per_100g": 18, "fat_per_100g": 0.2, "fiber_per_100g": 0.9, "sodium_per_100g_mg": 0},
    {"name": "watermelon", "calories_per_100g": 30, "protein_per_100g": 0.6, "carbs_per_100g": 7.6, "fat_per_100g": 0.2, "fiber_per_100g": 0.4, "sodium_per_100g_mg": 1},
    {"name": "papaya", "calories_per_100g": 43, "protein_per_100g": 0.5, "carbs_per_100g": 11, "fat_per_100g": 0.3, "fiber_per_100g": 1.7, "sodium_per_100g_mg": 8},
    {"name": "pomegranate", "calories_per_100g": 83, "protein_per_100g": 1.7, "carbs_per_100g": 19, "fat_per_100g": 1.2, "fiber_per_100g": 4, "sodium_per_100g_mg": 3},
    {"name": "strawberry", "calories_per_100g": 32, "protein_per_100g": 0.7, "carbs_per_100g": 7.7, "fat_per_100g": 0.3, "fiber_per_100g": 2, "sodium_per_100g_mg": 1},
    {"name": "avocado", "calories_per_100g": 160, "protein_per_100g": 2, "carbs_per_100g": 9, "fat_per_100g": 15, "fiber_per_100g": 7, "sodium_per_100g_mg": 7},
    # Vegetables
    {"name": "salad", "calories_per_100g": 15, "protein_per_100g": 1.2, "carbs_per_100g": 2.9, "fat_per_100g": 0.2, "fiber_per_100g": 1.2, "sodium_per_100g_mg": 28},
    {"name": "potato", "calories_per_100g": 77, "protein_per_100g": 2, "carbs_per_100g": 17, "fat_per_100g": 0.1, "fiber_per_100g": 2.2, "sodium_per_100g_mg": 6},
    {"name": "tomato", "calories_per_100g": 18, "protein_per_100g": 0.9, "carbs_per_100g": 3.9, "fat_per_100g": 0.2, "fiber_per_100g": 1.2, "sodium_per_100g_mg": 5},
    {"name": "onion", "calories_per_100g": 40, "protein_per_100g": 1.1, "carbs_per_100g": 9, "fat_per_100g": 0.1, "fiber_per_100g": 1.7, "sodium_per_100g_mg": 4},
    {"name": "spinach", "calories_per_100g": 23, "protein_per_100g": 2.9, "carbs_per_100g": 3.6, "fat_per_100g": 0.4, "fiber_per_100g": 2.2, "sodium_per_100g_mg": 79},
    {"name": "broccoli", "calories_per_100g": 34, "protein_per_100g": 2.8, "carbs_per_100g": 7, "fat_per_100g": 0.4, "fiber_per_100g": 2.6, "sodium_per_100g_mg": 33},
    {"name": "carrot", "calories_per_100g": 41, "protein_per_100g": 0.9, "carbs_per_100g": 10, "fat_per_100g": 0.2, "fiber_per_100g": 2.8, "sodium_per_100g_mg": 69},
    {"name": "cucumber", "calories_per_100g": 15, "protein_per_100g": 0.7, "carbs_per_100g": 3.6, "fat_per_100g": 0.1, "fiber_per_100g": 0.5, "sodium_per_100g_mg": 2},
    {"name": "beans", "calories_per_100g": 31, "protein_per_100g": 1.8, "carbs_per_100g": 7, "fat_per_100g": 0.1, "fiber_per_100g": 2.7, "sodium_per_100g_mg": 6},
    {"name": "cauliflower", "calories_per_100g": 25, "protein_per_100g": 1.9, "carbs_per_100g": 5, "fat_per_100g": 0.3, "fiber_per_100g": 2, "sodium_per_100g_mg": 30},
    {"name": "cabbage", "calories_per_100g": 25, "protein_per_100g": 1.3, "carbs_per_100g": 6, "fat_per_100g": 0.1, "fiber_per_100g": 2.5, "sodium_per_100g_mg": 18},
    {"name": "brinjal", "calories_per_100g": 25, "protein_per_100g": 1, "carbs_per_100g": 6, "fat_per_100g": 0.2, "fiber_per_100g": 3, "sodium_per_100g_mg": 2},
    {"name": "eggplant", "calories_per_100g": 25, "protein_per_100g": 1, "carbs_per_100g": 6, "fat_per_100g": 0.2, "fiber_per_100g": 3, "sodium_per_100g_mg": 2},
    {"name": "ladies finger", "calories_per_100g": 33, "protein_per_100g": 1.9, "carbs_per_100g": 7.5, "fat_per_100g": 0.2, "fiber_per_100g": 3.2, "sodium_per_100g_mg": 7},
    {"name": "okra", "calories_per_100g": 33, "protein_per_100g": 1.9, "carbs_per_100g": 7.5, "fat_per_100g": 0.2, "fiber_per_100g": 3.2, "sodium_per_100g_mg": 7},
    # Indian dishes & snacks
    {"name": "biryani", "calories_per_100g": 200, "protein_per_100g": 6, "carbs_per_100g": 28, "fat_per_100g": 7, "fiber_per_100g": 0.5, "sodium_per_100g_mg": 450},
    {"name": "chicken curry", "calories_per_100g": 180, "protein_per_100g": 15, "carbs_per_100g": 5, "fat_per_100g": 12, "fiber_per_100g": 0.8, "sodium_per_100g_mg": 350},
    {"name": "curry", "calories_per_100g": 180, "protein_per_100g": 15, "carbs_per_100g": 5, "fat_per_100g": 12, "fiber_per_100g": 0.8, "sodium_per_100g_mg": 350},
    {"name": "lassi", "calories_per_100g": 80, "protein_per_100g": 3, "carbs_per_100g": 12, "fat_per_100g": 2, "fiber_per_100g": 0, "sodium_per_100g_mg": 50},
    {"name": "chai", "calories_per_100g": 30, "protein_per_100g": 1.5, "carbs_per_100g": 4, "fat_per_100g": 1, "fiber_per_100g": 0, "sodium_per_100g_mg": 25},
    {"name": "tea", "calories_per_100g": 1, "protein_per_100g": 0, "carbs_per_100g": 0, "fat_per_100g": 0, "fiber_per_100g": 0, "sodium_per_100g_mg": 4},
    {"name": "coffee", "calories_per_100g": 2, "protein_per_100g": 0.1, "carbs_per_100g": 0, "fat_per_100g": 0, "fiber_per_100g": 0, "sodium_per_100g_mg": 2},
    {"name": "vada", "calories_per_100g": 220, "protein_per_100g": 5.5, "carbs_per_100g": 28, "fat_per_100g": 10, "fiber_per_100g": 1.5, "sodium_per_100g_mg": 420},
    {"name": "pakora", "calories_per_100g": 250, "protein_per_100g": 5, "carbs_per_100g": 22, "fat_per_100g": 16, "fiber_per_100g": 2, "sodium_per_100g_mg": 400},
    {"name": "samosa", "calories_per_100g": 260, "protein_per_100g": 4.2, "carbs_per_100g": 31, "fat_per_100g": 13, "fiber_per_100g": 2.1, "sodium_per_100g_mg": 450},
    {"name": "pav bhaji", "calories_per_100g": 160, "protein_per_100g": 4, "carbs_per_100g": 22, "fat_per_100g": 6, "fiber_per_100g": 2.5, "sodium_per_100g_mg": 520},
    {"name": "poha", "calories_per_100g": 130, "protein_per_100g": 2.8, "carbs_per_100g": 26, "fat_per_100g": 2.5, "fiber_per_100g": 1.2, "sodium_per_100g_mg": 320},
    {"name": "halwa", "calories_per_100g": 350, "protein_per_100g": 4, "carbs_per_100g": 45, "fat_per_100g": 16, "fiber_per_100g": 1, "sodium_per_100g_mg": 80},
    {"name": "gulab jamun", "calories_per_100g": 320, "protein_per_100g": 5.5, "carbs_per_100g": 45, "fat_per_100g": 12, "fiber_per_100g": 0.5, "sodium_per_100g_mg": 120},
    {"name": "jalebi", "calories_per_100g": 260, "protein_per_100g": 3, "carbs_per_100g": 45, "fat_per_100g": 8, "fiber_per_100g": 0.5, "sodium_per_100g_mg": 50},
    # Western & fast food
    {"name": "pizza", "calories_per_100g": 266, "protein_per_100g": 11, "carbs_per_100g": 33, "fat_per_100g": 10, "fiber_per_100g": 2.3, "sodium_per_100g_mg": 598},
    {"name": "burger", "calories_per_100g": 295, "protein_per_100g": 17, "carbs_per_100g": 24, "fat_per_100g": 14, "fiber_per_100g": 1.2, "sodium_per_100g_mg": 497},
    {"name": "sandwich", "calories_per_100g": 250, "protein_per_100g": 11, "carbs_per_100g": 28, "fat_per_100g": 11, "fiber_per_100g": 1.5, "sodium_per_100g_mg": 580},
    {"name": "fries", "calories_per_100g": 312, "protein_per_100g": 3.4, "carbs_per_100g": 41, "fat_per_100g": 15, "fiber_per_100g": 3.8, "sodium_per_100g_mg": 210},
    {"name": "fried chicken", "calories_per_100g": 260, "protein_per_100g": 20, "carbs_per_100g": 9, "fat_per_100g": 16, "fiber_per_100g": 0.3, "sodium_per_100g_mg": 600},
    {"name": "noodles", "calories_per_100g": 138, "protein_per_100g": 4.5, "carbs_per_100g": 25, "fat_per_100g": 2.1, "fiber_per_100g": 1.2, "sodium_per_100g_mg": 450},
    {"name": "soup", "calories_per_100g": 35, "protein_per_100g": 2, "carbs_per_100g": 4, "fat_per_100g": 1, "fiber_per_100g": 0.5, "sodium_per_100g_mg": 350},
    # Beverages
    {"name": "coca cola", "calories_per_100g": 42, "protein_per_100g": 0, "carbs_per_100g": 11, "fat_per_100g": 0, "fiber_per_100g": 0, "sodium_per_100g_mg": 4},
    {"name": "cola", "calories_per_100g": 42, "protein_per_100g": 0, "carbs_per_100g": 11, "fat_per_100g": 0, "fiber_per_100g": 0, "sodium_per_100g_mg": 4},
    {"name": "smoothie", "calories_per_100g": 60, "protein_per_100g": 1.5, "carbs_per_100g": 12, "fat_per_100g": 0.5, "fiber_per_100g": 1, "sodium_per_100g_mg": 15},
    {"name": "juice", "calories_per_100g": 45, "protein_per_100g": 0.5, "carbs_per_100g": 11, "fat_per_100g": 0.1, "fiber_per_100g": 0.2, "sodium_per_100g_mg": 2},
    {"name": "water", "calories_per_100g": 0, "protein_per_100g": 0, "carbs_per_100g": 0, "fat_per_100g": 0, "fiber_per_100g": 0, "sodium_per_100g_mg": 0},
    # Nuts & snacks
    {"name": "almonds", "calories_per_100g": 579, "protein_per_100g": 21, "carbs_per_100g": 22, "fat_per_100g": 50, "fiber_per_100g": 12.5, "sodium_per_100g_mg": 1},
    {"name": "cashew", "calories_per_100g": 553, "protein_per_100g": 18, "carbs_per_100g": 30, "fat_per_100g": 44, "fiber_per_100g": 3.3, "sodium_per_100g_mg": 12},
    {"name": "peanuts", "calories_per_100g": 567, "protein_per_100g": 26, "carbs_per_100g": 16, "fat_per_100g": 49, "fiber_per_100g": 8.5, "sodium_per_100g_mg": 18},
    {"name": "walnuts", "calories_per_100g": 654, "protein_per_100g": 15, "carbs_per_100g": 14, "fat_per_100g": 65, "fiber_per_100g": 6.7, "sodium_per_100g_mg": 2},
    {"name": "biscuit", "calories_per_100g": 450, "protein_per_100g": 7, "carbs_per_100g": 65, "fat_per_100g": 18, "fiber_per_100g": 2, "sodium_per_100g_mg": 350},
    {"name": "cookie", "calories_per_100g": 502, "protein_per_100g": 5, "carbs_per_100g": 65, "fat_per_100g": 24, "fiber_per_100g": 2.5, "sodium_per_100g_mg": 350},
    {"name": "chips", "calories_per_100g": 536, "protein_per_100g": 7, "carbs_per_100g": 50, "fat_per_100g": 35, "fiber_per_100g": 4.5, "sodium_per_100g_mg": 550},
    {"name": "chocolate", "calories_per_100g": 546, "protein_per_100g": 5, "carbs_per_100g": 61, "fat_per_100g": 31, "fiber_per_100g": 2.2, "sodium_per_100g_mg": 24},
    {"name": "ice cream", "calories_per_100g": 207, "protein_per_100g": 3.5, "carbs_per_100g": 24, "fat_per_100g": 11, "fiber_per_100g": 0.7, "sodium_per_100g_mg": 80},
    {"name": "cake", "calories_per_100g": 389, "protein_per_100g": 5.3, "carbs_per_100g": 53, "fat_per_100g": 15, "fiber_per_100g": 0.6, "sodium_per_100g_mg": 315},
]

def main():
    db = Session()
    try:
        for f in COMMON_FOODS:
            if not db.query(Food).filter(Food.name == f["name"]).first():
                db.add(Food(**f))
        db.commit()
        print("Seeded foods successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
