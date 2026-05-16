"""Add sequence defaults for primary key columns (fix 500 on register)

Revision ID: 002
Revises: 001
Create Date: 2025-02-25

PostgreSQL requires a DEFAULT or explicit value for id columns.
The initial migration created tables without SERIAL/sequences, so INSERT fails.
This adds sequences and sets id defaults so the ORM can insert without specifying id.
"""
from alembic import op

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def _set_sequence(table: str, column: str = "id") -> None:
    seq = f"{table}_{column}_seq"
    op.execute(f"CREATE SEQUENCE IF NOT EXISTS {seq}")
    op.execute(f"ALTER TABLE {table} ALTER COLUMN {column} SET DEFAULT nextval('{seq}')")
    op.execute(
        f"SELECT setval('{seq}', COALESCE((SELECT MAX({column}) FROM {table}), 1))"
    )


def upgrade() -> None:
    for table in ("users", "foods", "meals", "meal_items", "nutrient_aggregates", "recommendations"):
        _set_sequence(table)


def downgrade() -> None:
    for table in ("users", "foods", "meals", "meal_items", "nutrient_aggregates", "recommendations"):
        op.execute(f"ALTER TABLE {table} ALTER COLUMN id DROP DEFAULT")
        op.execute(f"DROP SEQUENCE IF EXISTS {table}_id_seq")
