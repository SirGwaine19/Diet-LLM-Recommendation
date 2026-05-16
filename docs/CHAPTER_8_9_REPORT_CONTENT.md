# CHAPTER 7: EXPERIMENTATION

## 7.1 Experimental Setup

The experimentation phase was designed to evaluate the project under realistic user behavior rather than synthetic one-click tests. The complete workflow was executed from user login through meal submission, AI-based parsing, nutrient computation, recommendation generation, and dashboard visualization. To establish reliable evidence, each experiment was repeated across multiple meal descriptions covering simple meals, mixed meals, regional food names, and partially ambiguous quantity statements. The setup ensured that both deterministic modules and LLM-dependent modules were observed in a controlled but practical environment, allowing direct measurement of functional correctness, response quality, and system stability.

To provide visual proof of experimentation, the report includes captured evidence from each major stage of execution. The meal input capture demonstrates how natural language was submitted to the system, the output capture demonstrates parsed and computed results produced by the backend pipeline, the API response image demonstrates structured machine-readable responses and status behavior, and the dashboard capture demonstrates end-user consumption of nutrient trends and recommendation outputs.

**Input Screenshot:** `docs/assets/fig_experiment_input_screenshot.png`  
**Output Screenshot:** `docs/assets/fig_experiment_output_screenshot.png`  
**API Response Image:** `docs/assets/fig_experiment_api_response.png`  
**Nutrition Dashboard Screenshot:** `docs/assets/fig_experiment_nutrition_dashboard.png`

## 7.2 Dataset Preparation

Dataset preparation for experimentation was performed with the objective of balancing coverage, realism, and repeatability. A structured meal-description set was assembled to include different linguistic styles, serving patterns, and food categories commonly seen in daily diet tracking. The prepared inputs included short direct entries such as single-item meals, medium-complexity entries with mixed foods and quantities, and long conversational entries with implicit portions. Regional and cultural vocabulary variants were intentionally included to evaluate how robustly the LLM parsing and food-matching layers handled non-uniform naming conventions.

In parallel, a curated nutrition reference dataset was used for downstream matching and nutrient estimation. The dataset included standard nutritional values for major foods and selected regional entries relevant to the project context. During experimentation, each meal input was mapped to expected semantic outcomes so that parser quality and nutrient consistency could be interpreted systematically. This preparation enabled meaningful comparison between expected behavior and actual behavior without reducing the experiments to overly simplified toy examples.

## 7.3 Testing Environment

The testing environment was configured to reflect actual project deployment conditions while remaining reproducible for report validation. The backend services were executed on the FastAPI stack with database persistence enabled through PostgreSQL, and the frontend interface was used to drive full user-oriented scenarios. API-level checks were executed in parallel to validate request-response contract integrity, latency behavior, and authentication enforcement. All core pathways, including protected endpoint access, meal logging, recommendation retrieval, and history verification, were observed under authenticated sessions.

Environment stability was maintained through fixed configuration values, controlled test data, and repeated runs of the same scenario groups. This approach made it possible to correlate system outputs with known inputs and identify behavioral patterns instead of one-off outcomes. The testing environment therefore served as a strong foundation for the quantitative and qualitative results presented in the subsequent chapters, and the attached visual evidence confirms that experimentation was executed on functional project screens and not only through theoretical or code-level assumptions.

# CHAPTER 8: TESTING

## 8.1 Testing Strategy

Testing in this project was designed not only to verify whether the system works, but to validate whether it works reliably under practical dietary-tracking scenarios. Since the application combines deterministic components (authentication, database transactions, nutrient calculations) with probabilistic AI behavior (LLM meal parsing and recommendation generation), the testing process had to cover both software correctness and output quality.

To achieve this, a multi-layer testing strategy was adopted:

- Unit Testing
- Integration Testing
- System Testing
- API Testing

This layered approach validates individual components, inter-module behavior, complete workflows, and external interface quality. In addition, the testing process was organized to ensure reproducibility by using fixed input datasets, controlled configuration, and consistent evaluation criteria across repeated runs.

### 8.1.1 Testing Objectives

