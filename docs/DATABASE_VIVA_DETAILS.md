# Database Viva Notes (Detailed)

## Database Overview (Opening Statement)

The project uses a **PostgreSQL relational database** with **SQLAlchemy ORM** and **Alembic migrations**.
The database is designed to store:

- user account and profile data,
- raw meal logs and parsed meal items,
- computed nutrition aggregates,
- generated recommendation history,
- reference food nutrition data.

In simple terms, the database supports the complete pipeline:
**user profile -> meal logging -> nutrient computation -> recommendation generation**.

## Database Technology Choices (Why)

- **PostgreSQL**
  - Reliable relational DB with strong ACID guarantees.
  - Good fit for structured entities and foreign-key constraints.
- **SQLAlchemy**
  - Maps Python classes to tables and relationships cleanly.
  - Keeps data access maintainable and expressive.
- **Alembic**
  - Provides version-controlled schema evolution.
  - Enables reproducible DB changes across environments.

## Core Tables in This Project

### 1) `users`

Stores account and health-profile information.

Important columns:

- identity: `id`, `email` (unique), `hashed_password`, `full_name`
- profile: `age`, `sex`, `height_cm`, `weight_kg`, `target_weight_kg`, `activity_level`
- preferences: `dietary_preferences`, `allergies`, `cultural_preferences` (JSON)
- goals: `daily_calorie_target`, `protein_target_g`, `carb_target_g`, `fat_target_g`
- account status/meta: `is_active`, `created_at`, `updated_at`

### 2) `foods`

Reference nutrition catalog used for matching meal items.

Important columns:

- `id`, `name`, `description`
- per-100g nutrients:
  - `calories_per_100g`
  - `protein_per_100g`
  - `carbs_per_100g`
  - `fat_per_100g`
  - `fiber_per_100g`
  - `sodium_per_100g_mg`

### 3) `meals`

Represents one meal event logged by a user.

Important columns:

- `id`
- `user_id` (FK to `users`)
- `timestamp`
- `meal_type` (breakfast/lunch/dinner/snack)
- `source` (e.g., text-based logging)

### 4) `meal_items`

Represents itemized foods inside one meal.

Important columns:

- `id`
- `meal_id` (FK to `meals`)
- `food_name` (raw/parsed name)
- `normalized_food_id` (optional FK to `foods`)
- `quantity`, `unit`
- metadata from parser:
  - `portion_size_category`
  - `preparation_method`
  - `confidence_score`

### 5) `nutrient_aggregates`

Stores computed nutrition totals.

Important columns:

- `id`
- `meal_id` (FK to `meals`, nullable)
- `user_id` (FK to `users`)
- `date`
- nutrient totals:
  - `calories`, `protein_g`, `carbs_g`, `fat_g`, `fiber_g`, `sodium_mg`
- `created_at`

### 6) `recommendations`

Stores AI-generated daily coaching/summary text.

Important columns:

- `id`
- `user_id` (FK to `users`)
- `type` (e.g., daily)
- `content`
- `generated_at`
- `user_feedback`
- `metadata` (stored via ORM field `extra_metadata`)

## Entity Relationships (ER Perspective)

Main cardinalities:

- **User -> Meals**: one-to-many
- **Meal -> MealItems**: one-to-many
- **Meal -> NutrientAggregate**: one-to-one in current ORM design (`uselist=False`)
- **User -> Recommendations**: one-to-many
- **MealItem -> Food**: many-to-one (optional normalized match)
- **User -> NutrientAggregates**: one-to-many

Relationship behavior:

- Project uses cascade patterns (`delete-orphan`) in ORM to keep child data consistent.
- In initial migration, many foreign keys use DB-level `ON DELETE CASCADE`, so deleting a parent user/meal removes dependent rows.
- `meal_items.normalized_food_id` uses `ON DELETE SET NULL` to preserve logged meal item even if reference food changes.

## Normalization Strategy

The schema is mostly normalized and practical:

- Reusable master data (`foods`) is separated from transactional logs (`meal_items`).
- Meal-level event (`meals`) and item-level detail (`meal_items`) are separated.
- Computed totals are materialized in `nutrient_aggregates` to speed reads.
- Recommendation text/history is isolated from raw meal/nutrient data.

This gives a balanced design: normalized enough for integrity, with precomputed aggregates for performance.

## Indexes and Constraints

From migration:

- Primary key index on all `id` columns.
- explicit useful index: `users.email` unique index.
- index on `foods.name` for lookup speed.

Key constraints:

- `users.email` unique.
- foreign key constraints across meals/items/aggregates/recommendations.
- non-null constraints on essential identity and linkage fields.

## Data Lifecycle (End-to-End)

When a user logs meal text:

1. A row is inserted into `meals`.
2. Parsed entries are inserted into `meal_items`.
3. Matching tries to link each item to `foods` via `normalized_food_id`.
4. Total nutrients are computed and stored in `nutrient_aggregates`.
5. Later, recommendation generation reads aggregates + profile and inserts into `recommendations`.

This means the DB preserves:

- **raw trace** (what user logged),
- **structured trace** (parsed items),
- **computed trace** (nutrition totals),
- **advice trace** (recommendation + feedback).

## Migrations and Schema Evolution

Alembic setup:

- environment configured in `alembic/env.py`
- metadata loaded from SQLAlchemy models (`Base.metadata`)
- migration versions in `alembic/versions`

Current visible migration pattern:

- `001_initial_schema.py`: creates core tables and indexes.
- `002_add_sequence_defaults.py`: additional schema update step.

Why this matters in viva:

- Schema changes are reproducible, auditable, and team-safe.
- Avoids manual SQL drift between developer environments.

## Strengths of This Database Design

- Clear relational structure for core entities.
- Good referential integrity via foreign keys.
- Separation between reference data and user event data.
- Supports analytics/history through persisted aggregates.
- Stores recommendation history with feedback for future learning loops.

## Limitations to Mention Honestly

- Food matching depends on text heuristics; normalization may be imperfect.
- Nutrient aggregates are currently basic (no advanced constraint/quality flags).
- Reporting queries may need more composite indexes at scale.
- Recommendation metadata currently flexible JSON; stricter schema may help long-term analytics.

## Future Database Improvements

- Add composite indexes for frequent filters:
  - (`user_id`, `date`) on `nutrient_aggregates`
  - (`user_id`, `timestamp`) on `meals`
  - (`user_id`, `generated_at`) on `recommendations`
- Add check constraints (e.g., non-negative quantities/macros).
- Add soft-delete/audit tables for compliance.
- Partition large time-series tables if usage grows.
- Add data quality flags and confidence thresholds for parsed items.

## Viva Questions and Short Answers

- **Why PostgreSQL for this project?**
  It provides strong consistency and relational integrity, which are essential for linked health/nutrition entities.

- **Why keep both `meal_items` and `nutrient_aggregates`?**
  `meal_items` preserves detailed item-level traceability, while `nutrient_aggregates` enables fast dashboard and recommendation reads.

- **How do you maintain referential integrity?**
  Through foreign keys, ORM relationships, and cascade behavior at ORM and migration levels.

- **Why use JSON columns in `users` and `recommendations`?**
  JSON allows flexible storage for variable preferences/metadata without frequent schema changes.

- **How are schema changes managed safely?**
  Using Alembic migration scripts with revision history, so updates are reproducible across environments.
