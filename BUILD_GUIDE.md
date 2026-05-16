# Step-by-Step Build Guide: Diet LLM Recommendation System

This guide provides detailed steps to build the project following the design document. Follow these steps sequentially.

**Staying aligned with this repository:** File-by-file roles and a short “how it was built” narrative are in **[PROJECT_STRUCTURE.txt](PROJECT_STRUCTURE.txt)**. Database options (Docker vs local PostgreSQL) are detailed in **[database/SETUP.md](database/SETUP.md)**. The guide below is the master checklist; where the repo already differs (e.g. Vite-only frontend, `GET /meals` date filters), the notes in those sections apply.

---

## Prerequisites Setup

### Step 1: Install Required Software
1. **Python 3.9+**: Download and install from python.org
2. **Node.js 18+**: Download and install from nodejs.org (for frontend)
3. **PostgreSQL 14+**: Install PostgreSQL database
4. **Git**: For version control
5. **Code Editor**: VS Code or your preferred IDE

### Step 2: Set Up Development Environment
1. Create project directory structure (this repo also includes `docker-compose.yml` at the root for PostgreSQL, plus `PROJECT_STRUCTURE.txt`, `README.md`, etc.):
   ```
   diet-recommendation-system/
   ├── backend/
   ├── frontend/
   ├── database/
   ├── docs/
   └── docker-compose.yml   # optional: local Postgres via Docker
   ```

2. Initialize Git repository:
   ```bash
   git init
   git add .gitignore
   ```

3. Create `.gitignore` files for both backend and frontend

---

## Phase 1: Text-Only MVP

### Part A: Backend Foundation

#### Step 3: Set Up Backend Project Structure
1. Navigate to `backend/` directory
2. Create Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Create `requirements.txt` with dependencies:
   - FastAPI, Uvicorn (web framework)
   - SQLAlchemy, Alembic (database ORM and migrations)
   - psycopg2-binary (PostgreSQL adapter)
   - python-dotenv (environment variables)
   - pydantic, pydantic-settings (data validation)
   - python-jose, passlib (authentication)
   - openai (LLM integration)
   - httpx (HTTP client)

4. Install dependencies: `pip install -r requirements.txt`

#### Step 4: Configure Environment Variables
1. Create `.env` file in `backend/` directory
2. Add the following variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `SECRET_KEY`: Random secret for JWT tokens
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `ALGORITHM`: JWT algorithm (HS256)
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
   - `DEBUG`: Development mode flag

#### Step 5: Set Up Database Connection
1. Create `app/core/database.py`:
   - Import SQLAlchemy
   - Create engine with connection pooling
   - Create SessionLocal for database sessions
   - Create Base class for models
   - Create `get_db()` dependency function

2. Create `app/core/config.py`:
   - Use pydantic-settings to load environment variables
   - Define Settings class with all config variables
   - Load from `.env` file

#### Step 6: Create Database Models
1. Create `app/models/` directory structure

2. **User Model** (`app/models/user.py`):
   - Fields: id, email, hashed_password, full_name
   - Profile: age, sex, height_cm, weight_kg, target_weight_kg, activity_level
   - Preferences: dietary_preferences (JSON), allergies (JSON), cultural_preferences (JSON)
   - Goals: daily_calorie_target, protein_target_g, carb_target_g, fat_target_g
   - Metadata: is_active, created_at, updated_at
   - Relationships: meals, recommendations

3. **Meal Model** (`app/models/meal.py`):
   - Fields: id, user_id (FK), timestamp, meal_type, source (text/image)
   - Relationship: user, meal_items

4. **MealItem Model** (`app/models/meal_item.py`):
   - Fields: id, meal_id (FK), food_name, normalized_food_id, quantity, unit
   - Fields: portion_size_category, preparation_method, confidence_score
   - Relationship: meal, nutrition_data

5. **NutrientAggregate Model** (`app/models/nutrient.py`):
   - Fields: id, meal_id (FK), user_id (FK), date
   - Nutrients: calories, protein_g, carbs_g, fat_g, fiber_g, sodium_mg, etc.
   - Relationship: meal, user

6. **Recommendation Model** (`app/models/recommendation.py`):
   - Fields: id, user_id (FK), type (daily/weekly/meal), content, generated_at
   - Fields: user_feedback (liked/ignored/followed), metadata (JSON)
   - Relationship: user