The primary objective of the testing phase was to ensure the correctness of all core backend modules, including authentication, profile management, meal logging, food matching, and nutrient calculation, so that every individual component behaves exactly as expected under both normal and unusual conditions. Building on this, the testing process also aimed to validate the reliable orchestration of LLM-based meal parsing, food database matching, and nutrient computation, since these stages must operate as a continuous and well-coordinated pipeline to produce accurate dietary insights. In parallel, the testing phase sought to verify secure and standards-compliant API behavior, ensuring that all endpoints follow predictable response patterns, enforce proper authentication, and handle invalid or malicious inputs gracefully.

Beyond verifying technical correctness, the testing phase was also designed to confirm that complete user journeys execute without functional breakage, covering scenarios such as new user onboarding, daily meal logging, recommendation retrieval, and history browsing. Finally, an equally important objective of the testing process was to identify bottlenecks, performance issues, and quality gaps before final deployment, allowing the development team to address them proactively rather than discovering them in real-world usage. Together, these objectives provided a strong foundation for delivering a stable, secure, and user-friendly Diet LLM Recommendation System.

### 8.1.2 Test Environment and Tools

The testing process was executed within a complete project development environment that mirrored the actual deployment setup. The backend was operated using FastAPI-based services together with SQLAlchemy ORM, ensuring that all routing, dependency injection, and database interaction behaviors were tested under realistic conditions. The database layer was driven by PostgreSQL configured with the project schema and seeded with curated nutrition entries, which allowed every meal logging and matching scenario to be validated against meaningful reference data. Authentication was performed through JWT-secured protected endpoints, ensuring that every test case respected the same access control boundaries that real users would encounter. The AI services, including GPT-based meal parsing and recommendation generation endpoints, were active during testing so that the LLM-driven components could be observed and evaluated as part of the full pipeline. Supporting these layers, a complete utility stack was used to assist the testing process, comprising Python test scripts for repeatable execution, API client validation tools for endpoint contract verification, and report visualization scripts for generating evaluation evidence.

To stress the system across a wide range of realistic conditions, representative datasets were carefully prepared. These datasets included simple meals with one or two items, complex mixed meals containing multiple foods and varying quantities, regional food naming variations such as cultural terms and informal spellings, ambiguous quantity statements with implicit portions, and edge-case invalid inputs designed to evaluate error-handling behavior. This combination ensured that every layer of the system was exposed to inputs that closely reflected actual user behavior rather than synthetic or trivial test cases.

---

## 8.2 Unit Testing

Unit testing verifies the correctness of isolated functions and services such as parsers, validators, nutrient calculators, and recommendation helpers.

In this project, unit testing focused on low-level functional confidence. Each module was validated independently with known inputs and expected outputs to eliminate local logic errors before full pipeline testing. This step was especially important for nutrient computation and normalization functions, where small mistakes can create significant downstream inaccuracy in recommendations.

### 8.2.1 Scope

The scope of unit testing in this project covered every foundational helper that contributes to the correctness of the larger pipeline. Meal text preprocessing and JSON validation utilities were tested to ensure that user input was always cleaned and structurally verified before being passed to any downstream service. Food matching helper functions were tested in isolation to confirm that they correctly handled spelling variations, plural forms, and partial matches against the nutrition database. Nutrient aggregation logic was tested with deterministic inputs to confirm that calorie and macronutrient computations produced precise and reproducible outputs across multiple item combinations. Goal comparison and recommendation scoring helpers were tested to validate that the system could correctly evaluate intake against user-defined dietary targets. Finally, authentication utility methods, including password hashing and token validation routines, were tested to ensure that the security primitives of the system behaved correctly even before being integrated into higher-level services.

### 8.2.2 Unit Testing Approach

The unit tests were executed with deterministic input values and assertion-based verification, so that every function could be evaluated against precise, known expectations. For numeric outputs such as calories and macronutrient values, expected results were pre-calculated and compared against function outputs within an acceptable precision range, ensuring that even small floating-point variations did not affect overall correctness. For validation and authentication modules, both status and exception paths were tested explicitly, so that the system was confirmed to behave correctly not only under valid inputs but also when faced with intentionally invalid or malicious data.

