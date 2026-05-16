# Methodology

This section describes the methodology for designing, implementing, and evaluating the proposed LLM-based diet recommendation system.

---

## 3.1 System Architecture

The proposed system follows a modular, multi-tier architecture comprising four primary layers:

1. **Client Layer**: A web-based interface enabling users to log meals via natural language text or images, view nutritional summaries, and receive personalized recommendations.

2. **API Layer**: A RESTful backend built on FastAPI, exposing endpoints for authentication, user management, meal logging, and recommendation retrieval.

3. **AI/ML Layer**: Integrates large language models (LLMs) for natural language understanding, structured extraction, and recommendation generation; computer vision models for image-based food recognition; and embedding models for semantic retrieval.

4. **Data Layer**: Comprises a relational database (PostgreSQL) for structured storage of users, meals, nutrients, and recommendations; a vector store for semantic search over nutrition knowledge bases; and object storage for meal images.

**Figure 1** (not shown) illustrates the data flow: user input → preprocessing → LLM/vision parsing → nutrition matching → storage → recommendation engine → response.

---

## 3.2 Data Collection and Preprocessing

### 3.2.1 Nutrition Database

A curated nutrition database is constructed by aggregating data from:

- **USDA FoodData Central**: Providing per-100g nutrient profiles for common foods.
- **Regional food databases**: Including culturally relevant items (e.g., Indian, Mediterranean cuisines).
- **Branded food APIs**: For commercial products with standardized nutrition labels.

Each food entry contains: `name`, `calories_per_100g`, `protein_per_100g`, `carbs_per_100g`, `fat_per_100g`, `fiber_per_100g`, and `sodium_per_100g_mg`.

### 3.2.2 User Data

User profiles capture:

- **Demographic attributes**: Age, sex, height, weight, activity level.
- **Dietary constraints**: Preferences (vegetarian, vegan, low-carb), allergies (nuts, gluten, lactose), and cultural preferences.
- **Goals**: Daily calorie target, macronutrient splits (protein, carbs, fat).

All data is collected with informed consent and stored securely with encryption at rest.

### 3.2.3 Meal Logs

Users submit meal descriptions in natural language (e.g., "I had two slices of pepperoni pizza and a Coke for lunch"). The system preprocesses input by:

1. Normalizing whitespace and correcting minor typos (handled implicitly by the LLM).
2. Detecting language to ensure compatibility.
3. Passing the raw text to the LLM-based parser.

---

## 3.3 Proposed Algorithms

### 3.3.1 LLM-Based Structured Extraction

**Objective**: Convert unstructured natural language meal descriptions into structured records.

**Method**:

1. A carefully designed prompt instructs the LLM to extract:
   - Food item names
   - Quantities and units (e.g., 2 slices, 1 cup)
   - Portion size category (small/medium/large) when units are ambiguous
   - Preparation method (fried, baked, grilled)
   - Confidence score (0–1) per item

2. The LLM returns a JSON object adhering to a predefined schema.

3. Low-confidence items are flagged for user confirmation.

**Prompt Design**:

```
You are a meal logging assistant. Extract structured data from the user's message.
Rules:
- Extract each food item with: food_name, quantity, unit, portion_size_category, preparation_method, confidence_score
- Never fabricate nutrient values
- Return valid JSON only
```

### 3.3.2 Fuzzy and Semantic Food Matching

**Objective**: Map parsed food names to entries in the nutrition database.

**Method**:

1. **Fuzzy Search**: Perform case-insensitive substring matching (SQL `ILIKE`) to retrieve candidate foods.

2. **Semantic Retrieval** (for RAG-enhanced systems):
   - Generate embeddings for the parsed food name using an embedding model (e.g., OpenAI `text-embedding-3-small`).
   - Query the vector store for the k-nearest neighbors.
   - Re-rank candidates using cosine similarity.

3. **LLM Re-Ranking** (optional): When multiple candidates have similar scores, use the LLM to select the most contextually appropriate match.

4. Return the best match or prompt the user if confidence is below a threshold.

### 3.3.3 Nutrient Calculation

**Objective**: Compute total nutrients for a meal.

**Method**:

For each meal item with matched food entry:

```
factor = quantity / 100  (if unit is grams)
factor = quantity        (if unit is serving, cup, bowl)

calories = food.calories_per_100g × factor
protein  = food.protein_per_100g  × factor
carbs    = food.carbs_per_100g    × factor
fat      = food.fat_per_100g      × factor
```

Aggregate across all items to obtain meal-level totals.

### 3.3.4 Retrieval-Augmented Generation (RAG)

**Objective**: Ground LLM recommendations in factual nutrition knowledge to prevent hallucination.

**Method**:

1. **Knowledge Base Construction**:
   - Compile documents on macronutrients, micronutrients, portion control, healthy swaps, and dietary guidelines.
   - Chunk documents into passages of 200–500 tokens.
   - Generate embeddings and store in a vector database (e.g., pgvector, Pinecone).

