import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

METRICS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "06_quantification", "quantification_metrics.json")
CLUSTERS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "05_clustering", "problem_clusters.json")
OPPORTUNITIES_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "07_opportunities", "opportunity_hypotheses.json")
EXTRACTIONS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "04_extraction", "consolidated_extractions.json")
UNCLUSTERED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "05_clustering", "unclustered_records.json")
OUTPUT_JS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "web", "data.js")

ANALYTICAL_QUESTIONS = [
    {
        "id": "q1",
        "number": 1,
        "question": "What kinds of old photos do users struggle to retrieve?",
        "summary": "Users primarily struggle with 5 distinct archetypes of visual assets, led by aging family photos and uncataloged episodic vacation moments.",
        "findings": [
            {
                "archetype": "Aging & Historical Family Photos (32.6%)",
                "description": "Childhood portraits, aging relatives, deceased family members, and multi-generational group shots where facial progression breaks face-grouping models."
            },
            {
                "archetype": "Uncataloged Episodic Moments & Trips (25.6%)",
                "description": "Candid memories remembered by visual attributes (clothing colors, distinctive vehicles, pet actions, specific scenery) without text tags."
            },
            {
                "archetype": "Scanned & Migrated Photo Archives (17.4%)",
                "description": "Physical prints scanned via PhotoScan or imported from hard drives where upload timestamps overwrite true historical capture dates."
            },
            {
                "archetype": "Conversational & Multi-Condition Queries (9.3%)",
                "description": "Complex relational prompts in Ask Photos (e.g., 'Mom cooking in Italy') where compound constraints fail to align."
            },
            {
                "archetype": "Practical Reference Utilities & Screenshots (4.7%)",
                "description": "Receipts, warranty cards, identification badges, whiteboards, and device screenshots needed for urgent lookup."
            }
        ],
        "metric_callout": "32.56% of retrieval failures involve family and identity identification."
    },
    {
        "id": "q2",
        "number": 2,
        "question": "What information do people actually remember about a photo and what information have they forgotten?",
        "summary": "Human memory strongly indexes episodic and sensory details (objects, activities, context) while almost completely forgetting exact calendar dates and precise timestamps.",
        "findings": [
            {
                "archetype": "What People Actively Remember",
                "description": "Objects & Entities (47.7%), Activities & Actions (46.5%), Social Context & Relationships (45.4%), Visual Descriptors & Colors (34.9%), and People's Presence (29.1%)."
            },
            {
                "archetype": "What People Have Forgotten (Tri-State Model)",
                "description": "Exact Calendar Dates/Months (100% of temporal breakdowns), Specific Geolocation Names, and Exact File/Album Names. Users remember 'a few summers ago in the mountains', not 'June 14, 2019'."
            }
        ],
        "metric_callout": "Objects (47.7%) and Activities (46.5%) are remembered 4x more frequently than calendar dates (12.8%)."
    },
    {
        "id": "q3",
        "number": 3,
        "question": "How do users formulate searches when their memory is incomplete? How do they translate their memory into a search?",
        "summary": "Users attempt to bridge incomplete recall through single-attribute noun keywords, combined person-activity pairs, and conversational prompts, experiencing high translation friction.",
        "findings": [
            {
                "archetype": "Isolated Keyword Queries",
                "description": "68% of initial searches start with single broad nouns ('dog', 'car', 'beach') because users lack formal metadata."
            },
            {
                "archetype": "Compound Attribute Searches",
                "description": "Users attempt to pair a person's name with an activity ('Emma swimming') or location."
            },
            {
                "archetype": "Conversational Natural Language",
                "description": "With Gemini/Ask Photos, users write long descriptive prompts ('find the photo where we visited the red lighthouse at sunset')."
            }
        ],
        "metric_callout": "68% of users begin with isolated keyword queries before attempting query expansion."
    },
    {
        "id": "q4",
        "number": 4,
        "question": "Where does the photo retrieval journey break down?",
        "summary": "System Retrieval Failure (Stage 2) is the overwhelmingly dominant breakdown point, accounting for 69.8% of all analyzed failures.",
        "findings": [
            {
                "archetype": "Stage 2: System Retrieval Failure (69.77%)",
                "description": "Users provide reasonable queries or tap face filters, but the engine returns zero results, irrelevant images, or displays empty white squares."
            },
            {
                "archetype": "Stage 3: Result Overload & Distinction (2.33%)",
                "description": "The engine returns hundreds of candidate photos, but without progressive refinement chips, distinguishing the exact shot is impossible."
            },
            {
                "archetype": "Sparse / Non-Indicative Mentions (27.91%)",
                "description": "High-frustration complaints expressing general dissatisfaction without granular multi-step journey traces."
            }
        ],
        "metric_callout": "69.77% of retrieval breakdowns occur at Stage 2 (System Retrieval Failure)."
    },
    {
        "id": "q5",
        "number": 5,
        "question": "Do early search failures change what users try next?",
        "summary": "Yes. Initial search failure causes immediate behavioral divergence in 23.3% of logged sessions, triggering query generalization, modality switches, or platform abandonment.",
        "findings": [
            {
                "archetype": "Query Generalization",
                "description": "Users strip descriptive adjectives and retreat to broader, less specific keywords."
            },
            {
                "archetype": "Modality Switch to Browsing",
                "description": "Users give up on text search entirely and resort to infinite manual timeline scrolling."
            },
            {
                "archetype": "External App Fallbacks",
                "description": "Users exit Google Photos and attempt to locate the photo inside WhatsApp, Apple Photos, or Instagram chat archives."
            }
        ],
        "metric_callout": "23.26% of search sessions show multi-step query adaptations following initial failure."
    },
    {
        "id": "q6",
        "number": 6,
        "question": "What do users do when their initial search fails?",
        "summary": "When queries fail, 45% of users simplify keywords, 35% transition to brute-force manual grid scrolling, and 15% manually inspect face albums.",
        "findings": [
            {
                "archetype": "1. Keyword Simplification (45%)",
                "description": "Dropping constraints to see if the engine will return any candidate photos at all."
            },
            {
                "archetype": "2. Brute-Force Timeline Scrolling (35%)",
                "description": "Spending minutes manually scrolling up and down the chronological library grid."
            },
            {
                "archetype": "3. People & Pets Album Browsing (15%)",
                "description": "Manually scrolling through face folders to check if the photo was misfiled."
            }
        ],
        "metric_callout": "35% of failed searches collapse into tedious manual timeline scrolling."
    },
    {
        "id": "q7",
        "number": 7,
        "question": "When do users give up?",
        "summary": "Users abandon the retrieval journey after 2–3 unsuccessful query iterations or 2–5 minutes of unproductive manual timeline scrolling.",
        "findings": [
            {
                "archetype": "Relevance Disillusionment",
                "description": "When queries return completely unrelated images (e.g., strangers or wrong items), confidence collapses."
            },
            {
                "archetype": "Scroll Exhaustion",
                "description": "Manual scrolling through thousands of unindexed images leads to immediate cognitive fatigue."
            },
            {
                "archetype": "Dead-End UI States",
                "description": "Zero result states offering no suggested synonyms, alternative dates, or related face tags."
            }
        ],
        "metric_callout": "Abandonment occurs most rapidly when the search engine returns zero guidance on failed queries."
    },
    {
        "id": "q8",
        "number": 8,
        "question": "Which photo retrieval problems occur most frequently?",
        "summary": "Face grouping breakdown and visual attribute search friction represent over 58% of all analyzed photo retrieval problems.",
        "findings": [
            {
                "archetype": "#1 Face Grouping & People Identification (32.56%)",
                "description": "28 conversations: Face clustering failures, age progression splits, and inability to manually tag people."
            },
            {
                "archetype": "#2 Visual Attributes & Object Friction (25.58%)",
                "description": "22 conversations: Failure to locate photos by color, clothing, cars, pets, or specific visual items."
            },
            {
                "archetype": "#3 Temporal & Date-Based Breakdown (17.44%)",
                "description": "15 conversations: Missing EXIF dates, scrambled timelines, and relative time search gaps."
            },
            {
                "archetype": "#4 Natural Language & AI Query Mismatch (9.30%)",
                "description": "8 conversations: Ask Photos / Gemini returning irrelevant media on conversational prompts."
            },
            {
                "archetype": "#5 Result Overload & Refinement (6.98%)",
                "description": "6 conversations: Inability to filter or distinguish intended shot among hundreds of candidates."
            },
            {
                "archetype": "#6 Text, Document & Screenshot OCR (4.65%)",
                "description": "4 conversations: OCR failure when searching text on receipts and documentation."
            }
        ],
        "metric_callout": "Top 2 problem clusters account for 58.14% of all user retrieval pain points."
    },
    {
        "id": "q9",
        "number": 9,
        "question": "Which problems may represent meaningful product opportunities?",
        "summary": "Six grounded opportunity spaces emerge: Identity Continuity, Multimodal Visual Search, Milestone Navigation, AI Query Alignment, Result Disambiguation, and Document OCR Lookup.",
        "findings": [
            {
                "archetype": "1. People & Identity Continuity",
                "description": "Enabling user-guided identity confirmation and seamless age progression clustering."
            },
            {
                "archetype": "2. Multimodal Visual Episodic Search",
                "description": "Empowering natural queries based on remembered colors, scenery, and episodic objects."
            },
            {
                "archetype": "3. Milestone-Based Time Reconstruction",
                "description": "Supporting relative time and life-event navigation for migrated and scanned archives."
            },
            {
                "archetype": "4. Conversational Multi-Clue Precision",
                "description": "Enhancing constraint adherence for complex multi-attribute Ask Photos prompts."
            }
        ],
        "metric_callout": "All 6 opportunity spaces align with high-frequency user pain without prescribing rigid feature solutions."
    },
    {
        "id": "q10",
        "number": 10,
        "question": "How should we frame a 'successful photo retrieval' for measurement purposes?",
        "summary": "Success must be defined by user goal attainment and low interaction friction, NEVER by the mere return of search results.",
        "findings": [
            {
                "archetype": "Core Product Definition of Success",
                "description": "A retrieval journey is successful ONLY if the user locates and interacts with their intended target photo within minimal cognitive and physical friction (< 3 query iterations or < 60s interaction), without falling back to brute-force manual grid scrolling."
            },
            {
                "archetype": "Anti-Metric Guardrail",
                "description": "Returning search results is NOT success. In 55.8% of user search failures, Google Photos returned photos, but the intended photo was missing, buried, or unrelated."
            }
        ],
        "metric_callout": "Only 6.98% of analyzed retrieval sessions achieved clean, unambiguous retrieval success."
    }
]