7. Create `app/models/__init__.py` to export all models

#### Step 7: Set Up Database Migrations
1. Initialize Alembic:
   ```bash
   alembic init alembic
   ```

2. Configure `alembic.ini`:
   - Update `sqlalchemy.url` to use environment variable

3. Configure `alembic/env.py`:
   - Import Base from your models
   - Set `target_metadata = Base.metadata`

4. Create initial migration:
   ```bash
   alembic revision --autogenerate -m "Initial schema"
   ```

5. Review and edit migration file if needed

6. Apply migration:
   ```bash
   alembic upgrade head
   ```

#### Step 8: Create Authentication System
1. Create `app/core/security.py`:
   - `verify_password()`: Verify password against hash
   - `get_password_hash()`: Hash passwords using bcrypt
   - `create_access_token()`: Generate JWT tokens
   - `verify_token()`: Verify and decode JWT tokens

2. Create `app/schemas/auth.py`:
   - `Token`: Response schema with access_token and token_type
   - `TokenData`: Token payload schema
   - `UserLogin`: Login request schema
   - `UserRegister`: Registration request schema

3. Create `app/api/v1/auth.py`:
   - POST `/register`: User registration endpoint
   - POST `/login`: User login endpoint (returns JWT token)
   - GET `/me`: Get current user info (protected)

4. Create authentication dependency:
   - `app/core/dependencies.py`:
   - `get_current_user()`: Extract user from JWT token

#### Step 9: Create User Management API
1. Create `app/schemas/user.py`:
   - `UserBase`, `UserCreate`, `UserUpdate`, `UserResponse` schemas

2. Create `app/api/v1/users.py`:
   - GET `/users/me`: Get current user profile
   - PUT `/users/me`: Update user profile
   - GET `/users/me/goals`: Get user goals
   - PUT `/users/me/goals`: Update user goals

3. Create `app/services/user_service.py`:
   - Business logic for user operations
   - Profile validation
   - Goal calculation helpers

#### Step 10: Build Food Logging Service (Text Parsing)
1. Create `app/services/llm_service.py`:
   - Initialize OpenAI client
   - `parse_meal_text()`: Function to send text to LLM for parsing
   - Design prompt that:
     - Asks LLM to extract structured meal data
     - Returns JSON with meal items, quantities, units
     - Handles ambiguities with confidence scores
     - Never fabricates nutrients

2. Create `app/schemas/meal.py`:
   - `MealItemCreate`: Schema for parsed meal items
   - `MealCreate`: Schema for meal creation
   - `MealResponse`: Schema for meal responses

3. Create `app/services/nutrition_service.py`:
   - `search_food()`: Search nutrition database for food items
   - `calculate_nutrients()`: Calculate nutrients for meal items
   - `match_food_item()`: Fuzzy/semantic matching of food names
   - For MVP: Use a simple food database (CSV/JSON) or API like USDA FoodData Central

4. Create `app/api/v1/meals.py`:
   - POST `/meals/log`: Accept text input, parse with LLM, match to nutrition DB, save
   - GET `/meals`: Get user's meal history (optional query params `start_date` and `end_date` to filter by calendar day—used by the dashboard weekly chart)
   - GET `/meals/{meal_id}`: Get specific meal details
   - DELETE `/meals/{meal_id}`: Delete a meal

5. Create `app/services/meal_service.py`:
   - Orchestrate: LLM parsing → Nutrition matching → Database storage
   - Handle errors and edge cases

#### Step 11: Build Recommendation Service
1. Create `app/services/recommendation_service.py`:
   - `get_user_history_summary()`: Aggregate last N days of meals
   - `calculate_daily_stats()`: Compute daily nutrition totals
   - `generate_daily_summary()`: Use LLM to create daily summary
   - Design prompt that:
     - Includes user profile and goals
     - Includes recent meal history
     - Generates positive, non-judgmental feedback
     - Provides actionable suggestions

2. Create `app/schemas/recommendation.py`:
   - `RecommendationCreate`, `RecommendationResponse` schemas

3. Create `app/api/v1/recommendations.py`:
   - GET `/recommendations/daily`: Get today's summary
   - POST `/recommendations/generate`: Manually trigger summary generation
   - POST `/recommendations/{id}/feedback`: Record user feedback