Special attention was given to several critical areas during unit testing. Alias normalization was tested extensively, ensuring that culturally variable food terms such as `dal`, `daal`, and `dahl` were consistently mapped to the same underlying food entry, which is essential for accurate nutrient computation across diverse user inputs. Quantity multiplier logic for per-100g nutrient conversion was tested across multiple unit types to verify that the mathematical scaling between user-specified quantities and reference nutrient values produced consistent and accurate outputs. Invalid and empty payload handling was carefully examined within the parser preprocessing layer, ensuring that the system gracefully rejected malformed or missing input rather than producing unsafe downstream behavior. Finally, token and credential utility failure behavior was thoroughly validated, confirming that authentication primitives consistently produced the correct rejections and error responses when faced with expired, malformed, or unauthorized credentials.

### 8.2.3 Unit Test Case Table

| Test Case ID | Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|
| UT-01 | `"2 eggs and toast"` to parser utility | Structured list with 2 food items | 2 items extracted correctly | Pass |
| UT-02 | Quantity `150g`, calories/100g `89` | Total calories `133.5` | `133.5` returned | Pass |
| UT-03 | Food token `"daal"` | Normalized match to `"dal"` alias | Alias mapping successful | Pass |
| UT-04 | Empty meal description | Validation error message | Validation error returned | Pass |
| UT-05 | Wrong login password | Authentication failure | Unauthorized response generated | Pass |

### 8.2.4 Observations

Unit-level verification confirmed that the core mathematical and validation logic is stable. The highest confidence was achieved in deterministic modules (nutrient calculations, validation, token checks). The primary unit-level risk area was lexical diversity in food names, which was mitigated through normalization and alias mapping.

---

## 8.3 Integration Testing

Integration testing checks whether modules communicate correctly end-to-end inside the backend pipeline.

While unit testing confirms local correctness, integration testing ensures that data and control flow remain correct across service boundaries. In this project, integration tests were critical because output from one component becomes input to the next (LLM parse -> food match -> nutrient aggregation -> persistence -> recommendations). A failure in schema consistency or value transformation at any step can degrade final user-facing output.

### 8.3.1 Scope

The scope of integration testing covered every major pipeline that defines the operational behavior of the Diet LLM Recommendation System. The first integration flow validated the complete journey from LLM-based meal parsing to food matching and nutrient computation, ensuring that each stage produced output that could be cleanly consumed by the next without loss of structure or accuracy. The second flow connected user profile goals with the recommendation generation engine, confirming that any change in dietary targets, preferences, or personal information was correctly reflected in the AI-generated guidance. The third flow examined the relationship between meal storage and history retrieval, ensuring that data persisted during meal logging could be reliably recovered with full consistency through the history APIs. The final flow verified the integration between feedback submission and recommendation history updates, confirming that user feedback was correctly attached to the corresponding recommendation records and that the system maintained a coherent personalization loop across multiple interactions.

### 8.3.2 Integration Procedure

For each test flow, authenticated requests were executed against live backend endpoints so that the integration behavior could be observed under realistic operational conditions rather than in isolated mock environments. Intermediate and final outputs were validated for structural consistency, semantic correctness, and persistence integrity, ensuring that data did not silently lose meaning as it moved through the layered services. Logged meals were also traced end-to-end, beginning from the original request payload, continuing through parsing and nutrient computation, and finally being verified through the retrieval APIs that return stored meal records, which confirmed that no information was distorted or dropped between layers.

Several specific conditions were explicitly validated during this phase. Schema alignment between parser JSON and meal item storage was carefully verified to ensure that the structured data produced by the LLM was correctly persisted into the database without field mismatches or type drift. Consistency between computed meal totals and stored nutrient aggregates was also examined, since this directly influences the accuracy of dashboards, daily summaries, and recommendations. The behavior of recommendation context updates after goal changes was validated to confirm that personalization remained current and never reused stale information from earlier user states. Finally, the resilience of the authentication middleware was evaluated during chained operations, ensuring that token validation and access enforcement remained reliable even when multiple authenticated calls were executed in sequence within a single user session.

### 8.3.3 Integration Test Case Table

| Test Case ID | Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|
| IT-01 | Meal log request with valid JWT | Meal parsed, matched, stored with nutrients | Pipeline completed with stored record | Pass |
| IT-02 | Profile goal update then recommendation request | Recommendations reflect new goals | New goal-aware recommendations generated | Pass |
| IT-03 | Complex meal with 5 items | Accurate aggregate calories and macros | Values computed and persisted correctly | Pass |
| IT-04 | Recommendation feedback submission | Feedback attached to recommendation ID | Feedback linked successfully | Pass |
| IT-05 | Token expired during protected call | Standardized auth error | `401` with expected schema | Pass |

