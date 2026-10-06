# Forensic Integrity and Consistency Audit Report — Project V5.2

**Audit Date:** 2026-09-26 15:47:08 UTC  
**Target Scope:** V5.2 Expanded Ground-Truth Corpus Diagnosis  
**Audit Purpose:** Comprehensive Pre-Correction Forensic Baseline Diagnosis  
**Files Modified During Audit:** **0** (Pre-correction snapshot archived to `archive/v5_2_pre_correction/`)  

---

## Executive Summary of Audit Findings

A comprehensive forensic audit of all data artifacts, pipeline code, dashboard generation logic, and markdown documentation logs was performed.

### Key Audit Conclusions:
1. **Underlying Data Integrity is Solid:**
   - Raw dataset contains **7,358** authentic public records across 6 channels.
   - Exact deduplication (178) and spam filtering (13) produces **7,167** normalized records.
   - Strict retrieval relevance filtering yields **510** verified relevant retrieval records and **6,657** irrelevant records (510 + 6,657 = 7,167).
   - Cluster coverage is complete: **487** clustered across 6 clusters + **23** unclustered noise records = **510** total (100.00%).
   - Total extracted cognitive clue spans across the 510 relevant records = **686** spans (1.35 spans/conv).

2. **Identified Discrepancies & Stale Relics (To Be Corrected in Subsequent Steps):**
   - **Stale String Relic in Metrics:** `quantification_metrics.json` correctly uses denominator 510, but the string field `denominator_definition` has a stale hardcoded suffix `(86 records)` in 28 entries.
   - **Stale Key Takeaways & Percentages:** `quantification_metrics.json`, `build_dashboard_bundle.py`, and `web/index.html` contain stale V5 baseline numbers (69.8%, 55.8%, N=86, 757) rather than recomputed V5.2 values (39.61% Stage 2 failure, 44.90% failure outcome, N=510, 7,358 raw).
   - **Multi-Search Attempt Counting Logic Bug:** In `metric_calculator.py` (Line 214), evaluating `t != 'none'` counted 23 records with `reformulation_tactics: ['unspecified']` as multiple attempts, inflating multi-attempt count to 71 (13.92%) instead of the canonical 48 (9.41%).
   - **Hardcoded V5 Questions in Dashboard Bundle:** `src/web/build_dashboard_bundle.py` contains hardcoded V5 N=86 percentage distributions across all 10 analytical questions.
   - **Missing Breakdown Object on 4 Extraction Records:** In `data/04_extraction/failure_stages.json` and `consolidated_extractions.json`, 4 records have an empty dictionary as `failure_breakdown`.
   - **Markdown Log Inconsistencies:** `phases-implementation-log.md` (Lines 110-225) contains un-updated execution logs from the old N=86 run.

---

## A. Dataset Reconciliation (Recomputed Ground Truth)

All metrics below are derived directly from the JSON files on disk without relying on existing markdown summaries.

| Dataset Metric | Recomputed Canonical Value | Verification Status | Notes / Derivation |
| :--- | :--- | :--- | :--- |
| **Total Raw Ingested Records** | **7,358** | Verified | `data/01_raw/raw_conversations.json` |
| **Duplicates Removed (Cleaning)** | **178** | Verified | Exact normalized SHA-256 hash deduplication |
| **Spam / Malformed Filtered** | **13** | Verified | Spam pattern match / length < 3 chars |
| **Empty Records Filtered** | **0** | Verified | All non-spam records contained text |
| **Total Filtered in Step 2** | **191** | Verified | 178 + 13 + 0 = 191 records removed |
| **Cleaned & Normalised Records** | **7,167** | Verified | `data/02_normalized/normalized_conversations.json` (7,358 - 191 = 7,167) |
| **Verified Relevant Records** | **510** | Verified | `data/03_filtered/relevant_conversations.json` (7.12% relevance rate) |
| **Irrelevant / Excluded Records** | **6,657** | Verified | `data/03_filtered/irrelevant_conversations.json` (92.88%) |
| **Dataset Identity Check** | **510 + 6,657 = 7,167** | **MATCH (100.00%)** | Exact mathematical reconciliation |

### Source Distribution Breakdown