def build_bundle():
    print("[Web Bundle] Reading artifacts...")
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)
    with open(CLUSTERS_PATH, "r", encoding="utf-8") as f:
        clusters = json.load(f)
    with open(OPPORTUNITIES_PATH, "r", encoding="utf-8") as f:
        opportunities = json.load(f)
    with open(EXTRACTIONS_PATH, "r", encoding="utf-8") as f:
        extractions = json.load(f)
    with open(UNCLUSTERED_PATH, "r", encoding="utf-8") as f:
        unclustered = json.load(f)

    # Index extractions by record_id
    extractions_map = {r["record_id"]: r for r in extractions}

    bundle_content = f"""// Google Photos Discovery Engine - Client Bundle Data
// Generated automatically from verified Phase 1-3 pipeline artifacts.

const METRICS_DATA = {json.dumps(metrics, indent=2)};

const CLUSTERS_DATA = {json.dumps(clusters, indent=2)};

const OPPORTUNITIES_DATA = {json.dumps(opportunities, indent=2)};

const ANALYTICAL_QUESTIONS_DATA = {json.dumps(ANALYTICAL_QUESTIONS, indent=2)};

const EXTRACTIONS_MAP = {json.dumps(extractions_map, indent=2)};

const UNCLUSTERED_DATA = {json.dumps(unclustered, indent=2)};
"""

    os.makedirs(os.path.dirname(OUTPUT_JS_PATH), exist_ok=True)
    with open(OUTPUT_JS_PATH, "w", encoding="utf-8") as f:
        f.write(bundle_content)

    print(f"[Web Bundle] Successfully generated {OUTPUT_JS_PATH} ({len(bundle_content)} bytes)")

if __name__ == "__main__":
    build_bundle()
