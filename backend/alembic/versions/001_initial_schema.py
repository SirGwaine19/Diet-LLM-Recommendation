"""Initial schema

Revision ID: 001
Revises:
Create Date: 2025-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("sex", sa.String(), nullable=True),
        sa.Column("height_cm", sa.Float(), nullable=True),
        sa.Column("weight_kg", sa.Float(), nullable=True),
        sa.Column("target_weight_kg", sa.Float(), nullable=True),
        sa.Column("activity_level", sa.String(), nullable=True),
        sa.Column("dietary_preferences", sa.JSON(), nullable=True),
        sa.Column("allergies", sa.JSON(), nullable=True),
        sa.Column("cultural_preferences", sa.JSON(), nullable=True),
        sa.Column("daily_calorie_target", sa.Integer(), nullable=True),
        sa.Column("protein_target_g", sa.Float(), nullable=True),
        sa.Column("carb_target_g", sa.Float(), nullable=True),
        sa.Column("fat_target_g", sa.Float(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True, default=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.create_table(
        "foods",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("calories_per_100g", sa.Float(), nullable=True, default=0),
        sa.Column("protein_per_100g", sa.Float(), nullable=True, default=0),
        sa.Column("carbs_per_100g", sa.Float(), nullable=True, default=0),
        sa.Column("fat_per_100g", sa.Float(), nullable=True, default=0),
        sa.Column("fiber_per_100g", sa.Float(), nullable=True, default=0),
        sa.Column("sodium_per_100g_mg", sa.Float(), nullable=True, default=0),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_foods_id"), "foods", ["id"], unique=False)
    op.create_index(op.f("ix_foods_name"), "foods", ["name"], unique=False)

    op.create_table(
        "meals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("meal_type", sa.String(), nullable=True),
        sa.Column("source", sa.String(), nullable=False, default="text"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_meals_id"), "meals", ["id"], unique=False)

    op.create_table(
        "meal_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("meal_id", sa.Integer(), nullable=False),
        sa.Column("food_name", sa.String(), nullable=False),
        sa.Column("normalized_food_id", sa.Integer(), nullable=True),
        sa.Column("quantity", sa.Float(), nullable=False, default=1.0),
        sa.Column("unit", sa.String(), nullable=True),
        sa.Column("portion_size_category", sa.String(), nullable=True),
        sa.Column("preparation_method", sa.String(), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(["meal_id"], ["meals.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["normalized_food_id"], ["foods.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_meal_items_id"), "meal_items", ["id"], unique=False)

    op.create_table(
        "nutrient_aggregates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("meal_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("calories", sa.Float(), nullable=True, default=0),
        sa.Column("protein_g", sa.Float(), nullable=True, default=0),
        sa.Column("carbs_g", sa.Float(), nullable=True, default=0),
        sa.Column("fat_g", sa.Float(), nullable=True, default=0),
        sa.Column("fiber_g", sa.Float(), nullable=True, default=0),
        sa.Column("sodium_mg", sa.Float(), nullable=True, default=0),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["meal_id"], ["meals.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_nutrient_aggregates_id"), "nutrient_aggregates", ["id"], unique=False)

    op.create_table(
        "recommendations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("user_feedback", sa.String(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_recommendations_id"), "recommendations", ["id"], unique=False)


def downgrade() -> None:
    op.drop_table("recommendations")
    op.drop_table("nutrient_aggregates")
    op.drop_table("meal_items")
    op.drop_table("meals")
    op.drop_table("foods")
    op.drop_table("users")
