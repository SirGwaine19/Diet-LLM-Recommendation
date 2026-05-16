# Diet LLM Recommendation System - CS Student Explanation

## 1) What this project is

This project is a full-stack web application that helps users track meals and receive personalized diet guidance.

The key idea is simple:

- User writes a meal in plain language (example: "2 idlis with sambar and 1 cup tea")
- The backend uses an LLM to convert that text into structured food items
- Those items are matched with a food database to estimate nutrients
- The system stores meal history and generates a daily summary/recommendation

So academically, this is an applied AI + web systems project that combines:

- NLP-style extraction using an LLM
- API-driven backend design
- relational data modeling
- secure authentication
- modern frontend architecture

## 2) Problem it solves

Traditional calorie/macro apps force users to manually search and enter each food item. That is slow and error-prone.

This project reduces friction by allowing natural language input and still producing structured nutrition data.
It also adds personalized daily feedback instead of only raw numbers.

## 3) High-level architecture

The system has three main layers:

1. Client Layer (Frontend)

- React + TypeScript single-page app where users interact with the system.
- Includes pages for login/register, profile/goals, meal logging, dashboard, and history.
- Collects user input, sends API requests, and displays nutrient totals and recommendations.

1. API + Business Logic Layer (Backend)

- FastAPI REST backend that receives and validates requests from the frontend.
- Handles authentication/authorization (JWT), user profile operations, meal parsing workflow, and recommendation generation.
- Coordinates service modules so data flows cleanly from input to storage to response.

1. Data + External AI Layer

- PostgreSQL stores persistent, structured data: users, meals, meal items, nutrient aggregates, recommendations, and food reference data.
- OpenAI API is used for AI tasks: converting meal text into structured items and generating personalized daily recommendation text.
- This layer combines reliable relational storage with LLM-based intelligence.

## 4) End-to-end flow (what happens when user logs a meal)

1. User submits meal text in the frontend.
2. Frontend sends `POST /api/v1/meals/log` with JWT token.
3. Backend validates token and user identity.
4. `llm_service` calls OpenAI (`gpt-4o-mini`) to extract structured meal items.
5. `nutrition_service` matches each item with foods in database.
6. Nutrients are computed and aggregated.
7. Meal, meal items, and nutrient aggregate are stored in PostgreSQL.
8. Dashboard queries totals/history and shows progress.
9. User can generate a daily recommendation via recommendation endpoint.

This is a clean pipeline design: input -> parsing -> matching -> computation -> persistence -> feedback.

## 5) Core modules in this repository

- `backend/app/api/v1/`  
Route handlers for auth, users, meals, recommendations.
- `backend/app/services/`  
Business logic services:
  - `llm_service.py` (LLM parsing)
  - `meal_service.py` (orchestration)
  - `nutrition_service.py` (food matching + nutrient math)
  - `recommendation_service.py` (daily summary generation)
- `backend/app/models/`  
SQLAlchemy models for relational schema.
- `backend/alembic/`  
Versioned schema migrations.
- `frontend/src/pages/` and `frontend/src/components/`  
UI pages and reusable components.
- `frontend/src/services/`  
Axios service layer for API communication.

## 6) Technologies used and why each was used

### Backend and API

- Python
  - Chosen because it is strong for rapid backend development and AI integration.
- FastAPI
  - Used to build REST APIs with high developer productivity.
  - Built-in request validation and automatic Swagger docs (`/docs`) are useful for testing and demonstration.
- Uvicorn
  - ASGI server used to run FastAPI efficiently.
- Pydantic + pydantic-settings
  - Used for strict request/response schema validation and environment-based configuration.

### Database and persistence

- PostgreSQL
  - Chosen for reliable relational storage, transactions, and strong SQL support.
  - Good fit for structured entities: users, meals, meal_items, nutrient_aggregates, recommendations.
- SQLAlchemy
  - ORM used to map Python classes to database tables.
  - Keeps data access clean and maintainable.
- Alembic
  - Used for versioned database migrations.
  - Important in team/academic environments to keep schema evolution reproducible.
- `psycopg2-binary`
  - PostgreSQL driver for Python.

### Authentication and security

- JWT (`python-jose`)
  - Stateless authentication for protected API routes.
  - Frontend stores token and sends it as `Authorization: Bearer`.
- `passlib` + `bcrypt`
  - Password hashing (never storing plain text passwords).
  - Basic but essential security practice.

### AI integration

- OpenAI Python SDK (`openai`)
  - Used to call LLM models for:
    - natural language meal parsing
    - daily summary/recommendation generation
  - This is the intelligence layer of the project.

### Frontend

- React 18
  - Component-based UI framework for building SPA screens and reusable UI blocks.
- TypeScript
  - Adds static types to reduce runtime bugs and improve maintainability.
- Vite
  - Fast development server and build tool.
  - Improves local iteration speed.
- React Router
  - Client-side routing for pages (`/dashboard`, `/profile`, `/log-meal`, etc.).
- Axios
  - HTTP client used for API calls and interceptors (auto-attach JWT, handle 401 globally).
- TanStack React Query
  - Server-state caching and synchronization (queries/mutations, invalidation after updates).
- Zustand
  - Lightweight global state for auth token management.
- React Hook Form
  - Efficient form state handling and validation for login/register/profile/meal forms.
- date-fns
  - Date calculations and formatting (daily/weekly dashboard views).

### DevOps and local development

- Docker Compose
  - Runs PostgreSQL quickly in local development with consistent setup.
- `.env` + `python-dotenv`
  - Secure and environment-specific configuration management.
- Git/GitHub
  - Version control and collaboration.

## 7) Data model (conceptual)

Main entities and relationships:

- User
  - Owns many meals
  - Owns many recommendations
- Meal
  - Belongs to one user
  - Has many meal items
  - Has one nutrient aggregate
- MealItem
  - Stores each parsed food line item
  - Optionally linked to normalized food reference
- Food
  - Reference nutrition dataset (per 100g values)
- NutrientAggregate
  - Stores computed totals (calories/macros/etc.) per meal/day context
- Recommendation
  - Stores generated daily advice + optional user feedback

## 8) Why this architecture is good for a major project

- Clear separation of concerns (UI, API, data, AI service layers)
- Real-world security baseline (JWT + hashed passwords)
- Reproducible database lifecycle (Alembic migrations)
- Modular service layer for future upgrades (image logging, RAG, multilingual support)
- Easy to demo and evaluate (Swagger docs + dashboard + history + recommendation loop)

## 9) Current limitations and future scope

Current limitations:

- Nutrition matching is lookup-based and may be approximate.
- LLM output quality depends on prompt/model behavior.
- No advanced personalization model beyond rule/context prompting.

Future improvements:

- Image-based meal logging (vision model integration)
- Better food matching with embeddings/vector search
- Habit and trend analytics over longer windows
- Role-based admin analytics and moderation tools
- Multilingual meal input and localized recommendations

## 10) One-line academic takeaway

This project demonstrates how to engineer a practical AI-powered health application by integrating LLM inference with a robust full-stack web architecture, secure API design, and relational data persistence.