| Source Channel | Raw Count (%) | Normalized Count (%) | Relevant Count (%) | Irrelevant Count (%) |
| :--- | :--- | :--- | :--- | :--- |
| **Apple App Store (`app_store`)** | 5,787 (78.65%) | 5,699 (79.52%) | 300 (58.82%) | 5,399 (81.10%) |
| **Google Play Store (`google_play`)** | 1,553 (21.11%) | 1,450 (20.23%) | 192 (37.65%) | 1,258 (18.90%) |
| **Google Help Community (`google_help_community`)** | 10 (0.14%) | 10 (0.14%) | 10 (1.96%) | 0 (0.00%) |
| **YouTube (`youtube`)** | 4 (0.05%) | 4 (0.06%) | 4 (0.78%) | 0 (0.00%) |
| **Forums (`forums`)** | 2 (0.03%) | 2 (0.03%) | 2 (0.39%) | 0 (0.00%) |
| **Social (`social`)** | 2 (0.03%) | 2 (0.03%) | 2 (0.39%) | 0 (0.00%) |
| **Total** | **7,358 (100%)** | **7,167 (100%)** | **510 (100%)** | **6,657 (100%)** |

### Temporal Date Distribution
- **Date Span:** `2024-09-30T20:00:55+00:00` to `2026-09-26T13:10:56.442069+00:00` (Strictly within 2-year lookback).
- **Raw Year Distribution:** 2026: 7,316 (99.43%), 2025: 34 (0.46%), 2024: 8 (0.11%).
- **Normalized Year Distribution:** 2026: 7,125 (99.41%), 2025: 34 (0.47%), 2024: 8 (0.11%).
- **Relevant Year Distribution:** 2026: 499 (97.84%), 2025: 8 (1.57%), 2024: 3 (0.59%).

### Uniqueness and Duplicate Audit
- **Record IDs:** 100% unique across all files (Raw: 7,358/7,358; Norm: 7,167/7,167; Rel: 510/510; Irrel: 6,657/6,657). Zero ID collision.
- **Source IDs:** 100% unique across all raw and normalized records.
- **Source URLs:** Raw has 1,578 unique URLs across 7,358 reviews (expected because multiple app store reviews share identical application store listing URLs).
- **Original Text:** Raw has 7,209 unique texts (149 duplicate texts). Normalized dataset has 7,167 unique texts (100% deduplicated). Relevant dataset has 510 unique texts (100% unique).
- **Near-Duplicate Texts in Relevant Set:** 4 small groups of near-identical text (e.g. minor whitespace/punctuation differences) identified; all represent genuine distinct review submissions.

---

## B. Stale Version & Hardcoded Number Audit

The entire repository was scanned for stale relics inherited from earlier runs:

| Pattern / Value | Occurrences & Files Found | Classification | Detailed Diagnosis |
| :--- | :--- | :--- | :--- |
| **`N=86` / `86 records`** | `data/06_quantification/quantification_metrics.json` (28x)<br>`src/quantification/metric_calculator.py` (4x)<br>`web/index.html` (L109)<br>`web/data.js` (28x)<br>`phases-implementation-log.md` (16x)<br>`src/run_phase3.py` (L116) | **Stale current-output value** | `quantification_metrics.json` correctly uses denominator 510, but the literal string `denominator_definition` hardcodes `(86 records)`. |
| **`69.8%` / `69.77%`** | `data/06_quantification/quantification_metrics.json` (L244)<br>`src/quantification/metric_calculator.py` (L244)<br>`src/web/build_dashboard_bundle.py` (L86, 89, 101)<br>`web/data.js` (L307, 310, 322)<br>`web/index.html` (L89)<br>`phases-implementation-log.md` (L131, 208)<br>`src/run_phase3.py` (L97) | **Stale current-output value** | 69.8% represents the V5 baseline failure stage rate (60/86). The actual V5.2 failure stage 2 rate is **39.61%** (202/510). |
| **`55.8%` / `55.81%`** | `src/web/build_dashboard_bundle.py` (L236)<br>`web/data.js` (L457)<br>`phases-implementation-log.md` (L130)<br>`src/run_phase3.py` (L96) | **Stale current-output value** | 55.81% is the V5 outcome failure rate (48/86). The canonical V5.2 failure rate is **44.90%** (229/510). |
| **`757`, `688`, `602`** | `web/index.html` (L148)<br>`phases-implementation-log.md` (L171, 205, 207, 208, 221)<br>`src/run_phase4.py` (L56)<br>`src/run_phase5.py` (L43, 45, 46, 59) | **Stale current-output value** | V5 pipeline counts (757 raw, 688 normalized, 602 irrelevant) baked into templates instead of V5.2 counts (7,358 raw, 7,167 normalized, 6,657 irrelevant). |
| **`282 clues`** | `v5 and v5.2 results log.md` (L15)<br>`src/run_phase2.py` (L83)<br>`src/extraction/build_phase2_artifacts.py` (L423) | **Historical / log-only value** | Valid baseline metric in comparative log comparing V5 (282 clues) vs V5.2 (686 clues). |
| **`ISO 8601`** | `architecture.md` (L149, 154) | **Valid current value** | Refers to the ISO date standard, not a corpus count. |

