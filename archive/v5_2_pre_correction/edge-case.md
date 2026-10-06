# Edge Cases & Corner Scenarios: Google Photos Discovery Engine

This document catalogs all potential corner scenarios, data anomalies, LLM failure modes, rate-limit edge cases, and research integrity challenges across the 5 project phases, along with their explicit mitigation strategies.

---

## 1. Data Ingestion & Multi-Source Scraping (Step 1)

| Edge Case / Scenario | Impact | System Handling & Mitigation Strategy |
| :--- | :--- | :--- |
| **1.1. Scraper Block / HTTP 403 / 429 / CAPTCHA** | Scraping endpoint (e.g., Google Play, Reddit, Help Community) blocks requests or hits anti-bot protection. | • Catch exception immediately.<br/>• Log the exact source, timestamp, and failure reason in [ingestion-exceptions.md](file:///c:/Users/prakh/OneDrive/Desktop/new_life/pm_projects/V5/ingestion-exceptions.md).<br/>• Switch to substitute public export/RSS/API endpoint.<br/>• **Never** manufacture synthetic data to fill the gap. |
| **1.2. Multilingual Code-Switching & Non-English Text** | Review mixes English with another language (e.g., Hinglish, Spanglish) or is purely non-English. | • Run fast language detection (`langdetect` / `fasttext`).<br/>• If predominantly non-English, exclude and record in cleaning log.<br/>• If English with minor foreign terms, retain original text without translation to preserve nuance. |
| **1.3. Extremely Short Reviews (< 4 words)** | e.g., *"Search sucks"*, *"Can't find photos"*, *"Broken update"*. | • Preserve record in ingestion, but flag low qualitative richness.<br/>• Classified as relevant in Step 3 if retrieval-focused, but categorized as `not_indicative` in Step 7 (Failure Stages) due to lack of journey detail. |
| **1.4. Extremely Long Community Threads (> 3,000 words)** | Community forum threads with multi-user replies exceeding LLM context window or token limits. | • Split by conversational turns / distinct user posts.<br/>• Isolate the original poster (OP) problem statement and relevant reply sub-threads.<br/>• Truncate peripheral signature/footer noise before sending to LLM. |
| **1.5. Product Confusion (Apple Photos vs Google Photos)** | User complains about Google Photos on iOS but references Apple iCloud Photos / iOS Photos app features. | • LLM relevance prompt specifically verifies that the retrieval struggle occurred within the Google Photos client/web interface. |
| **1.6. Deleted / Anonymized Authors & Missing Dates** | Source lacks exact ISO timestamp or author handle. | • Generate deterministic hash ID based on `source` + `source_url` + text prefix.<br/>• Mark `date` as `null` or approximate from parent thread; never fabricate fake timestamps or author names. |

---

## 2. Cleaning, Normalization & Deduplication (Step 2)

| Edge Case / Scenario | Impact | System Handling & Mitigation Strategy |
| :--- | :--- | :--- |
| **2.1. Copy-Paste Bot Spam & Promotional Links** | Repeated identical spam promoting third-party recovery software or affiliate links. | • Regex and URL heuristic filters identify common spam patterns.<br/>• Flag `spam_score > 0.8` and quarantine into excluded dataset. |
| **2.2. Cross-Platform Duplicate Posts** | Same user posts the identical complaint on Reddit and the Google Help Community. | • Compute SHA-256 hash on normalized text (lowercased, whitespace-stripped).<br/>• Retain the first verified occurrence; link the second as a duplicate reference without double-counting in metrics. |
| **2.3. Malformed HTML / Unicode Artifacts** | Unescaped HTML entities (`&amp;`, `&quot;`, `&#39;`), zero-width spaces, or broken emoji encoding. | • Normalize text via `html.unescape()` and clean invalid Unicode characters while preserving user-inserted emojis and raw text punctuation. |

---

## 3. Relevance Classification & Boundary Ambiguities (Step 3)

| Edge Case / Scenario | Impact | System Handling & Mitigation Strategy |
| :--- | :--- | :--- |
| **3.1. Dual-Topic Feedback (Storage + Search Failure)** | e.g., *"Google charged me for 100GB storage and I still can't find my old vacation pictures when I search for them."* | • **Rule:** If retrieval/search failure is a constituent part of the complaint, classify as `is_retrieval_relevant: true`.<br/>• Tag `relevance_category: multi_topic_retrieval_issue`. |
| **3.2. Sync/Backup Bug vs. Search Indexing Breakdown** | e.g., *"All my photos from 2020 disappeared after the update."* | • Distinguish between media deletion/sync loss vs search failure.<br/>• If the user explicitly notes photos exist in cloud/library but search queries return nothing, mark `relevant`.<br/>• If photos were permanently deleted or failed to upload from device, classify as `irrelevant` (backup/sync). |
| **3.3. Feature Requests for Metadata Tagging** | e.g., *"Why can't I manually tag people's names so I can find them later?"* | • Classify as `relevant` under retrieval preparation / tagging breakdown because the root motivation is retrieval enabling. |

---

## 4. Qualitative Cognitive Clue Extraction (Step 4A & 4B)

| Edge Case / Scenario | Impact | System Handling & Mitigation Strategy |
| :--- | :--- | :--- |
| **4.1. Verbatim Grounding Hallucination** | LLM extracts a memory clue but invents or paraphrases the quote instead of providing the exact substring. | • Automated verification script checks `verbatim_evidence_span in original_text`.<br/>• If exact match fails, script performs fuzzy alignment or falls back to substring slicing from the original text. |
| **4.2. Relative / Fuzzy Temporal Clues** | e.g., *"When my daughter was a toddler"*, *"Before Covid"*, *"A few summers ago"*. | • Categorize as `Time / Temporal` clue category.<br/>• Store exact phrase as `clue_value` without forcing conversion to a specific calendar year. |
| **4.3. Omission vs. Explicit Forgetting (Tri-State Model)** | Review says: *"I searched for my blue jacket but got nothing."* (Did user forget the date, or just not mention it?). | • **CRITICAL RESEARCH INTEGRITY RULE:** Never infer forgetting from omission.<br/>• Date/Time, Location, etc., must be classified as `not_mentioned`.<br/>• Only mark `explicitly_forgotten` if user explicitly uses indicator phrases (*"forgot"*, *"don't remember the date"*, *"can't recall where"*). |
| **4.4. Partial / Probabilistic Recall** | e.g., *"I think it was either 2018 or 2019 in Greece or Italy."* | • Extract both candidate values as fuzzy remembered clues.<br/>• Mark memory state as `explicitly_remembered` (fuzzy/probabilistic recall) with exact verbatim span. |
| **4.5. Negative Clues (What the photo was NOT)** | e.g., *"I searched for my dog, knowing it wasn't the park photo."* | • Extract as `Context / Negation` clue; capture verbatim boundary. |

---

## 5. Multi-Search Attempt Sequences & Query Parsing (Step 5)

| Edge Case / Scenario | Impact | System Handling & Mitigation Strategy |
| :--- | :--- | :--- |
| **5.1. Vague Multi-Attempt Descriptions** | e.g., *"I tried searching 5 different ways and nothing worked."* | • Record `has_multiple_attempts: true`, `total_reported_queries: 5`.<br/>• Set `query_text: "unknown"` for unspecified queries. **Never invent hypothetical queries.** |
| **5.2. Modality Switch to Manual Browsing** | e.g., *"Search returned zero results, so I spent 2 hours scrolling down the infinite timeline."* | • Capture modality shift in sequence: Step 1 = Keyword search, Step 2 = Manual timeline scrolling.<br/>• Tag tactic change as `modality_switch_to_browsing`. |
| **5.3. Interrupted / Non-Linear Sessions** | User searched yesterday, gave up, and tried asking a friend for the date today. | • Extract sequence of user-initiated cognitive strategies; tag temporal discontinuity if reported. |

---

## 6. Outcome Classification & Retrieval Resolution (Step 6)

| Edge Case / Scenario | Impact | System Handling & Mitigation Strategy |
| :--- | :--- | :--- |
| **6.1. Results Returned but Wrong Photos** | Search returns 200 pictures, but none are the intended photo. | • **Rule:** Returning results is NOT success.<br/>• Classify outcome strictly as `Failure` (or `Partial Success` only if closely related context was found). |
| **6.2. Third-Party Workaround Resolution** | e.g., *"Couldn't find it in Google Photos search, so I found it on Instagram / WhatsApp."* | • In the context of Google Photos retrieval engine, classify as `Failure` (Google Photos search failed; user relied on an external workaround). |
| **6.3. Ambiguous / In-Progress Inquiry** | e.g., *"How do I find receipt screenshots from last month?"* (No outcome stated). | • Classify outcome as `Unknown`. Never assume success or failure. |

---

## 7. Retrieval Journey Failure Stage Attribution (Step 7)

| Edge Case / Scenario | Impact | System Handling & Mitigation Strategy |
| :--- | :--- | :--- |
| **7.1. Multi-Stage Compounding Breakdowns** | User struggled to translate memory (Stage 1), then got irrelevant results (Stage 2), and finally abandoned search (Stage 4). | • Classify the **primary origin stage** (e.g., Stage 1: Translation Struggle as the root failure).<br/>• Record secondary compounding stages in `breakdown_reasoning` notes. |
| **7.2. High Frustration, Zero Journey Details** | e.g., *"Google Photos search is completely useless."* | • Classify as `not_indicative` (Conversation not indicative of specific retrieval journey stage).<br/>• Exclude from failure stage funnel percentage calculations to prevent skewed data. |

---

## 8. Problem Clustering & Synthesis (Step 8)

| Edge Case / Scenario | Impact | System Handling & Mitigation Strategy |
| :--- | :--- | :--- |
| **8.1. Outlier / Unique Retrieval Problems** | A single review describes a highly specific issue that shares no pattern with others (e.g., searching for a rare camera lens distortion). | • **Do NOT force-fit** into an existing cluster.<br/>• Route record to `unclustered_records.json`.<br/>• Allow true problem clusters to emerge organically without forced 100% assignment. |
| **8.2. Micro-Cluster Explosion (< 3 reviews per cluster)** | Clustering algorithm creates 30 tiny clusters. | • Set minimum cluster threshold (e.g., minimum 3–5 representative records).<br/>• Merge sub-themes into broader thematic archetypes (e.g., merging "Receipt text search" and "Document screenshot search" into "Text & Document Visual Retrieval"). |

---

## 9. Metric Quantification & Denominator Integrity (Step 9)

| Edge Case / Scenario | Impact | System Handling & Mitigation Strategy |
| :--- | :--- | :--- |
| **9.1. Ambiguous Percentage Denominators** | Clue frequency could be calculated out of Total Conversations OR Total Clues. | • **Explicit Denominator Rule:** Every metric object must declare: `metric_name`, `numerator`, `denominator`, `denominator_definition`, and `percentage`.<br/>• Example: Remembered Time Clue % = (Conversations mentioning Time / Total Verified Relevant Conversations) * 100. |
| **9.2. Division by Zero Protection** | Small filter subset or 0 relevant records in a test slice. | • Guard all calculations: `percentage = (numerator / denominator * 100) if denominator > 0 else 0.0`. |

---

## 10. Opportunity Formulation & Anti-Prescription (Step 10)

| Edge Case / Scenario | Impact | System Handling & Mitigation Strategy |
| :--- | :--- | :--- |
| **10.1. LLM Solution Creep ("Build Feature X")** | LLM attempts to prescribe engineering solutions (e.g., *"Google should implement a voice filter button"*). | • Automated prompt guardrails and post-generation validator reject feature prescriptions.<br/>• Re-formats output to focus strictly on: *Observed Problem → Affected Segment → Retrieval Impact → User Research Question*. |
| **10.2. Subjective Opportunity Ranking** | LLM labels opportunities as "Best" or "Highest Priority". | • Strip subjective ranking tags; present all validated opportunity spaces objectively. |

---

## 11. Groq Free-Tier API Rate Limits & Infrastructure

| Edge Case / Scenario | Impact | System Handling & Mitigation Strategy |
| :--- | :--- | :--- |
| **11.1. HTTP 429 (Rate Limit Exceeded)** | Request burst hits Groq RPM or TPM limit. | • Exponential backoff with jitter (initial wait 2s, then 4s, 8s, 16s... up to 5 retries).<br/>• Paced request queue with mandatory sleep delay (e.g., 2.5s between calls). |
| **11.2. Daily Token / Request Exhaustion** | Daily free-tier limit reached during pipeline execution. | • Pipeline saves progress atomically to disk after every processed record.<br/>• When resumed tomorrow, the local disk cache (`.llm_cache.sqlite`) skips all completed records with 0 token spend. |
| **11.3. Malformed JSON / Schema Validation Error from LLM** | Groq LLM returns invalid JSON or missing mandatory keys. | • Retry with JSON schema correction prompt (up to 2 retries).<br/>• If still malformed, quarantine raw record for manual review without crashing the pipeline. |
| **11.4. Network Socket Hangup / Timeout** | Transient connection drop during streaming/completion. | • Catch `requests.exceptions.Timeout` / `groq.APIConnectionError`.<br/>• Retry with exponential backoff. |

---

## Summary of Architectural Guardrails

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 EDGE CASE GUARDRAIL MATRIX                                       │
├───────────────────────────┬──────────────────────────────────────────────────────────────────────┤
│ Zero Synthetic Records    │ Reject any non-verifiable, fabricated, or simulated feedback.        │
├───────────────────────────┼──────────────────────────────────────────────────────────────────────┤
│ Anti-Force-Fitting        │ Route non-conforming items to 'not_indicative' / unclustered noise.   │
├───────────────────────────┼──────────────────────────────────────────────────────────────────────┤
│ Strict Tri-State Memory   │ Explicitly Remembered | Explicitly Forgotten | Not Mentioned.        │
├───────────────────────────┼──────────────────────────────────────────────────────────────────────┤
│ Verbatim Evidence Match   │ Mandatory substring verification against original authentic text.    │
├───────────────────────────┼──────────────────────────────────────────────────────────────────────┤
│ Groq Token Preservation   │ 1-pass extraction, local pre-screening, SQLite caching, RPM pacing.  │
├───────────────────────────┼──────────────────────────────────────────────────────────────────────┤
│ Explicit Denominators     │ All statistical percentages declare numerator & denominator bounds.  │
└───────────────────────────┴──────────────────────────────────────────────────────────────────────┘
```