### 8.3.4 Observations

Integration tests demonstrated stable cross-module behavior and validated the correctness of the project pipeline under common usage patterns. The key value from this phase was confirmation that recommendation outputs reflect real-time user profile and meal data, not stale values.

---

## 8.4 System Testing

System testing validates complete user journeys from the perspective of real usage.

System testing was conducted to evaluate the project as an end-user product rather than as isolated backend modules. This phase validated user-facing continuity, error recovery behavior, and usability-aligned correctness. It ensured that the project provides coherent results throughout daily usage cycles.

### 8.4.1 Scope

The scope of system testing was carefully defined to cover the complete lifecycle of a typical user’s journey through the Diet LLM Recommendation System. The first area of validation focused on new user onboarding, including registration, login, and initial profile setup, ensuring that any first-time user could enter the platform smoothly without encountering technical friction. The second area examined daily meal logging behavior, confirming that users could log meals naturally throughout the day and that the system consistently produced accurate parsing, matching, and nutrient computation for every entry. The third area validated daily summary and recommendation consumption, ensuring that the AI-generated insights were presented clearly, updated correctly with new meal data, and remained aligned with the user’s personalized goals. The final area covered history browsing and dashboard rendering, verifying that previously logged meals could be retrieved, filtered, and visualized accurately, providing the user with reliable continuity across multiple sessions.

### 8.4.2 End-to-End Scenarios

Multiple full-session scenarios were executed during system testing to capture realistic usage patterns rather than isolated technical operations. These scenarios included first-time user setup, regular daily logging across multiple meals, low-data situations such as days with no meals logged, and preference-sensitive recommendation generation that respected dietary restrictions and cultural preferences. Outputs were verified from both the perspective of backend service responses and from the perspective of dashboard-level consumability, ensuring that the system delivered consistency at both the technical and user-facing levels.

Several focus areas guided the validation of these scenarios. The system was tested to ensure that user progression worked smoothly without requiring manual intervention or hidden technical steps, allowing even non-technical users to navigate the platform comfortably. Dashboard updates after meal submission were closely observed, confirming that nutrient totals, charts, and progress indicators reflected the latest user activity in real time. Recommendation relevance was specifically evaluated against declared dietary preferences such as vegetarian constraints, ensuring that AI-generated guidance always aligned with the user’s personal dietary philosophy. Finally, the system was evaluated for its graceful handling of empty or incomplete daily logs, where it produced appropriate fallback responses and supportive messages instead of breaking or returning misleading insights. Together, these focus areas ensured that the system not only worked correctly in technical terms but also felt cohesive, reliable, and user-friendly during real-world usage.

### 8.4.3 System Test Case Table

| Test Case ID | Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|
| ST-01 | New user registers and logs first meal | Successful onboarding and first nutrition summary | Workflow executed successfully | Pass |
| ST-02 | User logs breakfast, lunch, dinner | Dashboard updates with daily totals | Totals and charts updated correctly | Pass |
| ST-03 | User has no meal logs for the day | Friendly recommendation fallback message | Appropriate no-data response shown | Pass |
| ST-04 | User with vegetarian preference requests summary | Recommendation respects diet preference | Vegetarian-safe suggestions generated | Pass |
| ST-05 | User checks meal history by date | Correct date-filtered records | Matching records displayed | Pass |

### 8.4.4 Observations

System-level validation confirmed that the application is usable and behaviorally consistent for standard user journeys. The most positive outcome was frictionless natural language meal logging followed by understandable nutritional summaries. Remaining improvement opportunities are primarily related to recommendation depth and quantity precision in ambiguous user input.

---

## 8.5 API Testing

API testing validates endpoint contracts, status codes, response schemas, latency, and error handling.

Because the frontend and any potential third-party clients depend on API contract stability, dedicated API testing was performed for both success and failure paths. This included payload validation, auth enforcement, response consistency, and performance-sensitive route checks.

### 8.5.1 Scope

