# BUSINESS CONTEXT

We are making a Product Manager fellowship graduation project. 

The project is about Google Photos where users accumulate thousands of photos, videos, screenshots, documents, and other visual memories over years. Users can often find photos when they know exactly what they are looking for.
However, retrieval becomes difficult when the user's memory is incomplete. The user knows that the photo exists—but may not remember when it was taken, where it was taken, what album it belongs to, or the exact words needed to search for it.

The strategic goal for the project is to Increase the percentage of users who successfully retrieve a photo they remember but cannot precisely describe when they start searching.

The Product Manager fellowship graduation project has many parts to it, we are doing Part 1 right now and its task is to understand how people remember old visual information, where the existing photo retrieval experience breaks down, and identify an opportunity that can meaningfully improve successful retrieval.

This file is the source of truth for part 1. Read it fully & carefully before writing code.

---

# OBJECTIVE

Build an AI-powered discovery engine that analyzes publicly available user feedback and conversations about Google Photos retrieval for large number of user feedback and conversation.

The system should go beyond:
* sentiment analysis
* summarizing reviews
* simple keyword frequency
* star-rating analysis

It should enable you to identify and compare different retrieval problems and opportunity areas using evidence from real users.

It should behave like an AI-powered qualitative research analyst but should display the final results in easy to understand manner and language.
The system should analyze large volumes of user conversations and convert them into structured evidence that will be used in later parts of the project - Business metric decomposition, User interviews, Problem definition and AI-native MVP. These parts are not relevant for the scope of this AI discovery engine.
Therefore, design the system so that its outputs are useful for these stages.

Discovery engine should help uncover questions like (sample questions only):
1. What kinds of old photos do users struggle to retrieve?
2. What information do people actually remember about a photo and what information have they forgotten?
3. How do users formulate searches when their memory is incomplete? How they translate their memory into a search?
4. Where the photo retrieval journey breaks down?
5. Do early search failures change what users try next?
6. What users do when their initial search fails?
7. When do users give up?
8. Which photo retrieval problems occur most frequently?
9. Which problems may represent meaningful product opportunities?
10. How should we frame a "successful photo retrieval" for measurement purposes?

---

# PRODUCT SCOPE

The primary product being researched is Google Photos.

Focus the core research on users discussing Google Photos.

Potential sources include:

1. Google Play Store reviews of Google Photos
2. Apple App Store reviews of Google Photos
3. Google Photos Help / Community discussions
4. Reddit discussions
5. YouTube comments
6. Public forums
7. Other publicly available social discussions

---

# IMPORTANT CONSIDERATIONS

Do NOT jump directly from raw reviews to final conclusions.
Each intermediate stage should be inspectable.
Once data is ingested, cleaned and relevant conversations filtered in STEP 3 below, this data must be accessible to all subsequent steps.  

---
# RESEARCH INTEGRITY & PIPELINE SPECIFICATIONS FOR SUBSEQUENT STEPS

> **IMPORTANT RESEARCH INTEGRITY NOTICE:**
> This section talks about prohibiting synthetic fallbacks, establishing honest timeframes, and enforcing strict qualitative evidence standards.

## 1. Core Strategic Objective & Scope Alignment
* **Strategic Business Goal:** Increase the percentage of users who successfully retrieve a photo they remember but cannot precisely describe when they start searching.
* **Purpose:** Act as an AI-powered discovery engine for qualitative research. It is **not** a generic search, sentiment analysis, or complaints dashboard.
* **Downstream PM Utility:** Output structured, verified evidence to inform metric decomposition, user interviews, problem definitions, and MVP development without inventing findings.