#### Step 12: Set Up API Router
1. Create `app/api/v1/__init__.py`:
   - Import all route modules (auth, users, meals, recommendations)
   - Create main `api_router` and include all sub-routers with prefixes
   - Add `dependencies=[Depends(get_current_user)]` to users, meals, recommendations (all protected)
   - Auth router stays without router-level deps (register/login are public; /me has per-route auth)

2. Update `app/main.py`:
   - Create FastAPI app instance with title, description, version
   - Add CORS middleware with `allow_origins`, `allow_credentials`, `allow_methods`, `allow_headers`
   - Include API router at prefix `/api/v1`
   - Add `GET /` root endpoint (API info, links to docs/health)
   - Add `GET /health` endpoint (returns status + database connectivity check)

#### Step 13: Test Backend API
1. **Start PostgreSQL database**
   - **Option A (Docker):** From the repository root, run `docker compose up -d` and use the credentials in `database/SETUP.md` / your `backend/.env` `DATABASE_URL`.
   - **Option B:** Install PostgreSQL locally and ensure it is listening on the host/port in `DATABASE_URL` (often `localhost:5432`).

2. **Configure environment** – copy `backend/.env.example` to `backend/.env` and set:
   - `DATABASE_URL=postgresql://user:password@localhost:5432/diet_recommendation_db`
   - `SECRET_KEY`, `OPENAI_API_KEY`

3. **Run migrations**:
   ```bash
   cd backend
   alembic upgrade head
   ```

4. **Start server**:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Test endpoints**:
   - Open **FastAPI docs**: http://localhost:8000/docs
   - **Health check**: `curl http://localhost:8000/health`
   - **Register**:
     ```bash
     curl -X POST http://localhost:8000/api/v1/auth/register \
       -H "Content-Type: application/json" \
       -d '{"email":"test@example.com","password":"testpass123","full_name":"Test User"}'
     ```
   - **Login** (save the `access_token` from response):
     ```bash
     curl -X POST http://localhost:8000/api/v1/auth/login \
       -H "Content-Type: application/json" \
       -d '{"email":"test@example.com","password":"testpass123"}'
     ```
   - **Log meal** (replace `YOUR_TOKEN`):
     ```bash
     curl -X POST http://localhost:8000/api/v1/meals/log \
       -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" \
       -d '{"text":"2 eggs and toast with butter","meal_type":"breakfast"}'
     ```
   - **Get recommendations**:
     ```bash
     curl -X GET http://localhost:8000/api/v1/recommendations/daily \
       -H "Authorization: Bearer YOUR_TOKEN"
     ```

---

### Part B: Frontend Foundation

#### Step 14: Set Up Frontend Project
1. Navigate to `frontend/` directory
2. **This repository uses Vite** (not Create React App). Initialize or verify:
   ```bash
   npm create vite@latest . -- --template react-ts
   ```
   Configure `vite.config.ts` with dev server port **3000** and a **proxy** for `/api` → `http://localhost:8000` so the SPA can call `/api/v1/...` without CORS issues during development.

3. Install additional dependencies:
   - `axios`: HTTP client
   - `react-router-dom`: Routing
   - `@tanstack/react-query`: Data fetching
   - `zustand` or `redux`: State management
   - `react-hook-form`: Form handling
   - `date-fns`: Date formatting

#### Step 15: Set Up Frontend Structure
1. Create directory structure:
   ```
   frontend/src/
   ├── components/
   │   ├── common/
   │   ├── auth/
   │   ├── dashboard/      # e.g. NutritionProgress, WeeklyProgressGraph
   │   ├── meals/
   │   └── recommendations/
   ├── pages/
   ├── services/
   ├── hooks/
   ├── store/
   └── utils/
   ```

2. Create API service layer:
   - `src/services/api.ts`: Axios instance with base URL and interceptors
   - `src/services/authService.ts`: Authentication API calls
   - `src/services/mealService.ts`: Meal logging API calls (`list` supports optional `startDate` / `endDate` for ranged history)
   - `src/services/userService.ts`: Profile and goals
   - `src/services/recommendationService.ts`: Recommendation API calls