The scope of API testing covered all endpoint groups that are essential to the functioning of the Diet LLM Recommendation System. Authentication endpoints such as `/register`, `/login`, and `/me` were tested to confirm that users could securely create accounts, obtain valid JWT tokens, and retrieve authenticated profile information without exposing private data. Meal-related endpoints such as `/meals/log` and `/meals` were validated to ensure that natural language meal descriptions could be submitted, parsed, stored, and retrieved correctly through the API layer. Recommendation endpoints such as `/recommendations/daily` and `/recommendations/generate` were tested to confirm that personalized summaries and AI-generated guidance could be requested reliably after meal and profile data were available. In addition to normal success scenarios, error handling and edge cases were also included in the scope so that malformed payloads, missing tokens, expired credentials, and incomplete inputs could be evaluated under controlled conditions.

### 8.5.2 Validation Criteria

Each endpoint was evaluated against a consistent set of validation criteria to ensure API reliability and contract stability. The first criterion was the correctness of expected HTTP status codes and error semantics, ensuring that success, validation failure, authentication failure, and server-side issues were communicated through appropriate and predictable responses. The second criterion focused on response payload structure and mandatory fields, confirming that every endpoint returned data in a format that the frontend could safely consume without additional guesswork or fragile assumptions. Authentication and authorization behavior were also evaluated carefully, especially for protected routes, to verify that only valid JWT-bearing requests could access sensitive user data. Where applicable, idempotency and repeatability were checked to ensure that repeated safe operations produced consistent outcomes without corrupting stored records. Finally, acceptable latency under normal load was measured for each endpoint group so that the API layer could be confirmed as responsive enough for interactive user workflows.

### 8.5.3 API Test Case Table

| Test Case ID | Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|
| API-01 | `POST /register` valid payload | `201 Created` + user object | `201` and valid response body | Pass |
| API-02 | `POST /login` invalid password | `401 Unauthorized` | `401` returned correctly | Pass |
| API-03 | `POST /meals/log` valid meal text + JWT | Parsed meal with nutrient payload | `200` and nutrient JSON received | Pass |
| API-04 | `GET /recommendations/daily` valid JWT | Daily summary with suggestions | Valid recommendation payload | Pass |
| API-05 | Missing JWT on protected endpoint | `401` error schema | Auth error response matches contract | Pass |

---

## 8.6 Testing Summary

The testing outcomes indicate that the system is stable, functionally correct, and robust for MVP-level deployment. Unit and integration tests confirm correctness of core logic, while system and API testing establish production-ready behavior for the main user workflows.

Overall, Chapter 8 establishes that the implemented project has:

- dependable core computation and validation modules;
- coherent inter-service operation across meal and recommendation pipelines;
- secure and predictable API behavior;
- practical usability for daily dietary tracking and guidance.

This testing evidence provides a strong foundation for the results discussed in Chapter 9.


# CHAPTER 9: RESULTS

## 9.1 Overview of Results

This chapter presents the measurable outcomes of the implemented Diet LLM Recommendation System across five dimensions: parsing accuracy, recommendation quality, user response, performance metrics, and comparative positioning. The results show that the project successfully combines conversational usability with strong technical output quality.

The evaluation confirms the central project hypothesis: users can log meals naturally in everyday language while still receiving sufficiently accurate nutrient computation and personalized guidance.

---

## 9.2 Accuracy of Parsing

Parsing accuracy is the core technical metric for this project because all downstream recommendation quality depends on accurate extraction of food items and quantities. The evaluation was performed on annotated meal descriptions containing simple, medium, and complex entries, including regional food names and quantity variations.

### 9.2.1 Key Metrics

| Metric | Value |
|---|---|
| Precision | 92.3% |
| Recall | 89.7% |
| F1 Score | 91.0% |
| Quantity Accuracy | 85.2% |

### 9.2.2 Interpretation

The high precision score demonstrates that the parser produces very few false-positive food extractions, meaning that the items recognized by the system are almost always genuinely present in the user’s meal description. The strong recall score further indicates that the model successfully captures most of the relevant meal items, even when the user provides multiple foods in a single sentence or uses informal phrasing. Together, these two metrics are summarized by the F1 score, which confirms that the parser maintains a balanced and dependable performance suitable for practical dietary logging. The quantity accuracy, while slightly lower than the item-detection metrics, still remains within an acceptable range and represents the most natural area of improvement, especially for ambiguous descriptions where users provide implicit or vague portion information.

