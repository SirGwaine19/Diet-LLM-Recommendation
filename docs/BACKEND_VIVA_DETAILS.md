# Backend Viva Notes (Detailed)

## Backend Overview (Opening Statement)

The backend is built with **FastAPI (Python)** and acts as the system's core logic layer.
It handles authentication, meal parsing orchestration, nutrition computation, recommendation generation, and persistent storage in PostgreSQL via SQLAlchemy.

It follows a layered design:

- **API layer**: route handlers in `app/api/v1`
- **Service layer**: business logic in `app/services`
- **Data layer**: SQLAlchemy models in `app/models`
- **Core infra**: config, DB session, auth utilities in `app/core`

## Backend Tech Stack (and Why)

- **FastAPI**: high productivity REST API framework with automatic validation and docs.
- **Uvicorn**: ASGI server runtime.
- **SQLAlchemy**: ORM mapping Python classes to relational tables.
- **Alembic**: versioned DB migrations.
- **PostgreSQL + psycopg2**: relational persistence.
- **Pydantic + pydantic-settings**: schema validation + env-based config.
- **python-jose**: JWT encode/decode.
- **passlib + bcrypt**: password hashing and verification.
- **OpenAI SDK**: LLM-powered meal parsing + recommendation generation.

## Application Bootstrapping and Routing

In `app/main.py`:

- FastAPI app is initialized with title/version metadata.
- CORS middleware is configured using `settings.CORS_ORIGINS`.
- All versioned routes are mounted under `/api/v1`.
- Two operational endpoints exist:
  - `/` for API info
  - `/health` for API + DB connectivity check (`SELECT 1`)

In `app/api/v1/__init__.py`:

- Public routes: `auth` (`/auth/register`, `/auth/login`)
- Protected routes (JWT-required): `users`, `meals`, `recommendations`

This gives a clean versioned API surface and consistent auth boundaries.

## Authentication and Security Flow (Important Viva Point)

### Registration/Login

In `app/api/v1/auth.py`:

- **Register**:
  - checks duplicate email
  - hashes password with bcrypt (`get_password_hash`)
  - stores user
  - returns JWT access token
- **Login**:
  - verifies user exists
  - verifies password hash (`verify_password`)
  - checks `is_active`
  - returns JWT token

### Token Mechanics

In `app/core/security.py`:

- `create_access_token()` creates JWT with:
  - `sub` = user id
  - `exp` = expiration based on `ACCESS_TOKEN_EXPIRE_MINUTES`
- `verify_token()` decodes JWT and returns subject or `None` on failure.

### Protected Access

In `app/core/dependencies.py`:

- `HTTPBearer` extracts token from header.
- Token is verified.
- User is fetched by ID from DB.
- Rejects invalid token / missing user / inactive user with 401 or 403.

This is a proper stateless JWT pattern for API-first systems.

## Meal Logging Pipeline (Core Innovation Flow)

When frontend calls `POST /api/v1/meals/log`, backend does:

1. Validate user/token.
2. In `meal_service.log_meal_from_text()`:
   - parse free-text meal with LLM (`parse_meal_text`)
   - infer `meal_type` if missing
   - create `Meal` row
   - create `MealItem` rows for each parsed item
3. For each item:
   - run DB food matching via `nutrition_service.match_food_item()`
4. Compute nutrition totals:
   - `calculate_meal_nutrients()` aggregates calories/protein/carbs/fat/fiber/sodium
5. Persist one `NutrientAggregate` row linked to meal.
6. Commit transaction and return structured `MealResponse`.

### Practical robustness in your implementation

- `meals.py` catches OpenAI-related failures.
- Maps quota/auth errors to informative 503 responses (not generic crashes).
- Returns clear diagnostic messages (e.g., missing API key, quota issues).

That's a strong real-world engineering detail to mention in viva.

## Nutrition Service Logic

In `app/services/nutrition_service.py`:

- Food search uses `ILIKE` fuzzy matching.
- Matching strategy is fallback-based:
  - full phrase
  - first token
  - singular/plural heuristics
- Nutrient scaling logic:
  - gram units => `quantity / 100`
  - serving-like units => quantity as serving multiplier
- If no matched food:
  - uses default per-serving fallback values to avoid zero outputs.

This design favors graceful behavior over hard failure.

## Recommendation Engine Flow

In `recommendation_service.py`:

1. Compute current day totals from `NutrientAggregate`.
2. Build 7-day history summary.
3. Construct profile-aware prompt including:
   - user demographics
   - goals
   - dietary preferences/allergies
   - today's macros + historical trend
4. Call LLM (`gpt-4o-mini`) to generate concise 4-5 line coaching summary.
5. Save recommendation in DB with metadata (date + stats).

In API:

- `GET /recommendations/daily`: fetch today's summary if exists.
- `POST /recommendations/generate`: generate on demand.
- `POST /recommendations/{id}/feedback`: store user feedback.

## Data Model (Conceptual ER Summary)

- **User**: account + profile + nutrition goals.
- **Meal**: one logged event; belongs to user.
- **MealItem**: parsed item rows under a meal.
- **Food**: nutrition reference data.
- **NutrientAggregate**: computed totals linked to meal + date.
- **Recommendation**: generated coaching text + metadata + optional feedback.

Important relation quality:

- cascades (`delete-orphan`) are used to maintain referential consistency.

## Config and Environment

From `app/core/config.py`:

Critical env values include:

- `DATABASE_URL`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `OPENAI_API_KEY`
- `CORS_ORIGINS`

This centralizes deploy-time configuration and avoids hardcoding secrets.

## Why This Backend Is Academically Strong

- Clear **separation of concerns** (API vs service vs data vs infra).
- Strong baseline **security** (hashed passwords + JWT + dependency-based auth).
- Real-world **AI integration** with operational error handling.
- Structured, normalized **relational persistence**.
- Extensible module boundaries for future features.

## Limitations You Can Honestly Mention

- Food matching is heuristic text matching, not semantic embedding-based matching.
- Fallback nutrient estimates can reduce precision when foods are unmatched.
- Recommendation quality depends on LLM response variability.
- No async task queue yet (LLM calls happen in request cycle).

Mentioning these shows maturity and critical evaluation.

## Future Backend Improvements (Good Viva Closing)

- Add embedding/vector similarity for better food normalization.
- Add confidence thresholds + human correction loop for parsed items.
- Introduce background jobs (Celery/RQ) for long-running AI tasks.
- Add rate limiting + audit logging for production hardening.
- Add automated tests around meal parsing/nutrient math edge cases.

## Likely Viva Questions (with short direct answers)

- **Why FastAPI instead of Django?**
  FastAPI gives lightweight, high-performance REST APIs with automatic schema validation and docs, ideal for service-based architecture.

- **How is authorization enforced globally?**
  Protected routers include `Depends(get_current_user)` so every request must pass JWT validation and active-user checks.

- **Where is business logic kept?**
  In service modules (`meal_service`, `nutrition_service`, `recommendation_service`), keeping route handlers thin.

- **How do you ensure DB consistency in meal logging?**
  Meal, items, and nutrient aggregate are created in one session/transaction flow, then committed together.

- **What happens if OpenAI fails?**
  Backend catches provider/quota/key errors and returns controlled HTTP errors with user-actionable messages.