---

## C. Problem Cluster Consistency Audit

Recomputed directly from `data/05_clustering/problem_clusters.json` and `unclustered_records.json`:

| Cluster ID | Cluster Name | Canonical Count | Recomputed % | Quantification JSON % | Discrepancy Found |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `face_grouping_people_identification_breakdown` | Face Grouping & People Identification Failure | 130 | 25.49% | 25.49% | None in counts; stale `(86 records)` string in definition |
| `semantic_ai_natural_language_query_mismatch` | Natural Language & AI Query Semantic Mismatch | 121 | 23.73% | 23.73% | None in counts; stale `(86 records)` string in definition |
| `temporal_chronological_discovery_gap` | Temporal & Date-Based Navigation Breakdown | 119 | 23.33% | 23.33% | None in counts; stale `(86 records)` string in definition |
| `visual_attribute_object_detail_retrieval_friction` | Visual Attributes & Object-Specific Retrieval Friction | 55 | 10.78% | 10.78% | None in counts; stale `(86 records)` string in definition |
| `result_overload_and_refinement_exhaustion` | Result Overload & Refinement Exhaustion | 33 | 6.47% | 6.47% | None in counts; stale `(86 records)` string in definition |
| `text_document_screenshot_ocr_breakdown` | Text, Document & Screenshot OCR Search Breakdown | 29 | 5.69% | 5.69% | None in counts; stale `(86 records)` string in definition |
| **Subtotal Clustered** | **6 Emergent Problem Clusters** | **487** | **95.49%** | **95.49%** | **100% Unique Member IDs (0 duplicate cluster assignments)** |
| `unclustered_records` | Unclustered / Non-Indicative Outliers | 23 | 4.51% | 4.51% | Preserved unclustered to prevent force-fitting |
| **Total Relevant Corpus** | **Clustered (487) + Unclustered (23)** | **510** | **100.00%** | **100.00%** | **Exact Match (487 + 23 = 510)** |

---

## D. Failure-Stage Funnel Consistency Audit

Recomputed directly from `data/04_extraction/failure_stages.json`:

| Failure Stage | Canonical Count | Recomputed % (N=510) | `quantification_metrics.json` Count (%) | Discrepancy & Root Cause |
| :--- | :--- | :--- | :--- | :--- |
| **Not Indicative** | **249** | **48.82%** | 253 (49.61%) | Metric calculator defaulted 4 unmapped/empty breakdown records to Not Indicative (249 + 4 = 253). |
| **2. System Retrieval Failure** | **202** | **39.61%** | 202 (39.61%) | Exact match in counts. (Dashboard narrative used stale 69.8%). |
| **3. Result Overload / Distinction** | **29** | **5.69%** | 29 (5.69%) | Exact match. |
| **4. Refinement Breakdown** | **22** | **4.31%** | 22 (4.31%) | Exact match. |
| **1. Translation Struggle** | **4** | **0.78%** | 4 (0.78%) | Exact match. |
| **Unspecified / Empty Breakdown Object** | **4** | **0.78%** | *(Grouped in Not Indicative)* | 4 records in `failure_stages.json` contain an empty dictionary. |
| **Total** | **510** | **100.00%** | **510 (100.00%)** | Exact total reconciliation. |

---

## E. Retrieval Outcome Consistency Audit

Recomputed directly from `data/04_extraction/retrieval_outcomes.json`:

| Outcome Category | Canonical Count | Recomputed % (N=510) | `quantification_metrics.json` Count (%) | Discrepancy Found |
| :--- | :--- | :--- | :--- | :--- |
| **Failure** | 229 | 44.90% | 229 (44.90%) | None in counts; stale `(86 records)` string in definition |
| **Success** | 209 | 40.98% | 209 (40.98%) | None in counts; stale `(86 records)` string in definition |
| **Unknown** | 42 | 8.24% | 42 (8.24%) | None in counts; stale `(86 records)` string in definition |
| **Partial Success** | 30 | 5.88% | 30 (5.88%) | None in counts; stale `(86 records)` string in definition |
| **Total** | **510** | **100.00%** | **510 (100.00%)** | Exact match. |

---

## F. Memory-Clue Audit (Spans vs Conversations Distinction)

Recomputed directly from `data/04_extraction/remembered_clues.json`:

> [!IMPORTANT]
> A critical distinction is maintained between:
> 1. **Total Extracted Clue Spans:** Total count of individual verbatim clue substrings extracted across all reviews.
> 2. **Conversation Count:** Number of unique conversations containing at least one clue of that dimension.
> 3. **Percentage of Relevant Conversations:** (Conversation Count / 510) * 100.

| Memory Dimension | Total Clue Spans Extracted | Unique Conversations Mentioning Dimension | % of Relevant Conversations (N=510) | Average Spans per Mentioning Conversation |
| :--- | :--- | :--- | :--- | :--- |
| **Time** | 134 spans | 132 convs | **25.88%** | 1.02 |
| **People** | 124 spans | 122 convs | **23.92%** | 1.02 |
| **Objects** | 123 spans | 115 convs | **22.55%** | 1.07 |
| **Activity** | 62 spans | 55 convs | **10.78%** | 1.13 |
| **Location** | 59 spans | 59 convs | **11.57%** | 1.00 |
| **Context** | 58 spans | 55 convs | **10.78%** | 1.05 |
| **Visuals** | 48 spans | 47 convs | **9.22%** | 1.02 |
| **Event** | 47 spans | 47 convs | **9.22%** | 1.00 |
| **Text / OCR** | 31 spans | 29 convs | **5.69%** | 1.07 |
| **Total Corpus Clues** | **686 spans** | **510 conversations** | **1.35 spans / conversation** | - |

---

## G. Multi-Search Journey Audit

Recomputed directly from `data/04_extraction/multi_search_journeys.json`:

| Journey Category | Canonical Count | Recomputed % (N=510) | `quantification_metrics.json` Reported Count | Discrepancy & Root Cause |
| :--- | :--- | :--- | :--- | :--- |
| **Multiple Retrieval Attempts** | **48** | **9.41%** | 71 (13.92%) | **BUG IN METRIC CALCULATOR:** `metric_calculator.py` line 214 tested `t != 'none'`, which incorrectly matched 23 records with `reformulation_tactics: ['unspecified']`, inflating the count to 71. |
| **Single Retrieval Attempt** | **117** | **22.94%** | *(Combined into 439)* | Explicitly described 1 single query attempt without reformulation. |
| **Unspecified Retrieval Attempts** | **345** | **67.65%** | *(Combined into 439)* | Review text states complaint/praise without detailed step-by-step query trace. |
| **Explicit Reformulation Observed** | **38** | **7.45%** | Not broken out separately | User explicitly documented changing keywords, adding filters, switching tabs, etc. |
| **Total** | **510** | **100.00%** | **510 (100.00%)** | Exact total reconciliation. |

---

## H. Files Requiring Correction (Action Plan)

The following files contain identified discrepancies or stale relics that will need systematic updating during the correction phase:

1. **`data/06_quantification/quantification_metrics.json`:**
   - Update 28 stale `denominator_definition` strings from `(86 records)` to `(510 records)`.
   - Update `key_takeaway` string from `(69.8%)` to `(39.61%)`.
   - Correct `multi_search_attempt_dynamics` multiple attempts count from 71 to 48 (and single/unspecified to 462).

2. **`src/quantification/metric_calculator.py`:**
   - Fix line 214 counting bug (`t not in ['none', 'unspecified']`).
   - Fix lines 84, 125, 150, 197 denominator string literals.
   - Fix line 244 key takeaway string.

3. **`src/web/build_dashboard_bundle.py`:**
   - Dynamically compute / update `ANALYTICAL_QUESTIONS` findings from canonical V5.2 data rather than hardcoded N=86 percentages.

4. **`web/data.js`:**
   - Regenerate from corrected `build_dashboard_bundle.py` and `quantification_metrics.json`.

5. **`web/index.html`:**
   - Fix hardcoded text at L89 (69.8%), L109 (N=86), L148 (757 records).

6. **`src/run_phase3.py`, `src/run_phase4.py`, `src/run_phase5.py`:**
   - Synchronize embedded execution summary templates with canonical V5.2 counts.

7. **`phases-implementation-log.md`:**
   - Synchronize Phase 3, 4, 5 summary logs with V5.2 510-record metrics.

8. **`v5 and v5.2 results log.md`:**
   - Synchronize raw channel breakdown table with canonical raw counts (Play Store: 1,553; App Store: 5,787; Help Community: 10; YouTube: 4; Forums: 2; Social: 2).

9. **`data/04_extraction/failure_stages.json` & `consolidated_extractions.json`:**
   - Normalize the 4 records with empty breakdown objects to valid failure stage format.

---

```
FORENSIC AUDIT COMPLETE
FILES MODIFIED: 0
```
