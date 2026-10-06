# System Architecture & Technical Specification: Google Photos Discovery Engine

## Core Objective & AI LLM Integration Context

As defined in the project objective ([problemstatement.md](file:///c:/Users/prakh/OneDrive/Desktop/new_life/pm_projects/V5/problemstatement.md)), this system builds an **AI-powered qualitative discovery engine** for Google Photos retrieval. 

The primary objective is achieved by **connecting the available AI LLM client** to act as an autonomous qualitative research analyst. Rather than relying on superficial sentiment analysis, star-rating aggregations, or static keyword regex, the system connects directly to the LLM client to uncover latent, complex patterns across large volumes of authentic user conversations:

1. **Cognitive Memory Modeling (Steps 4A & 4B):** The connected LLM client extracts what users actually remember vs. forget (using a strict Tri-State Memory Model) grounded in exact verbatim evidence spans.
2. **Behavioral Search Dynamics (Step 5):** The LLM parses search reformulation journeys, query tactic changes, and multi-turn adaptations.
3. **Failure Mode Diagnosis (Step 7):** The LLM classifies the exact cognitive or systemic breakdown stage across the retrieval journey.
4. **Emergent Pattern Synthesis & Clustering (Step 8):** The LLM performs emergent semantic clustering without artificial category caps to derive grounded problem archetypes.
5. **Key Analytical Insights & Opportunity Hypotheses (Step 10 & Dashboard):** The LLM answers the 10 foundational PM analytical questions and formulates non-prescriptive, evidence-backed product opportunity spaces for downstream product strategy.

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                LLM CLIENT CONNECTION & ORCHESTRATION LAYER                             │
│                                                                                                        │
│  [Configured LLM Client] ──► [Structured JSON Schema Mode] ──► [Verbatim Evidence Span Grounding]       │
│           │                                                                                            │
│           ├──► Step 3: Retrieval Relevance Binary Classification & Noise Exclusion                     │
│           ├──► Step 4A: Remembered Clues Qualitative Extraction & Categorization                       │
│           ├──► Step 4B: Tri-State Memory Profile Identification (Remembered / Forgotten / Omitted)     │
│           ├──► Step 5: Multi-Attempt Query Sequence Reconstruction & Tactic Shift Tracking             │
│           ├──► Step 6: Unambiguous Retrieval Outcome Determination (Success / Partial / Fail / Unknown)│
│           ├──► Step 7: 4-Stage Journey Breakdown Diagnosis & Attribution                               │
│           ├──► Step 8: Emergent Problem Clustering & Qualitative Archetype Synthesis                   │
│           └──► Step 10: Non-Prescriptive Opportunity Hypotheses Generation & Research Questions        │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## System Overview & Architecture Diagram

The **Google Photos Discovery Engine** is an AI-powered qualitative research pipeline and dashboard designed to discover, categorize, and quantify photo retrieval failure modes from real-world user conversations. It ingests authentic feedback from multiple public channels, cleans and filters for retrieval relevance, executes deep multi-dimensional qualitative LLM extraction, clusters emergent retrieval breakdowns, quantifies behavioral metrics, and surfaces evidence-grounded product opportunities.

```text
========================================================================================================
                                 GOOGLE PHOTOS DISCOVERY ENGINE ARCHITECTURE
========================================================================================================

 [PHASE 1: INGESTION & PREPARATION]
  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ STEP 1: Data Ingestion                                                                           │
  │ • Sources: Play Store, App Store, Help Community, Reddit, YouTube, Forums, Social Discussions    │
  │ • Output: raw_conversations.json + ingestion-exceptions.md                                       │
  └─────────────────────────────────────────────────┬────────────────────────────────────────────────┘
                                                    │
                                                    ▼
  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ STEP 2: Cleaning & Normalisation                                                                 │
  │ • Remove duplicates, strip spam/bots, unify canonical schema, preserve verbatim text             │
  │ • Output: normalized_conversations.json                                                          │
  └─────────────────────────────────────────────────┬────────────────────────────────────────────────┘
                                                    │
                                                    ▼
  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ STEP 3: Relevance Classification                                                                 │
  │ • Filter: Photo retrieval focus vs unrelated issues (storage, billing, login, sync/backup)       │
  │ • Output: relevant_conversations.json + irrelevant_conversations.json                            │
  └─────────────────────────────────────────────────┬────────────────────────────────────────────────┘
                                                    │
                                                    │ (Relevant Conversations Corpus)
                                                    ▼
 [PHASE 2: DEEP QUALITATIVE LLM EXTRACTION]
  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ STEP 4A: Remembered Clues Extraction                                                             │
  │ • Categories: Time, Location, People, Objects, Activity, Event, Visuals, Text/OCR, Context       │
  │ • Output: remembered_clues.json (with exact verbatim evidence spans)                             │
  ├──────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ STEP 4B: Forgotten Clues & Tri-State Memory                                                      │
  │ • Tri-State Model: Explicitly Remembered | Explicitly Forgotten | Not Mentioned                  │
  │ • Output: memory_gaps.json (No inferred forgetting from omission)                                │
  ├──────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ STEP 5: Multi-Search Attempt Journey                                                             │
  │ • Preserves query sequence, reformulation tactics, browsing shifts, and final outcome            │
  │ • Output: multi_search_journeys.json                                                             │
  ├──────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ STEP 6: Retrieval Outcome Classification                                                         │
  │ • Mutually Exclusive: Success | Partial Success | Failure | Unknown                              │
  │ • Output: retrieval_outcomes.json                                                                │
  ├──────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ STEP 7: Retrieval Journey Breakdown Stage                                                        │
  │ • Stages: 1. Translation | 2. System Retrieval | 3. Result Overload | 4. Refinement/Abandonment  │
  │ • Output: failure_stages.json                                                                    │
  └─────────────────────────────────────────────────┬────────────────────────────────────────────────┘
                                                    │
                                                    ▼
 [PHASE 3: SYNTHESIS, CLUSTERING & QUANTIFICATION]
  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ STEP 8: Emergent Problem Clustering                                                              │
  │ • Semantic clustering of shared failure patterns (no artificial fixed quotas, allow noise)       │
  │ • Output: problem_clusters.json + unclustered_records.json                                       │
  └─────────────────────────────────────────────────┬────────────────────────────────────────────────┘
                                                    │
                                                    ▼
  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ STEP 9: Metric Quantification                                                                    │
  │ • Transparent stats: Explicit numerators & denominators across outcomes, stages, & clue types    │
  │ • Output: quantification_metrics.json                                                            │
  └─────────────────────────────────────────────────┬────────────────────────────────────────────────┘
                                                    │
                                                    ▼
  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ STEP 10: Opportunity Identification                                                              │
  │ • Evidence-backed hypotheses & research questions (no premature solution/feature prescribing)    │
  │ • Output: opportunity_hypotheses.json                                                            │
  └─────────────────────────────────────────────────┬────────────────────────────────────────────────┘
                                                    │
                                                    ▼
 [PHASE 4: DASHBOARD UI (FLUENT 2)]
  ┌────────────────────────┬────────────────────────┬────────────────────────┬───────────────────────┐
  │ 1. Overview Analytics  │ 2. Problem Clusters    │ 3. 10 Analytical Qs    │ 4. Opportunity Cards  │
  │ (KPIs, Outcomes, Funnel│ (Memory, Failure Stage,│ (Struggle photo types, │ (Evidence, Segments,  │
  │  Top Clusters, Takeaway│  Quotes, Modal Viewer) │  Formulation, Drop-off)│  Research Questions)  │
  └────────────────────────┴────────────────────────┴────────────────────────┴───────────────────────┘
```

---

# Pipeline Steps Specification

---

## STEP 1 — DATA INGESTION

### Purpose
Collect authentic, unfiltered public user reviews, discussions, and conversations across multiple public channels regarding Google Photos over the past 3 to 5 years. Capture rich real-world retrieval experiences without fabricating synthetic data, while maintaining complete source traceability and logging any API/scraping exceptions in `ingestion-exceptions.md`.

### Input
- **Target Channels & Endpoints:**
  - Google Play Store (`com.google.android.apps.photos`)
  - Apple App Store (`id962194608`)
  - Google Photos Help Community (`support.google.com/photos/community`)
  - Reddit (`r/googlephotos`, `r/google`, search keywords)
  - YouTube (Comments on official and feature review videos)
  - Public Forums (Android Central, MacRumors, Google Product Forums)
  - Social Discussions (X / Twitter, Threads, Quora, Public Facebook)
- **Search Query Seeds:** "Google Photos search", "can't find photos", "search not working", "photo retrieval", "find old photos", "search by text/person/date/location", "similar photos", "Ask Photos", "Gemini search", "search relevance".
- **Lookback Window:** Configurable 2 years.
- **Language Filter:** English.

### Output
- **Raw Ingested Records Dataset (`raw_conversations.json` / Database Table):**
  - `record_id`: Unique UUIDv5 based on `source` + `source_id` / `source_url`.
  - `source`: Platform name (`google_play`, `app_store`, `reddit`, `youtube`, `google_help_community`, `forums`, `social`).
  - `source_type`: Channel category (`app_review`, `forum_thread`, `community_post`, `video_comment`, `social_post`).
  - `source_url`: Verifiable URL of the discussion/review.
  - `source_id`: Native platform ID.
  - `date`: ISO 8601 publication timestamp.
  - `author_identifier`: Anonymized/pseudonymized author handle or ID.
  - `original_text`: Verbatim text content preserving formatting and punctuation.
  - `rating`: Star rating (1–5) if available, else `null`.
  - `language`: Detected ISO language code (e.g., `en`).
  - `collection_timestamp`: ISO 8601 ingestion timestamp.
  - `provenance_status`: Initial status set to `Unverified` or `Verified Genuine`.
- **Exception Log (`ingestion-exceptions.md`):** Detailed documentation of failed endpoints, rate limits, access blocks, and applied alternative substitutes.

---

## STEP 2 — CLEANING & NORMALISATION

### Purpose
Clean, deduplicate, sanitize, and unify the ingested raw records into a standardized canonical schema. Strip spam, bot submissions, automated advertisements, and duplicate cross-posts while preserving exact text verbatim and maintaining full source provenance.

### Input
- Dataset of raw records generated in **STEP 1** (`raw_conversations.json`).
- Preprocessing rules, spam heuristics, hashing algorithms, and character normalization definitions.

### Output
- **Normalized Records Dataset (`normalized_conversations.json`):**
  - Standardized JSON/relational structure matching canonical fields (`record_id`, `source`, `source_type`, `source_url`, `source_id`, `date`, `author_identifier`, `cleaned_text`, `original_text`, `rating`, `language`, `collection_timestamp`, `is_duplicate`, `spam_score`, `provenance_status`).
- **Cleaning & Filtering Log:**
  - Metrics detailing count of duplicates removed, spam records excluded, and normalization transformations performed.

---

## STEP 3 — RELEVANCE CLASSIFICATION

### Purpose
Classify each normalized record to filter for genuine photo retrieval conversations and exclude unrelated Google Photos issues (e.g., cloud storage tiers, subscription billing, login/auth errors, sync/backup bugs, photo editing tools, album sharing permissions) unless directly tied to photo retrieval.

### Input
- Normalized conversations dataset from **STEP 2** (`normalized_conversations.json`).
- LLM prompt guidelines and classification rubric specifying retrieval criteria:
  - Finding a specific photo or video.
  - Searching for old/historical photos.
  - Retrieving a photo with incomplete memory or vague recollections.
  - Locating screenshots, scanned documents, receipts, or visual assets.
  - Searching by people, places, objects, activities, events, visual descriptors, or timestamps.
  - Expressing frustration when a known photo cannot be found via search.

### Output
- **Relevant Conversations Corpus (`relevant_conversations.json`):**
  - Records tagged with `is_retrieval_relevant: true`.
  - `relevance_confidence`: Score between 0.0 and 1.0.
  - `relevance_reasoning`: Short explanation grounded in the text.
  - `relevance_category`: Primary topic tag (e.g., `specific_photo_search`, `vague_memory_search`, `document_receipt_retrieval`, `semantic_ask_photos_query`).
  - `provenance_status`: Updated to `Verified Genuine` for downstream research.
- **Irrelevant Conversations Archive (`irrelevant_conversations.json`):**
  - Records tagged with `is_retrieval_relevant: false` and the specific exclusion reason (e.g., `backup_sync_issue`, `storage_quota`, `account_login`).
- **Relevance Metrics Summary:** Total scanned, total relevant, total excluded with category breakdown.

---

## STEP 4A — WHAT DOES THE USER REMEMBER WHEN RETRIEVING PHOTOS?

### Purpose
Analyze each verified relevant conversation to extract the specific memory clues the user recalled when attempting to find the photo. Extract exact verbatim evidence spans for every clue and classify each clue into standard memory categories.

### Input
- Verified relevant conversations corpus from **STEP 3** (`relevant_conversations.json`).
- Memory categorization schema covering:
  - `Time / Temporal`: Year, season, approximate date, time of day.
  - `Location / Spatial`: City, landmark, country, indoor/outdoor, vacation venue.
  - `People / Social`: Faces, family members, friends, specific names, relationship context.
  - `Objects / Items`: Cars, clothing, animals, food, devices, physical items.
  - `Activity / Action`: Hiking, cooking, dancing, skiing, swimming, presenting.
  - `Event / Occasion`: Weddings, birthdays, graduations, road trips, concerts.
  - `Visual Characteristics`: Colors, lighting, angles, aesthetic attributes, compositions.
  - `Text / OCR`: Words inside the photo, signs, receipts, labels, document text.
  - `Context / Relationship`: Situational dynamics, who sent the photo, emotional states.

### Output
- **Remembered Clues Dataset (`remembered_clues.json`):**
  - `record_id`: Reference to the source conversation.
  - `remembered_clues`: Array of extracted objects, each containing:
    - `clue_category`: One of the standardized categories above.
    - `clue_value`: Extracted clue concept.
    - `verbatim_evidence_span`: Exact substring quote from the review where the user articulated remembering this detail.
    - `extraction_confidence`: Confidence metric (0.0 to 1.0).

---

## STEP 4B — WHAT USER DOES NOT REMEMBER WHEN RETREIVING PHOTOS

### Purpose
Identify what specific information the user forgot or could not recall while attempting photo retrieval. Enforce a strict Tri-State Memory Model to ensure research validity and eliminate hallucinated forgetting from omitted text.

### Input
- Verified relevant conversations corpus from **STEP 3** (`relevant_conversations.json`).
- Tri-State classification rules and semantic indicators ("I don't remember", "forgot", "can't recall", "can't remember", "no idea when/where"):
  - `Explicitly Remembered`: The user directly mentions knowing the detail.
  - `Explicitly Forgotten`: The user explicitly states they forgot, cannot recall, or context directly proves lack of recall.
  - `Not Mentioned`: The conversation omits this dimension. **(Strict rule: Never infer forgetting from omission)**.

### Output
- **Memory Gaps & Tri-State Assessment Dataset (`memory_gaps.json`):**
  - `record_id`: Reference to the conversation.
  - `tri_state_memory_profile`:
    - `date_time`: State (`explicitly_remembered` | `explicitly_forgotten` | `not_mentioned`) + evidence quote.
    - `location`: State (`explicitly_remembered` | `explicitly_forgotten` | `not_mentioned`) + evidence quote.
    - `people_names`: State (`explicitly_remembered` | `explicitly_forgotten` | `not_mentioned`) + evidence quote.
    - `event_name`: State (`explicitly_remembered` | `explicitly_forgotten` | `not_mentioned`) + evidence quote.
    - `object_details`: State (`explicitly_remembered` | `explicitly_forgotten` | `not_mentioned`) + evidence quote.
    - `visual_descriptors`: State (`explicitly_remembered` | `explicitly_forgotten` | `not_mentioned`) + evidence quote.
    - `text_ocr`: State (`explicitly_remembered` | `explicitly_forgotten` | `not_mentioned`) + evidence quote.
    - `other`: State + detail + evidence quote.
  - `forgotten_clues_summary`: Array of all explicitly forgotten items with exact text spans.

---

## STEP 5 — MULTIPLE SEARCH ATTEMPTS FOR A PHOTO

### Purpose
Capture and reconstruct the chronological sequence of search attempts described by users who performed multiple sequential queries or strategy shifts when attempting to retrieve a photo. Evaluate search reformulation patterns, tactic changes, and the final search outcome.

### Input
- Verified relevant conversations corpus from **STEP 3** combined with extracted memory clues from **STEP 4A** and **STEP 4B**.
- Multi-attempt extraction schema and query sequence parser.

### Output
- **Multi-Attempt Journey Dataset (`multi_search_journeys.json`):**
  - `record_id`: Conversation reference.
  - `has_multiple_attempts`: Boolean flag (`true` / `false`).
  - `total_reported_queries`: Integer count of queries reported in the conversation.
  - `query_sequence`: Ordered array of search actions:
    - `step_number`: 1, 2, 3...
    - `query_text`: Actual query stated, or `"unknown"` if exact text was not reported (never invented).
    - `query_type`: e.g., `keyword`, `person_filter`, `date_filter`, `location_tag`, `natural_language_semantic`, `visual_clue`.
    - `tactic_change`: Modification type compared to previous query (`generalization`, `specialization`, `modality_switch_to_browsing`, `added_person_tag`, `dropped_date_constraint`, `synonym_replacement`).
  - `strategy_evolved`: Description of whether and how the user's mental model or strategy adapted.
  - `journey_final_outcome`: Final resolution (`success`, `partial_success`, `failure`, `unknown`).
  - `abandonment_point`: Where the user stopped trying (if search was abandoned).

---

## STEP 6 — PHOTO SEARCH RETRIEVAL OUTCOME

### Purpose
Classify the ultimate retrieval resolution of the user's search session into four mutually exclusive categories based on unambiguous text evidence, ensuring that returning results is never falsely equated with finding the desired photo.

### Input
- Verified relevant conversations corpus from **STEP 3** and contextual extractions from **STEP 4A, 4B, and 5**.
- Outcome classification definitions:
  - **Success:** User explicitly retrieved/found the intended target photo.
  - **Partial Success:** User found related photos (same event/person) but not the specific intended target photo.
  - **Failure:** User was unable to find the intended photo despite searching.
  - **Unknown:** Text does not provide sufficient information to determine the final retrieval outcome.

### Output
- **Retrieval Outcomes Dataset (`retrieval_outcomes.json`):**
  - `record_id`: Conversation reference.
  - `outcome`: Categorical enum (`Success`, `Partial Success`, `Failure`, `Unknown`).
  - `verbatim_outcome_evidence`: Exact excerpt indicating the retrieval outcome.
  - `outcome_confidence`: Confidence score (0.0 to 1.0).

---

## STEP 7 — IDENTIFY WHERE THE RETRIEVAL JOURNEY APPEARS TO FAIL

### Purpose
Pinpoint the specific structural breakdown point in the user's end-to-end photo retrieval journey across four defined failure stages, or categorize the conversation as non-indicative if a specific breakdown point cannot be determined.

### Input
- Verified relevant conversations corpus with extracted clues, attempts, and outcomes (**STEP 3–6**).
- Taxonomy of the Four Retrieval Failure Stages:
  1. **Stage 1 — Translation Struggle:** The user struggles to translate their internal visual/episodic memory into a useful textual search query or filter.
  2. **Stage 2 — System Recall/Precision Failure:** The user provides a query/clues, but Google Photos fails to retrieve sufficiently relevant results (returns zero results, missing target photo, or completely irrelevant images).
  3. **Stage 3 — Result Overload / Distinction Difficulty:** Potentially relevant results are returned, but the user struggles to identify the intended photo among excessive, visually similar, or poorly contextualized candidates.
  4. **Stage 4 — Refinement Breakdown & Search Abandonment:** The initial search fails and the user struggles to determine what query or refinement to try next, leading to circular searching or abandonment.
  - *Fallback Stage:* **Conversation not indicative of retrieval journey** (used when conversation lacks sufficient journey granularity).

### Output
- **Journey Breakdown Stages Dataset (`failure_stages.json`):**
  - `record_id`: Conversation reference.
  - `primary_failure_stage`: Enum (`stage_1_translation`, `stage_2_system_retrieval`, `stage_3_distinction_overload`, `stage_4_refinement_abandonment`, `not_indicative`).
  - `breakdown_reasoning`: Qualitative synthesis of why the breakdown occurred at this stage.
  - `verbatim_breakdown_evidence`: Verbatim quote from the review documenting the breakdown.

---

## STEP 8 — CLUSTER SIMILAR PROBLEMS

### Purpose
Group verified relevant conversations into emergent, coherent problem clusters based on shared retrieval breakdowns, memory gap patterns, and search behaviors without imposing artificial fixed cluster quotas or force-fitting unaligned records.

### Input
- Aggregated dataset combining all outputs from **STEP 3, 4A, 4B, 5, 6, and 7** across all verified relevant conversations.
- Semantic clustering models, embedding representations of retrieval experiences, and qualitative cluster synthesis algorithms.

### Output
- **Problem Clusters Dataset (`problem_clusters.json`):**
  - Array of emergent cluster objects, each containing:
    - `cluster_id`: Unique slug identifier (e.g., `missing_temporal_event_retrieval`, `visual_color_object_search_breakdown`).
    - `cluster_name`: Descriptive, clear PM-oriented name.
    - `cluster_description`: Comprehensive summary of the shared problem context.
    - `conversation_count`: Total number of conversations belonging to this cluster.
    - `cluster_percentage`: Percentage of total verified relevant conversations.
    - `common_memory_clues`: List of frequently remembered clue types in this cluster.
    - `common_missing_clues`: List of explicitly forgotten or unavailable clue types.
    - `dominant_failure_stages`: Primary failure stages associated with this cluster.
    - `common_search_behaviors`: Typical query tactics, keyword types, and browsing shifts.
    - `old_photos_characteristics`: Specific types of old visual assets users struggle with in this cluster (e.g., untagged scanned vacation photos, screenshots of recipes, old family gatherings).
    - `representative_evidence_quotes`: Array of 2–4 verbatim user quotes illustrating the breakdown.
    - `member_record_ids`: Complete list of conversation record IDs for full traceability.
- **Unclustered / Noise Corpus (`unclustered_records.json`):** Isolated genuine records that do not fit into coherent emergent clusters, preserving data integrity without force-fitting.

---

## STEP 9 — QUANTIFICATION

### Purpose
Compute rigorous, transparent quantitative metrics, frequency distributions, and breakdown percentages across all analyzed dimensions with explicitly defined numerators, denominators, and eligibility criteria.

### Input
- All structured outputs from **STEP 1 through STEP 8**.
- Statistical calculation engine and aggregation rules.

### Output
- **Quantification Metrics Store (`quantification_metrics.json`):**
  - **Dataset Metrics:**
    - Total sources scanned, total raw conversations ingested, total relevant conversations, total irrelevant conversations, total verified genuine records.
  - **Search Retrieval Outcome Metrics:**
    - Exact counts and percentages for `Success`, `Partial Success`, `Failure`, and `Unknown` (Denominator: Total verified relevant conversations).
  - **Failure Stage Distribution:**
    - Exact percentages and counts for Stage 1 (Translation Struggle), Stage 2 (System Retrieval Failure), Stage 3 (Result Overload/Distinction), Stage 4 (Refinement Failure/Abandonment), and Non-Indicative.
  - **Remembered Clues Frequency Distribution:**
    - Percentage and occurrence count for each clue type (Time, Location, People, Objects, Activity, Event, Visual Characteristics, Text/OCR, Context/Relationships).
  - **Forgotten Clues Frequency Distribution (Tri-State):**
    - Frequency of `Explicitly Forgotten` status across Date/Time, Location, People/Names, Event Names, Objects, and Visual Details.
  - **Problem Cluster Distribution:**
    - Size, volume, and percentage share for each emergent problem cluster.
  - **Multi-Attempt Dynamics:**
    - Percentage of relevant conversations involving multiple search attempts, average sequence length, and abandonment rates.

---

## STEP 10 — OPPORTUNITY IDENTIFICATION

### Purpose
Synthesize the qualitative patterns, problem clusters, and quantitative breakdowns into high-potential, evidence-backed product opportunity hypotheses for Google Photos Product Managers. Formulate structured opportunity areas without prescribing premature feature solutions.

### Input
- Problem clusters from **STEP 8**, quantitative distributions from **STEP 9**, and supporting evidence spans from **STEP 4–7**.
- PM Opportunity framing criteria and strategic objective alignment.

### Output
- **Product Opportunity Hypotheses Dataset (`opportunity_hypotheses.json`):**
  - Structured Opportunity Cards containing:
    - `opportunity_id`: Unique identifier.
    - `problem_title`: Clear articulation of the observed user retrieval problem.
    - `problem_description`: Detailed analysis of how and why users fail in this situation.
    - `evidence`: Curated set of verbatim user quotes demonstrating the issue.
    - `affected_segment`: User archetypes and retrieval scenarios affected (e.g., long-term Google Photos users with 10k+ unorganized media, users searching for non-cataloged historical family events).
    - `frequency`: Occurrence count and percentage in analyzed dataset.
    - `affected_retrieval_stage`: Specific retrieval journey stage (Stage 1, 2, 3, or 4).
    - `why_successful_retrieval_matters`: Strategic user and business impact (e.g., prevents emotional search abandonment, increases photo engagement, builds trust in visual memory assistance).
    - `open_research_questions`: Specific qualitative questions to be tested in subsequent user interviews and concept evaluations.
    - *Anti-Prescription Compliance:* Verified free from premature solution/feature mandates ("Build Feature X").

---

# Downstream Consumption & Final Output Dashboard Mapping

The outputs of the 11 pipeline steps directly populate the four primary dashboard views built with the Fluent 2 Design System:

| Dashboard View | Primary Upstream Data Steps | Displayed Components & Metrics |
| :--- | :--- | :--- |
| **1. Overview** | **STEP 1, 2, 3, 6, 7, 8, 9** | Top-level KPI cards (Total Scanned, Ingested, Relevant/Irrelevant), Outcome donut/bar charts (Success, Partial Success, Failure, Unknown), Retrieval Breakdown funnel (Stages 1–4), Top Problem Clusters summary, and an AI-synthesized, evidence-backed Key Takeaway banner. |
| **2. Retrieval Problems (User Cluster Analysis)** | **STEP 8, 4A, 4B, 5, 7, 9** | Interactive Problem Cluster Cards showcasing: Cluster Name, Frequency (n, %), What Users Remember (Clue types), What is Missing (Tri-State breakdown), Failure Stage, Search Behaviour patterns, Old Photo Retrieval characteristics, and clickable "View Supporting Conversations" modal showing verbatim evidence spans. |
| **3. Key Analytical Questions** | **STEP 4A, 4B, 5, 6, 7, 8, 9, 10** | Clear, data-backed qualitative and quantitative answers to the 10 core PM questions (e.g., struggle photo types, remembered vs forgotten clues, search formulation tactics, journey failure points, reformulation behavior, abandonment triggers, and definition of successful retrieval). |
| **4. Opportunities** | **STEP 10, 8, 9** | Structured Opportunity Hypotheses Cards articulating: Problem, Evidence Quotes, Affected Segment, Frequency, Affected Retrieval Stage, Why Retrieval Matters, and Open User Research Questions for subsequent PM phases. |

---

# Data Integrity, Traceability & Storage Architecture

```
/data/
├── 01_raw/                   # Step 1: Raw scraped data with provenance
│   ├── raw_conversations.json
│   └── ingestion-exceptions.md
├── 02_normalized/            # Step 2: Cleaned, deduplicated canonical records
│   └── normalized_conversations.json
├── 03_filtered/              # Step 3: Classified relevance sets
│   ├── relevant_conversations.json
│   └── irrelevant_conversations.json
├── 04_extraction/            # Steps 4A, 4B, 5, 6, 7: Deep qualitative extractions
│   ├── remembered_clues.json
│   ├── memory_gaps.json
│   ├── multi_search_journeys.json
│   ├── retrieval_outcomes.json
│   └── failure_stages.json
├── 05_clustering/            # Step 8: Problem clusters and evidence sets
│   ├── problem_clusters.json
│   └── unclustered_records.json
├── 06_quantification/        # Step 9: Transparent metrics & distributions
│   └── quantification_metrics.json
└── 07_opportunities/         # Step 10: PM Opportunity hypotheses
    └── opportunity_hypotheses.json
```

### Architectural Guardrails:
1. **Zero Synthetic Records:** No generated or hallucinated reviews enter any stage of the pipeline.
2. **Immutable Provenance:** Every clue, failure stage, and cluster retains its originating `record_id`, `source_url`, and verbatim text span.
3. **Tri-State Memory Enforcement:** `Explicitly Remembered`, `Explicitly Forgotten`, and `Not Mentioned` are strictly maintained.
4. **Transparent Denominators:** All calculations clearly display numerator, denominator, and unknown counts.
5. **Inspectability:** Every intermediate file is human-readable JSON/Markdown, enabling complete end-to-end auditing.