2. **Retrieval**:
   - At recommendation time, formulate a query based on user context (e.g., "user has high sugar intake, low protein").
   - Retrieve top-k relevant passages.

3. **Augmented Generation**:
   - Construct a prompt containing: user profile, recent meal history, retrieved knowledge passages.
   - Instruct the LLM to generate personalized, evidence-based recommendations.

### 3.3.5 Daily Summary Generation

**Objective**: Provide users with actionable daily feedback.

**Method**:

1. Aggregate nutrient totals for the target date.
2. Compare against user goals (calorie target, macro splits).
3. Retrieve 7-day rolling history for trend analysis.
4. Construct a prompt for the LLM:

```
User Profile: [age, sex, weight, goals, preferences]
Today's Intake: [calories, protein, carbs, fat]
7-Day Trend: [daily totals]

Generate 2–4 paragraphs:
1. How today went (positive framing)
2. Comparison to goals
3. Gentle, actionable suggestions
Use warm, non-judgmental tone. Avoid medical advice.
```

5. Store the generated summary with metadata (date, stats) for later retrieval.

### 3.3.6 Image-Based Food Recognition (Phase 3)

**Objective**: Enable meal logging via photographs.

**Method**:

1. **Food Detection**: Use a vision model (e.g., GPT-4 Vision, YOLO-based detector) to identify food regions in the image.

2. **Food Classification**: Assign category labels to each detected region.

3. **Portion Estimation**:
   - Use reference objects (plate, utensils) as scale.
   - Prompt the user for size confirmation (small/medium/large).

4. **Conversion**: Pass detected items to the same nutrition matching and calculation pipeline used for text input.

---

## 3.4 System Implementation

| Component | Technology |
|-----------|------------|
| Backend Framework | FastAPI (Python) |
| Database | PostgreSQL with SQLAlchemy ORM |
| Migrations | Alembic |
| Authentication | JWT (HS256) with bcrypt password hashing |
| LLM Provider | OpenAI GPT-4o-mini / GPT-4 |
| Embedding Model | OpenAI text-embedding-3-small |
| Vector Store | pgvector (PostgreSQL extension) |
| Frontend | React with TypeScript (planned) |

### 3.4.1 API Design

RESTful endpoints organized by resource:

- `POST /api/v1/auth/register` — User registration
- `POST /api/v1/auth/login` — Authentication (returns JWT)
- `PUT /api/v1/users/me` — Update profile
- `POST /api/v1/meals/log` — Log meal from text
- `GET /api/v1/meals` — Retrieve meal history
- `POST /api/v1/recommendations/generate` — Generate daily summary

### 3.4.2 Database Schema

Six primary tables:

1. **users**: Profile, goals, preferences, authentication credentials
2. **meals**: Logged meals with timestamp and source (text/image)
3. **meal_items**: Individual food items within a meal
4. **foods**: Nutrition database entries
5. **nutrient_aggregates**: Per-meal and per-day nutrient totals
6. **recommendations**: Generated summaries with user feedback

---

## 3.5 Evaluation Methodology

### 3.5.1 Parsing Accuracy

- **Dataset**: 200 manually annotated meal descriptions with ground-truth structured data.
- **Metrics**:
  - Precision, Recall, F1 for food item extraction
  - Quantity accuracy (within ±10% of ground truth)
  - Confidence calibration (correlation between confidence scores and correctness)

### 3.5.2 Nutrition Matching Accuracy

- **Dataset**: 500 parsed food names with manually verified matches.
- **Metrics**:
  - Top-1 accuracy
  - Top-3 accuracy
  - Mean Reciprocal Rank (MRR)

### 3.5.3 Recommendation Quality

- **Expert Evaluation**: Nutritionists rate generated summaries on:
  - Factual correctness (1–5)
  - Relevance to user profile (1–5)
  - Actionability (1–5)
  - Tone appropriateness (1–5)

- **User Study**: N=50 participants use the system for 2 weeks:
  - System Usability Scale (SUS) score
  - Self-reported satisfaction
  - Adherence rate (% of suggestions followed)

### 3.5.4 System Performance

- **Latency**: Mean response time for meal logging and recommendation generation
- **Throughput**: Requests per second under load
- **Cost**: API token usage per operation

---

## 3.6 Ethical Considerations

1. **Privacy**: All personal data is encrypted; users can export or delete their data.

2. **Safety**: The system includes disclaimers that it is not a medical device. It avoids extreme dieting advice and uses non-judgmental language to prevent triggering eating disorders.

3. **Transparency**: Users are informed when AI is generating content. Recommendations cite knowledge sources when possible.

4. **Bias Mitigation**: The nutrition database includes diverse cultural foods. Prompts are designed to avoid dietary biases.

---

## 3.7 Summary

This methodology combines large language models for natural language understanding, semantic retrieval for knowledge grounding, and structured databases for accurate nutrition tracking. The modular architecture allows incremental development from a text-only MVP to a full-featured system with image logging and advanced personalization. Evaluation spans technical accuracy, user satisfaction, and ethical compliance.
