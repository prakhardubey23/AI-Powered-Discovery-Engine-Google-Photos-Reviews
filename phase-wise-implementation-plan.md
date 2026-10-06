# Phase-Wise Implementation Plan: Google Photos Discovery Engine

This implementation plan operationalizes the requirements from [problemstatement.md](file:///c:/Users/prakh/OneDrive/Desktop/new_life/pm_projects/V5/problemstatement.md) and technical architecture from [architecture.md](file:///c:/Users/prakh/OneDrive/Desktop/new_life/pm_projects/V5/architecture.md) into concrete, sequential execution phases.

---

## Core Research Integrity & Groq Free-Tier Optimization Strategy

### 1. Research Authenticity & Anti-Force-Fitting Directives
* **Zero Synthetic or Fabricated Data:** Never manufacture, paraphrase, or hallucinate user feedback, usernames, review IDs, dates, URLs, or quotes to satisfy quotas. All insights must derive strictly from authentic public reviews.
* **Strict Anti-Force-Fitting Rule:** In Phase 2 (Extraction) and Phase 3 (Clustering & Opportunities), never alter the context, meaning, or wording of a review to make it fit a preconceived failure stage, clue category, or cluster.
* **Permit Noise & Unclustered Records:** If a genuine retrieval conversation does not clearly fit standard stages or emergent clusters, label it honestly as `not_indicative`, `unknown`, or route it to `unclustered_records.json`. Let true patterns emerge organically.

### 2. Groq Free-Tier API Rate & Token Optimization Strategy
To strictly adhere to Groq free-tier limits (daily request/token caps and RPM/TPM ceilings), the pipeline incorporates a high-efficiency execution architecture:

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              GROQ FREE-TIER OPTIMIZATION ARCHITECTURE                                  │
├────────────────────────────────┬───────────────────────────────────────────────────────────────────────┤
│ 1. Consolidated Extraction     │ Combines Steps 4A, 4B, 5, 6, & 7 into a SINGLE multi-task JSON prompt │
│    (Single-Pass Call)          │ per review. Reduces API calls by 80% (from 5 calls/review to 1 call).  │
├────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ 2. Pre-LLM Heuristic Screening │ Step 3 uses fast local lexical filters to eliminate obvious off-topic │
│    (Token Saver)               │ reviews (storage/billing/login) before calling LLM on candidates.     │
├────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ 3. Persistent Disk Caching     │ All LLM responses are cached locally (SQLite / JSON cache by record   │
│    (Zero Redundant Calls)      │ hash). Re-running code uses 0 new API tokens/requests.                │
├────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ 4. Rate Throttling & Backoff   │ Built-in rate limiter (sleep pacing between calls, e.g., 25 RPM) with │
│    (429 Protection)            │ exponential backoff and daily token budget tracking.                  │
├────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ 5. Hierarchical Synthesis      │ Step 8 & 10 cluster locally via embeddings/signatures and make only   │
│    (Minimal Global Calls)      │ ~5–10 total LLM calls for entire dataset synthesis and opportunities. │
└────────────────────────────────┴───────────────────────────────────────────────────────────────────────┘
```

---

## Roadmap Overview

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   PHASE-WISE PIPELINE WORKFLOW                                         │
├─────────────────────────┬──────────────────────────────────────────────────────────────────────────────┤
│ Phase 1: Ingestion &    │ Ingest authentic 2-year public feedback (7 sources), clean, deduplicate,     │
│ Data Preparation        │ unify schema, and apply pre-filtered AI relevance classification.           │
├─────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ Phase 2: Deep LLM       │ Single-pass consolidated qualitative extraction: Remembered clues, Tri-State │
│ Qualitative Extraction  │ memory gaps, search attempts, outcomes, and failure stages with verbatim     │
│                         │ evidence spans (Groq-optimized, cached).                                     │
├─────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ Phase 3: Synthesis,     │ Emergent clustering (allowing unclustered noise), metric quantification with │
│ Clustering & Stats      │ explicit denominators, and non-prescriptive PM opportunity hypotheses.       │
├─────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ Phase 4: UI Dashboard   │ Build an interactive Fluent 2 web discovery dashboard with 4 core views:     │
│ (Fluent 2 Design)       │ Overview, Problem Clusters, 10 Analytical Qs, & Opportunity Hypotheses.      │
├─────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ Phase 5: Verification & │ Research integrity audits (0% synthetic check, provenance trace verification,│
│ Documentation           │ execution logs in phases-implementation-log.md).                            │
└─────────────────────────┴──────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Data Ingestion & Canonical Preparation (Steps 1 – 3)

### Objective
Ingest authentic 2-year public user conversations across 7 public channels, clean and deduplicate into a unified schema, and filter for genuine photo retrieval discussions while preserving API tokens.

### Tasks & Execution Steps

1. **Step 1: Multi-Channel Public Ingestion (`src/ingestion/`)**
   - Fetch authentic user feedback (last 2 years, English) from:
     - Google Play Store (`com.google.android.apps.photos`).
     - Apple App Store (`id962194608`).
     - Google Photos Help Community topic threads (`support.google.com/photos/community`).
     - Reddit (`r/googlephotos`, `r/google`).
     - YouTube comments on Google Photos Search / Ask Photos videos.
     - Public Forums (Android Central, MacRumors, Google Product Forums).
     - Social discussions (X/Twitter, Quora public posts).
   - Zero synthetic data generation; log any endpoint blocks/rate limits in `ingestion-exceptions.md`.
   - Output: `data/01_raw/raw_conversations.json`.

2. **Step 2: Cleaning & Normalisation (`src/cleaning/`)**
   - Deduplicate identical reviews and cross-posts using SHA-256 hashes.
   - Strip automated bots and promotional spam.
   - Unify into canonical schema (`record_id`, `source`, `source_type`, `source_url`, `source_id`, `date`, `author_identifier`, `original_text`, `cleaned_text`, `rating`, `language`, `collection_timestamp`, `provenance_status`).
   - Output: `data/02_normalized/normalized_conversations.json`.

3. **Step 3: Relevance Classification with Token-Efficient Pre-Filter (`src/classification/`)**
   - **Local Pre-Filter:** Fast lexical exclusion of non-retrieval topics (storage quotas, subscription billing, login/auth, backup/sync errors) without making LLM calls.
   - **LLM Verification on Candidates:** Send candidate reviews to Groq LLM in structured JSON mode to verify genuine photo retrieval intent.
   - Output: `data/03_filtered/relevant_conversations.json` & `data/03_filtered/irrelevant_conversations.json`.

---

## Phase 2: Deep Qualitative LLM Extraction (Steps 4A – 7)

### Objective
Perform rich qualitative cognitive and behavioral extraction on every relevant conversation using the connected Groq LLM client, consolidated into a **single-pass extraction prompt** to minimize API calls while maintaining verbatim evidence spans and Tri-State memory accuracy.

### Tasks & Execution Steps

1. **Single-Pass Consolidated LLM Extraction Engine (`src/extraction/consolidated_extractor.py`)**
   - Execute one unified prompt per relevant conversation that outputs structured JSON containing all Phase 2 dimensions:
     - **Step 4A (Remembered Clues):** Categorized into *Time, Location, People, Objects, Activity, Event, Visuals, Text/OCR, Context* with exact `verbatim_evidence_span`.
     - **Step 4B (Tri-State Memory Model):** Strict classification across 8 dimensions into `explicitly_remembered`, `explicitly_forgotten`, or `not_mentioned` (never infer forgetting from omission).
     - **Step 5 (Search Attempts):** Extracted query sequence (exact text or `"unknown"`, never invented), reformulation tactics, and strategy shifts.
     - **Step 6 (Retrieval Outcome):** `Success`, `Partial Success`, `Failure`, or `Unknown` with textual proof.
     - **Step 7 (Failure Breakdown Stage):** Diagnosis across *1. Translation Struggle*, *2. System Retrieval Failure*, *3. Result Overload/Distinction*, *4. Refinement Breakdown*, or *Not Indicative*.
   - **Groq Free-Tier Rate Management:**
     - Query local disk cache before making any API request.
     - Rate-limit execution with interval throttling (e.g. 20–25 requests/minute).
     - Automatic retry with exponential backoff on HTTP 429.
   - Outputs:
     - `data/04_extraction/remembered_clues.json`
     - `data/04_extraction/memory_gaps.json`
     - `data/04_extraction/multi_search_journeys.json`
     - `data/04_extraction/retrieval_outcomes.json`
     - `data/04_extraction/failure_stages.json`

---

## Phase 3: Synthesis, Emergent Clustering & Quantification (Steps 8 – 10)

### Objective
Cluster shared problem patterns organically without forcing fixed quotas, calculate transparent statistics with explicit denominators, and synthesize evidence-backed product opportunity hypotheses using minimal aggregate LLM calls.

### Tasks & Execution Steps

1. **Step 8: Emergent Problem Clustering (`src/clustering/`)**
   - Group records based on shared qualitative profiles (memory gaps + failure stages + query tactics).
   - Allow unclustered noise records in `unclustered_records.json` to prevent force-fitting.
   - Use a single aggregate LLM call to synthesize cluster titles, descriptions, and representative evidence quotes from member records.
   - Output: `data/05_clustering/problem_clusters.json` & `data/05_clustering/unclustered_records.json`.

2. **Step 9: Metric Quantification & Statistical Aggregation (`src/quantification/`)**
   - Compute exact quantitative distributions locally in Python (0 LLM tokens required):
     - Dataset volumes (scanned, ingested, relevant, irrelevant, genuine).
     - Outcome percentages (Success, Partial Success, Failure, Unknown) with explicit total relevant denominator.
     - Failure stage proportions (Stages 1–4, Non-indicative).
     - Remembered vs. Explicitly Forgotten clue frequencies.
     - Problem cluster distribution percentages.
   - Output: `data/06_quantification/quantification_metrics.json`.

3. **Step 10: Non-Prescriptive Opportunity Hypotheses (`src/opportunities/`)**
   - Synthesize high-impact problem clusters into structured Opportunity Cards via a single batch LLM reasoning call:
     - Problem Statement & Description.
     - Verbatim Supporting Quotes.
     - Affected User Segment & Retrieval Situation.
     - Frequency and Affected Retrieval Stage.
     - Why Successful Retrieval Matters (User & Business Value).
     - Open Qualitative Research Questions for user interviews.
   - Strictly avoid premature solution mandates (No "Build Feature X").
   - Output: `data/07_opportunities/opportunity_hypotheses.json`.

---

## Phase 4: Discovery Engine Dashboard UI (Fluent 2 Design)

### Objective
Build a lightweight, responsive web discovery dashboard using Vanilla CSS / Fluent 2 design principles to present the research findings clearly and interactively.

### Tasks & Execution Steps

1. **UI Architecture & Navigation (`web/`)**
   - Build a clean single-page interface with 4 dedicated navigation views:
     - **View 1: Overview Analytics** (Dataset KPIs, Outcome distributions, 4-stage failure funnel, Top problem clusters, AI Key Takeaway banner).
     - **View 2: Problem Clusters Explorer** (Cluster cards with memory profiles, failure stage tags, search patterns, old photos context, and "View Supporting Conversations" modal showing verbatim quotes).
     - **View 3: Key Analytical Questions** (Evidence-backed answers to the 10 foundational PM questions from [problemstatement.md](file:///c:/Users/prakh/OneDrive/Desktop/new_life/pm_projects/V5/problemstatement.md)).
     - **View 4: Opportunity Hypotheses** (PM Opportunity Cards with research questions for subsequent interview validation).
   - Implement Fluent 2 styling (neutral elevation, accessible contrast, typography hierarchy, responsive cards, zero clutter).

---

## Phase 5: Verification, Research Integrity Audit & Execution Logging

### Objective
Perform end-to-end audits to verify research authenticity, trace quotes to source records, validate calculations, and log all execution details.

### Tasks & Execution Steps

1. **Research Integrity & Traceability Verification:**
   - Verify 0% synthetic records exist in `data/`.
   - Verify all evidence spans match exact substrings of authentic `original_text`.
   - Verify Tri-State compliance (no inferred forgetting from omitted details).
   - Validate mathematical consistency of all numerators and denominators.
2. **Audit Logging:**
   - Record run timestamps, scraped volume per source, API exceptions, and yield metrics in `phases-implementation-log.md`.

---

## Complete Project Directory Layout

```text
pm_projects/V5/
├── problemstatement.md                 # Source of truth requirements
├── architecture.md                     # Technical architecture & pipeline spec
├── phases-implementation-plan.md       # Phase-wise execution plan
├── phases-implementation-log.md        # Run audit log & yields
├── ingestion-exceptions.md             # Ingestion errors & fallback log
├── data/
│   ├── .llm_cache.sqlite               # Local LLM response cache (Token saver)
│   ├── 01_raw/                         # Raw ingested data
│   ├── 02_normalized/                  # Cleaned canonical records
│   ├── 03_filtered/                    # Relevant vs irrelevant sets
│   ├── 04_extraction/                  # Extracted qualitative datasets
│   ├── 05_clustering/                  # Problem clusters & unclustered noise
│   ├── 06_quantification/              # Quantitative metrics & stats
│   └── 07_opportunities/               # PM Opportunity hypotheses
├── src/                                # Pipeline implementation scripts
└── web/                                # Fluent 2 PM discovery dashboard
```