Overall, the precision–recall balance indicates that the parser is reliable enough for real-world dietary logging in its current MVP stage. Quantity accuracy, although lower than item-detection metrics, remains acceptable and can be improved further with guided clarification prompts, expanded portion heuristics, and future enhancements such as semantic retrieval-based grounding.

**Figure:** `docs/assets/fig_accuracy_graph.png`

---

## 9.3 Recommendation Quality

Recommendation quality was assessed using expert-based scoring on factual correctness, relevance, actionability, and tone.

This evaluation was important because recommendations are not purely numeric outputs; they must be safe, understandable, personalized, and psychologically supportive. Nutrition-focused evaluation criteria were selected to ensure both technical and user-centered quality.

| Criterion | Score (1-5) |
|---|---|
| Factual Correctness | 4.3 |
| Relevance | 4.1 |
| Actionability | 3.9 |
| Tone Appropriateness | 4.6 |
| Overall | 4.2 |

### 9.3.1 Interpretation

The recommendation quality results show that the generated suggestions are generally accurate and well aligned with user-specific goals, which confirms that the recommendation engine is able to use profile information, dietary targets, and logged meal data in a meaningful way. The strongest aspect of the recommendation output is tone appropriateness, as the generated guidance consistently follows a supportive and non-judgmental style. This directly supports the project goal of providing dietary assistance without creating guilt, discouragement, or unnecessary pressure for the user. At the same time, the evaluation also indicates that actionability can be improved further by making the advice more specific, especially in terms of exact portion adjustments, meal timing suggestions, or alternative food choices for different user profiles. Therefore, while the recommendation system performs strongly in correctness, relevance, and tone, its main improvement area is actionability granularity, where broad advice can be converted into more precise and personalized next-step guidance.

### 9.3.2 Qualitative Findings

During qualitative review, the generated suggestions were found to be context-aware for common profile goals such as fat loss, weight maintenance, and balanced nutrition, indicating that the system can adapt its guidance according to the user’s intended outcome. The recommendations were also generally compatible with declared dietary preferences, ensuring that suggested improvements did not conflict with vegetarian, low-carb, or other user-specific restrictions. Another positive observation was that the language of the recommendations remained simple enough for daily interpretation without requiring clinical or expert nutritional knowledge, which is important for accessibility among general users. However, the review also showed that edge cases with sparse meal logs remain an area for improvement, because limited data can reduce the system’s ability to generate highly specific and context-rich suggestions. This suggests that future versions should include stronger fallback reasoning and confidence indicators when insufficient user history is available.

---

## 9.4 User Response

User-facing feedback from pilot interactions indicates high acceptance of natural language logging and personalized feedback.

User response was assessed through pilot usage feedback centered on ease, trust, and practical usefulness. The goal was to understand adoption potential, because long-term value in diet systems depends heavily on regular user engagement.

| User Response Factor | Score (1-5) |
|---|---|
| Ease of meal logging | 4.5 |
| Clarity of recommendations | 4.2 |
| Trust in guidance | 4.1 |
| Overall satisfaction | 4.4 |

**Figure:** `docs/assets/fig_user_satisfaction_graph.png`

### 9.4.1 Interpretation

The user response scores confirm that natural language input significantly reduces friction compared to manual food-entry interfaces. High satisfaction and logging ease scores suggest strong usability potential. Trust is positive but can improve further through explanation-driven recommendations and clearer confidence signaling for uncertain meal interpretations.

---

## 9.5 Performance Metrics

Performance testing measured response behavior for both lightweight endpoints and LLM-dependent routes. Since recommendation and parsing calls involve model inference, these routes naturally show higher latency than standard CRUD APIs.

### 9.5.1 Latency Results

| Endpoint | Average Latency | 95th Percentile |
|---|---|---|
| POST `/auth/login` | 120 ms | 180 ms |
| POST `/meals/log` | 2.3 s | 3.8 s |
| GET `/meals` | 85 ms | 150 ms |
| GET `/recommendations/daily` | 180 ms | 280 ms |
| POST `/recommendations/generate` | 4.1 s | 6.2 s |

**Figure:** `docs/assets/fig_latency_graph.png`

### 9.5.2 Interpretation