## 2. Updated Collection Window & Removal of Volume Quotas
* **Time Window:** Standardized to the **last 3 years** of genuine user feedback (with a configurable lookback of up to 5 years).
* **Elimination of Arbitrary Volume Targets:** Ingestion of reviews for volume targets are strictly removed as mandatory gates. Authentic, rich retrieval accounts take absolute precedence over artificial volume.
* **No Endless Loops or Fake Fallbacks:** Never loop endlessly or manufacture records to hit targets. If a source yields limited authentic retrieval journeys, report the actual yield and limitations honestly in phases-implementation-log.md

## 3. Strict Data Authenticity & Anti-Fabrication Rules
* **Zero Synthetic Data in Research:** Never generate, paraphrase, expand, or duplicate feedback to meet targets. Fabricating author names, review IDs, timestamps, URLs, or quotes is strictly forbidden.
* **Test Isolation Only:** Synthetic fixtures are allowed solely within isolated automated unit testing suites (`tests/fixtures/`) and must never enter the research corpus or dashboard analytics.
* **Provenance & Verification:** Distinguish records into `Verified Genuine`, `Unverified`, and `Quarantined/Synthetic`. Only verified authentic records enter downstream analysis post STEP 3 mentioned below.
* **Honest Source Error Logging:** If an API or scraper encounters rate limits or access blocks, record the actual error in the log. Never claim a source was scraped if it was not.

## 4. Genuine AI Qualitative Extraction & Evidence Grounding
* **Real LLM Extraction:** Core qualitative extraction must actively call the configured LLM client. Keyword regex rules must not masquerade as AI extraction.
* **Evidence Spans:** Every extracted memory clue, search gap, and failure reason must include the exact verbatim text span from the source review.
* **Tri-State Memory Model:**
  - `Explicitly Remembered`: Details the user directly mentions knowing.
  - `Explicitly Forgotten`: Details the user explicitly states they forgot or do not know.
  - `Not Mentioned`: Details omitted from the review. **Never infer forgetting from omission.**
* **No Invented Queries:** Extract only actual reported queries and filters. If exact queries are not stated, mark as `unknown`. Never construct hypothetical search queries.

## 5. Emergent Clustering & Metric Transparency
* **Emergent Clusters:** Do not force a fixed cluster count as mentioned in STEP 8 or force-fit every record. Allow noise and unclustered items. Cluster descriptions must reflect shared retrieval problems derived from member evidence.
* **Explicit Denominators:** Every percentage and metric must clearly state its numerator, denominator, eligibility criteria, and unknown/missing count. No hardcoded constants or arbitrary success thresholds (e.g., "under 20 seconds").
* **Non-Prescriptive Opportunities:** Opportunity cards must articulate observed problem patterns, evidence quotes, affected segments, and open user research questions without prematurely prescribing features.

## 6. Do not alter content of review to forcefit it in downstream analysis
* Even after STEP 3 mentioned below, if a relevant conversation does not fit into any of the steps mentioned below for analysis dont try to forcefit the same. Do not alter the content of the review or add/remove semantic meaning from it to make it fit into the descriptions. 


---
# STEP 1 — DATA INGESTION

Ingest data from the following sources - 

* **Google Play Store**: Package ID / App ID: 'com.google.android.apps.photos'. Pull last 5 years of global reviews. 
* **Apple App Store**: App ID: 'id962194608'. Pull last 5 years of global reviews. 
* **Google Photos Help / Community discussions**: Source: Google Photos Help Community, URL: support.google.com/photos/community. Pull discussions specifically related to:
    - Photo Search / Search
    - Finding or retrieving photos
    - Search relevance / incorrect results
    - People & Face Groups search
    - Places / location search
    - Similar-photo search
    - Missing photos from search results
    - Ask Photos / AI-powered search
    - Search ranking / "best match" vs recent results  
* **Reddit discussions**: Primary subreddit: r/googlephotos, r/google Pull posts and comments which talk about:
    - "Google Photos search"
    - "can't find photos"
    - "search not working"
    - "wrong search results"
    - "search results"
    - "photo retrieval"
    - "find old photos"
    - "search by text"
    - "search by person / face"
    - "search by date / location"
    - "similar photos"
    - "AI Search / Ask Photos"
    - "Gemini search"
    - "search relevance"  