#### Step 16: Implement Authentication UI
1. Create `src/pages/Login.tsx`:
   - Login form with email and password
   - Handle form submission
   - Store JWT token in localStorage
   - Redirect to dashboard on success

2. Create `src/pages/Register.tsx`:
   - Registration form
   - Basic validation
   - Redirect to login on success

3. Create `src/components/auth/ProtectedRoute.tsx`:
   - Check for authentication token
   - Redirect to login if not authenticated

4. Set up routing in `App.tsx`:
   - `/login`, `/register`, `/dashboard` routes
   - Protect dashboard route

#### Step 17: Implement User Profile UI
1. Create `src/pages/Profile.tsx`:
   - Display user profile information
   - Form to edit profile (age, height, weight, etc.)
   - Form to set dietary preferences and allergies
   - Form to set goals (calorie target, macros)

2. Optional: extract `ProfileForm` / `GoalsForm` into `src/components/` submodules; this repo keeps the main forms inline in `Profile.tsx` for simplicity.

#### Step 18: Implement Meal Logging UI
1. Create `src/pages/LogMeal.tsx`:
   - Text input area for free-form meal description
   - Submit button
   - Loading state while parsing
   - Display parsed meal items for confirmation
   - Show nutrition breakdown after confirmation

2. Create `src/components/meals/MealInput.tsx`:
   - Textarea for meal description
   - Submit handler

3. *(Optional / future)* `MealPreview.tsx` for edit-before-save—current MVP shows results immediately after log.

4. Create `src/components/meals/NutritionBreakdown.tsx`:
   - Display calories, macros, key nutrients
   - Visual indicators (progress bars, etc.)

#### Step 19: Implement Meal History UI
1. Create `src/pages/MealHistory.tsx`:
   - List of logged meals (chronological)
   - Filter by date range
   - Display meal items and nutrition for each meal
   - Delete meal functionality

2. Create `src/components/meals/MealCard.tsx`:
   - Card component to display individual meal
   - Show timestamp, items, nutrition summary

#### Step 20: Implement Recommendations/Dashboard UI
1. Create `src/pages/Dashboard.tsx`:
   - Display daily summary (recommendation)
   - Show today's nutrition progress vs goals
   - Weekly calorie trend (e.g. SVG chart) with previous/next week navigation—this repo uses `WeeklyProgressGraph.tsx` fed by `mealService.list` with a week date range
   - Quick links to meal logging and recent meals for today

2. Create `src/components/recommendations/DailySummary.tsx`:
   - Display LLM-generated daily summary
   - Format nicely with markdown or rich text
   - Show feedback buttons (like/ignore)

3. Create `src/components/dashboard/NutritionProgress.tsx`:
   - Progress bars for calories, macros
   - Visual indicators vs. targets

4. Create `src/components/dashboard/WeeklyProgressGraph.tsx` (or equivalent):
   - Plot daily calories for the selected week; optional comparison to calorie goal

#### Step 21: Add State Management
1. Set up authentication state:
   - Store current user
   - Store auth token
   - Login/logout actions

2. Set up meal state (optional, can use React Query):
   - Cache meal history
   - Optimistic updates

#### Step 22: Style the Application
1. Choose CSS framework (Tailwind CSS, Material-UI, or custom CSS)
2. Create consistent design system
3. Make it responsive for mobile
4. Add loading states and error handling
5. Improve UX with animations and transitions

#### Step 23: Test Frontend
1. Test all user flows:
   - Registration → Login → Profile setup → Meal logging → View recommendations
2. Test error handling
3. Test responsive design
4. Test with real backend API

---

## Phase 2: Improved Recommendations (RAG)

### Step 24: Set Up Vector Database
1. Choose vector DB (Pinecone, Weaviate, or pgvector with PostgreSQL)
2. Install and configure vector database
3. Set up embedding model (OpenAI embeddings or sentence-transformers)

### Step 25: Build Knowledge Base
1. Create nutrition knowledge documents:
   - Macronutrients guide
   - Micronutrients guide
   - Portion control tips
   - Healthy swaps
   - Cultural food information
2. Chunk documents into small passages
3. Generate embeddings for each chunk
4. Store in vector database

### Step 26: Implement RAG Pipeline
1. Create `app/services/rag_service.py`:
   - `retrieve_relevant_knowledge()`: Search vector DB for relevant chunks
   - `retrieve_user_context()`: Get relevant user history
   - `generate_rag_prompt()`: Combine context and knowledge