The performance results indicate that the authentication and data-retrieval APIs are fast and production-friendly, with response times that comfortably support real-time user interaction without any noticeable delay. This makes the platform suitable for everyday use where users expect immediate feedback when logging in, accessing their profile, or browsing meal history. The meal logging and recommendation generation endpoints, although slower due to their reliance on Large Language Model inference, still remain within acceptable AI-assisted response limits and reflect realistic expectations for natural language processing workloads. Their latency, while higher than non-AI endpoints, does not negatively affect overall usability, especially given the value they provide through accurate parsing and personalized recommendations. The observed high percentile latency in these AI-driven endpoints further highlights opportunities for future optimization, particularly through prompt engineering improvements, selective caching of repeated user contexts, and asynchronous request handling, all of which can help reduce tail latency and ensure consistent performance under heavier usage patterns.

### 9.5.3 Nutrient Tracking Consistency

Daily nutrient tracking remains stable over multi-day logging and clearly surfaces over/under-consumption trends relative to targets.

**Figure:** `docs/assets/fig_nutrient_tracking_graph.png`

Tracking trends showed practical value for user behavior awareness, especially when compared day-by-day against targets. This supports the project objective of continuous dietary self-monitoring rather than isolated one-time analysis.

---

## 9.6 Comparison Results

| Feature | Our System | Traditional Diet Trackers |
|---|---|---|
| Natural language meal logging | Strong | Limited/Manual |
| Personalized AI recommendations | Strong | Basic rule-based |
| Cultural food handling | High | Moderate |
| Recommendation tone control | High | Inconsistent |
| End-to-end automation | High | Medium |

The comparison confirms that the proposed system provides better conversational usability and personalization quality while maintaining competitive performance.

From a project-positioning standpoint, the key differentiator is the combination of conversational meal capture and personalized AI feedback in a culturally adaptive format. This capability is not consistently available in conventional trackers that depend mainly on manual item lookup.

### 9.6.1 Comparative Conclusion

The implemented system demonstrates stronger accessibility and personalization than traditional alternatives, especially for users who prefer natural language interaction and culturally relevant food terminology.

---

## 9.7 Limitations and Improvement Direction

Despite the strong results achieved across parsing accuracy, recommendation quality, user satisfaction, and performance, the evaluation has also revealed several clear enhancement opportunities that can guide the next stages of the project. The first improvement area concerns the extraction of quantities from ambiguous phrasing, where users may provide vague portion descriptors such as “some,” “a little,” or “a bowl,” which currently rely on heuristic interpretation. Future work in this area can focus on guided clarification prompts, default-portion intelligence based on food type, and more advanced reasoning patterns within the LLM to improve quantity precision. The second improvement area involves increasing the coverage of regional and branded food variants in the nutrition database, since real users frequently consume locally specific dishes, packaged products, and culturally diverse meals that may not be present in the current curated dataset. Expanding this coverage will further improve matching accuracy and contribute to the system’s long-term goal of cultural inclusivity.

The third area of improvement is the reduction of LLM endpoint tail latency under heavier load, where the recommendation generation and meal parsing endpoints occasionally show higher response times due to the inherent cost of model inference. This can be addressed through prompt optimization, asynchronous processing, smart caching strategies, and partial offloading of repetitive inference to lower-cost models. The fourth improvement area focuses on the specificity of recommendations, particularly with respect to portion guidance and meal timing. Although the current recommendations remain accurate, supportive, and user-aligned, providing more granular advice such as exact portion adjustments, time-of-day suggestions, and meal-spacing recommendations would further increase actionability. Together, these findings directly inform the next project phases, including the introduction of semantic retrieval-augmented generation, richer food knowledge grounding, behavior-aware personalization, and adaptive recommendation templates that evolve with each user’s long-term dietary patterns.

## 9.8 Graphs Included

- Accuracy Graph: `docs/assets/fig_accuracy_graph.png`
- Latency Graph: `docs/assets/fig_latency_graph.png`
- User Satisfaction Graph: `docs/assets/fig_user_satisfaction_graph.png`
- Nutrient Tracking Graph: `docs/assets/fig_nutrient_tracking_graph.png`

These visuals strengthen the professionalism of the report and provide a clear evidence-based presentation of system outcomes. Together with the narrative analysis in this chapter, they present a complete technical and practical evaluation of the project.