* **YouTube comments**: Source: YouTube videos specifically demonstrating/reviewing Google Photos Search, Ask Photos, Gemini in Google Photos, Google Photos AI search, Google Photo search, and finding/retrieving photos.
  Pull comments from:
    - Google / Google Photos official videos
    - Product-review videos which talk about AI powered search in google photos 
    - Google Photos feature/tutorial videos
    - Videos discussing Ask Photos / AI Search  
* **Public forums**: Search Google Photos-related discussions on:
    - Google Photos Help Community
    - Android Central Forums
    - Android Forums
    - MacRumors Forums
    - Google Product Forums / archived Google Photos discussions  
  Focus only on discussions involving photo search/retrieval, search relevance, missing/wrong results, face search, location/date search, and AI/Ask Photos.  
* **Other publicly available social discussions**: Search public discussions on:
    - X / Twitter
    - Facebook public posts/groups where accessible
    - Threads
    - Quora  
  Use Google Photos-specific keyword combinations for searching such as:
    - "Google Photos search"
    - "Google Photos can't find"
    - "Google Photos search results"
    - "Google Photos AI search"
    - "Ask Photos"
    - "Google Photos face search"
    - "Google Photos missing photos"  
* **Record metadata for each conversation/review**:
    * `source`
    * `source_type`
    * `source_url`
    * `source_id` (if available)
    * `date` (if available)
    * `author identifier`
    * `original_text`
    * `rating` (if applicable)
    * `language`
    * `collection_timestamp`
* **Time window**: Last 2 years of data 

**Requirements:**
* Fetch English reviews/conversations for all sources
* Preserve original text.
* Do not lose source traceability.
* Use only publicly available data and no scraping behind unauthorized login.
* If you are unable to scrape any source due to any reason - mention that source name and reason for not being able to scrape that source. Use a substitute instead and store this information in a separate file called `ingestion-exceptions.md`.
* Do not make synthethic data, use real data only.
---

# STEP 2 — CLEANING & NORMALISATION

* Remove obvious spam
* Remove duplicate content
* Normalize formatting
* Unify to a single schema

---

# STEP 3 — RELEVANCE CLASSIFICATION

Determine via AI if the conversation or review is "relevant" by checking if it is talking about photo retrieval. Also check for the following; they also classify as relevant only:
* Find a specific photo
* Search for an old photo
* Retrieve a photo
* Identify a photo
* Locate a screenshot/document/image
* Search using people, places, objects, events, time, or visual characteristics
* Retrieving a photo that they know exists but cannot find

Exclude and drop unrelated Google Photos problems such as:
* Storage 
* Subscriptions
* Login
* Backup
* Syncing
* Editing
* Sharing  
unless retrieval/search is also part of the problem.
---

# STEP 4A — WHAT DOES THE USER REMEMBER WHEN RETRIEVING PHOTOS?

For every relevant conversation, extract using AI what the user remembers about the desired photo. We get this info by looking at what he searched for. These are called 'clues'.  
Categorize remembered clues into categories like time, location, people, objects, activity, event, visual characteristics, text, context, relationships, etc. Examples mentioned below are just for explaining the concept. Each relevant conversation can have various clues which may not be present as examples below but need to be categorized into categories.

---

# STEP 4B — WHAT USER DOES NOT REMEMBER WHEN RETREIVING PHOTOS 

AI should identify from relevant conversations what the user doesn't remember while retrieving photos. AI/llm should pull from the context of the review/conversation for this analysis. "clues like "I don't remember", "forgot","can't recall", "can't remember" etc. should be taken as indicators for this analysis. AI/llm should also check if it can be inferred from the context of the review/conversation.

This will eventually help answer an important question: "What information do people not remember when trying to retrieve an old photo?"