2. Update recommendation service:
   - Use RAG to retrieve context before LLM generation
   - Include retrieved knowledge in prompts

### Step 27: Add Recipe Knowledge Base
1. Create recipe database (JSON or separate table)
2. Tag recipes with: cuisine, dietary preference, complexity, prep time
3. Generate embeddings for recipes
4. Implement recipe recommendation endpoint

---

## Phase 3: Image-Based Logging

### Step 28: Set Up Image Storage
1. Choose object storage (AWS S3, Azure Blob, or local storage for dev)
2. Configure storage service
3. Create `app/services/storage_service.py`:
   - Upload image function
   - Generate signed URLs for access

### Step 29: Integrate Vision Model
1. Choose vision model:
   - OpenAI Vision API (GPT-4 Vision)
   - Specialized food recognition model (Food-101, etc.)
   - Custom fine-tuned model
2. Create `app/services/vision_service.py`:
   - `detect_food_items()`: Detect and label foods in image
   - `estimate_portions()`: Estimate portion sizes (basic heuristics)

### Step 30: Build Image Logging Pipeline
1. Update `app/api/v1/meals.py`:
   - Add POST `/meals/log-image` endpoint
   - Accept image upload
   - Process through vision service
   - Convert to structured meal (reuse text pipeline)

2. Create `app/models/image.py`:
   - Store image metadata and storage path

3. Update frontend:
   - Add image upload component
   - Display detected foods for confirmation
   - Allow user to correct detections

---

## Phase 4: Optimization and Scaling

### Step 31: Implement Caching
1. Add Redis for caching:
   - Cache embeddings
   - Cache LLM responses for deterministic queries
   - Cache user summaries

2. Update services to use cache

### Step 32: Optimize LLM Usage
1. Implement model selection:
   - Use smaller models for parsing
   - Use larger models for complex reasoning
2. Implement prompt optimization
3. Add context summarization for long histories

### Step 33: Add Background Jobs
1. Set up task queue (Celery with Redis):
   - Weekly report generation
   - Batch processing of recommendations
   - Image processing

2. Create background job handlers

### Step 34: Add Monitoring and Logging
1. Set up logging (Python logging, structured logs)
2. Add application monitoring (Sentry, etc.)
3. Add performance metrics
4. Set up error tracking

### Step 35: Write Tests
1. Backend unit tests (pytest):
   - Test services
   - Test API endpoints
   - Test database models

2. Backend integration tests:
   - Test full workflows
   - Test LLM integration (mocked)

3. Frontend tests (Jest, React Testing Library):
   - Component tests
   - Integration tests

### Step 36: Documentation
1. API documentation (FastAPI auto-generates, but enhance it)
2. User documentation
3. Developer setup guide
4. Deployment guide

### Step 37: Deployment Preparation
1. Set up production environment variables
2. Configure production database
3. Set up CI/CD pipeline
4. Configure production server (Docker, etc.)
5. Set up SSL certificates
6. Configure domain and DNS

---

## Testing Checklist

After each phase, test:
- [ ] User registration and authentication
- [ ] Profile creation and updates
- [ ] Text-based meal logging
- [ ] Nutrition calculation accuracy
- [ ] Daily summary generation
- [ ] Meal history retrieval
- [ ] Error handling
- [ ] Security (authentication, authorization)
- [ ] Performance (response times)
- [ ] Mobile responsiveness (frontend)

---

## Key Considerations Throughout

1. **Security**: Always hash passwords, use HTTPS, validate inputs, sanitize outputs
2. **Error Handling**: Graceful error messages, logging, user-friendly feedback
3. **Performance**: Database indexing, query optimization, caching
4. **User Experience**: Loading states, clear feedback, intuitive UI
5. **Safety**: Medical disclaimers, non-judgmental language, eating disorder sensitivity
6. **Privacy**: Data encryption, access controls, GDPR compliance if needed

---

## Next Steps After MVP

- Add weekly review functionality
- Implement meal planning features
- Add social features (optional)
- Integrate wearable devices
- Add localization for different regions
- Create professional dashboard for dietitians

---

Good luck building your diet recommendation system! Follow these steps methodically, test as you go, and iterate based on feedback.