AI/llm should distinguish what user does not remember when retrieving photo into three categories:
* **Explicitly remembered** - The user directly mentions it.
* **Explicitly forgotten** - The user explicitly says they do not remember it or if it emanates from the context of the review
* **Not mentioned** - The conversation does not provide information.

Do NOT treat "not mentioned" as "forgotten." — This distinction is critical for research validity.
---

# STEP 5 — MULTIPLE SEARCH ATTEMPTS FOR A PHOTO 

When multiple searches are described in relevant conversations, AI/llm should preserve the sequence. If conversation context shows multiple attempts to retrieve photo with different types of clues one after the other, it falls in this category

We should store:
* number of queries in relevant conversation showing multiple search attempts 
* query sequence
* whether user strategy changed to arrive at successful result
* what type of change he did in the query
* final outcome - was user able to successfully retrieve photo or not

---

# STEP 6 — PHOTO SEARCH RETRIEVAL OUTCOME

AI/llm should classify the relevant conversations outcome into one of these categories:

* **Success** - User clearly found the intended photo.
* **Partial success** - User found related photos but not clearly the intended photo.
* **Failure** - User could not find the intended photo.
* **Unknown** - Outcome cannot be determined.

Never assume success simply because results were returned.

---

# STEP 7 — IDENTIFY WHERE THE RETRIEVAL JOURNEY APPEARS TO FAIL

AI/llm should classify where the retrieval journey appears to fail based on the relevant conversations.

Use these four primary stages:

## 1. The user struggles to translate their memory into a useful search.
Examples of this stage will look like:
* "I know what the photo looks like but don't know what to search."
* User remembers context but lacks obvious keywords.

## 2. The user provides a query/clues, but Google Photos fails to retrieve sufficiently relevant results.
Examples of this stage will look like:
* irrelevant results
* relevant photo apparently missing
* semantic/contextual query not understood
* multiple clues not combined effectively

## 3. Potentially relevant results are returned, but the user struggles to identify the intended photo.
Examples of this stage will look like:
* too many results
* many visually similar photos
* correct photo is difficult to distinguish
* result context is insufficient

## 4. The initial search fails and the user struggles to determine what to try next.
Examples of this stage will look like:
* repeated unsuccessful searches
* no idea what query to try next
* no useful refinement path
* user abandons search

Note: Examples are used here to help understand the concept. AI\llm should classify the relevant conversations based on these four stages.

If the conversation is not falling into any of the buckets, AI\llm should classify it as "Conversation not indicative of retrieval journey".

---

# STEP 8 — CLUSTER SIMILAR PROBLEMS
  
AI\llm should cluster relevant conversations which belong to the same type of context in one group

Potential clusters may include:
* Event/context-based retrieval
* Missing temporal information
* Missing location information
* People-based retrieval
* Visual-memory retrieval
* Object-based retrieval
* Text/document retrieval
* Multi-clue retrieval
* Semantic understanding failure
* Result overload
* Similar-photo identification
* Search refinement difficulty
* Search abandonment

These are just examples, NOT predefined final answers.  
Allow new clusters to emerge from the data.  
Avoid creating many tiny clusters.

For each cluster provide:
* cluster name
* cluster description
* number of relevant conversations in the cluster
* percentage of relevant conversations out of the total relevant conversations
* common memory clues present in relevant conversations of the cluster
* common missing clues not present in relevant conversations of the cluster
* common search behaviors of the cluster

Example of clustering:

**Example 1: Event-based retrieval with incomplete temporal information**  
Suppose you have:
* "Can't find old photos from my trip."
* "Search doesn't find pictures from vacation."
* "I remember the holiday but not when it happened."
* "How do I find photos from a trip when I don't remember the date?"

**Example 2: Visual-memory retrieval**  
* "I know the picture was a blue car."
* "I remember the photo had a red dress."
* "I remember what the picture looked like but not where it was taken."

*(Note: These are just examples of how to group relevant conversations into clusters. Use this to understand concept only and AI should cluster all possible relevant conversations based on a logic)*

---

# STEP 9 — QUANTIFICATION

Once all the above steps are completed calculate stats based on all the above steps. Like:

### Dataset
* total sources scanned
* total number of raw conversations ingested
* total number of relevant conversations
* total number of irrelevant conversations

### Search Retrieval outcome
* **Success** - % of relevant conversations where users clearly found the intended photo.
* **Partial Success** - % of relevant conversations where users found related photos but not clearly the intended photo.
* **Failure** - % of relevant conversations where users could not find the intended photo.
* **Unknown** - % of relevant conversations where outcome cannot be determined.

### Failure stage
* What % of user struggles to translate their memory into a useful search.
* What % of relevant conversations where user provides a query/clues, but Google Photos fails to retrieve sufficiently relevant results.
* What % of relevant conversations show potentially relevant results are returned, but the user struggles to identify the intended photo.
* What % of relevant conversations show the initial search fails and the user struggles to determine what to try next.

### Frequency of remembered clue types mentioned in relevant conversations
* time
* location
* people
* objects
* activity
* event
* visual characteristics
* text
* context
* relationships

### Frequency of forgotten clue types mentioned in relevant conversations
* date/time
* location
* people/name
* event name
* object
* other

### Problem clusters emanating from relevant conversations
* frequency and percentage of each major cluster

---

# STEP 10 — OPPORTUNITY IDENTIFICATION

Identify high-potential opportunity spaces from all the analysis done till now for a Google product manager to solve photos retrieval problem which makes business sense for Google. Identify problems which are most impactful and have most number of users affected. AI can use its reasoning capability to identify these opportunity spaces.

For each opportunity provide:
* Problem
* Evidence
* Affected segment
* Frequency
* Affected Retrieval Stage
* Why Successful Retrieval Matters

Do NOT rank opportunities as "best" or "worst."  
Do NOT jump to feature recommendations.

---

# FINAL OUTPUT

### Dashboard Objective
The dashboard should function as a photo retrieval problem discovery tool, not as a generic review analytics dashboard.

The dashboard should have the main sections:
1. Overview
2. User Cluster Analysis 
3. Key Analytical Questions
4. Opportunities

The dashboard should remain visually simple. Technical pipeline details, model information, cleaning statistics, and detailed AI outputs should remain hidden under a methodology or supporting section rather than occupying the main dashboard.

---

### 1. Overview

#### Dataset
* total sources scanned
* total number of raw conversations ingested
* total number of relevant conversations
* total number of irrelevant conversations

#### Search Retrieval outcome
* **Success** - % of relevant conversations where users clearly found the intended photo.
* **Partial Success** - % of relevant conversations where users found related photos but not clearly the intended photo.
* **Failure** - % of relevant conversations where users could not find the intended photo.

#### Failure stage - Where does retrieval break
* What % of user struggles to translate their memory into a useful search.
* What % of relevant conversations where user provides a query/clues, but Google Photos fails to retrieve sufficiently relevant results.
* What % of relevant conversations show potentially relevant results are returned, but the user struggles to identify the intended photo.
* What % of relevant conversations show the initial search fails and the user struggles to determine what to try next.

#### Top Retrieval Problem Clusters
* Show the most frequently occurring problem clusters identified from the data.

#### Key Takeaway
* Then finally one-line key takeaway from the slide (these are examples only, you can generate your own using AI)  
  *Example:* "Users often remember the context of a photo rather than a searchable attribute. Search failures frequently persist because users don't know how to reformulate their query."  
  *Note:* The actual findings must be generated from the collected dataset. Do not fabricate insights.

---

### 2. Retrieval Problems
The purpose is to allow the Product Manager to identify and compare different ways in which photo retrieval fails.

Instead of showing hundreds of individual reviews, take cluster information from STEP 10.

Each **Problem Cluster Card** should contain:
* **Problem Name** - A concise description of the retrieval problem
* **Frequency** - Number of conversations belonging to the cluster.
* **What Users belonging to this cluster remember while searching for a photo** - The types of memory clues users typically have (e.g. Person, Location, Time, Event, Activity, Object, Visual characteristics, Text, Context/relationship).
* **What Is Missing for the cluster** - Clearly distinguish:
  * Explicitly remembered
  * Explicitly forgotten
* **Failure Stage** - Show where the retrieval journey breaks for the cluster:
  * do users of this cluster struggle to translate their memory into a useful search?
  * or do users of this cluster provide query/clues, but Google Photos fails to retrieve sufficiently relevant results?
  * or do potentially relevant results are returned, but the user struggles to identify the intended photo?
  * or does the initial search fail and the user struggles to determine what to try next?
* **Search Behaviour** - Show how users attempted to search for photos in this cluster:
  * Keywords
  * People
  * Places
  * Dates
  * Objects
  * Visual characteristics
  * Query reformulation
  * Alternative strategies such as scrolling or browsing
* **Old Photos Retrieval** - What kinds of old photos do users struggle to retrieve?
* **Representative Evidence** - Show 1–3 representative user quotes or excerpts. Include a link/button: “View Supporting Conversations” (this should open the underlying evidence used to create the cluster).

The main comparison should allow the PM to see:  
**Problem → Frequency → Memory pattern → Failure stage → Search behaviour → Old Photo Retrieval → Evidence**

This is the core of the dashboard.

---

### 3. Key Analytical Questions

The following questions should be answered in this section in a clean, simple to understand and non cluttered way. All data backed from the analysis till now:
1. What kinds of old photos do users struggle to retrieve?
2. What information do people actually remember about a photo and what information have they forgotten?
3. How do users formulate searches when their memory is incomplete? How they translate their memory into a search?
4. Where the photo retrieval journey breaks down?
5. Do early search failures change what users try next?
6. What users do when their initial search fails?
7. When do users give up?
8. Which photo retrieval problems occur most frequently?
9. Which problems may represent meaningful product opportunities?
10. How should we frame a "successful photo retrieval" for measurement purposes?

---

### 4. Opportunities

#### Purpose
This section should convert observed retrieval problems into evidence-backed opportunity hypotheses.  
It should NOT directly recommend features.

The dashboard should help the PM move from:  
**Evidence → Pattern → Interpretation → Problem Hypothesis → Research Question**

Each **Opportunity Card** should contain:
* **Problem** - What user problem has been observed?
* **Evidence** - What real user conversations support it?
* **Affected Segment** - Which type of user/retrieval situation appears affected?
* **Frequency** - How frequently does the problem occur in the analyzed dataset?
* **Retrieval Stage** - Where does the problem occur?
* **Why Successful Retrieval Matters** - What does successful retrieval enable for the user?
* **Research Question** - What should be validated through further user research/interviews?

#### Important
Do not show:
* “Build Feature X”
* “Add Feature Y”
* “Best Opportunity”
* “Highest Priority”
* Product solution recommendations

The purpose is to identify opportunity areas, not prematurely decide the solution.

---

# DESIGN PRINCIPLES

Build this as a Product Manager's research tool, not as a generic analytics dashboard.

**Prioritize:**
* Use Fluent 2 Design System
* Simple language in the UI (no heavy jargon)
* Evidence
* Traceability
* User behavior
* Retrieval journey
* Frequency
* Patterns
* Contradictions
* Research hypotheses
* Easy to read and understand
* Consistent spacing, no overlaps

**Avoid:**
* Generic sentiment dashboards
* Word clouds as the main analysis
* Vanity metrics
* Unsupported conclusions
* Fabricated statistics
* Premature solution recommendations
* Complex words and complex design

---
