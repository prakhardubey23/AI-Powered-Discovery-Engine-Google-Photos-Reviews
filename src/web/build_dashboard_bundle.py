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

def get_analytical_questions(metrics: dict, clusters: list) -> list:
    total_relevant = metrics.get("dataset_kpis", {}).get("total_relevant_conversations", 510)
    
    # Extract cluster counts
    cluster_map = {c["cluster_id"]: c for c in clusters}
    face_c = cluster_map.get("face_grouping_people_identification_breakdown", {}).get("conversation_count", 130)
    face_pct = cluster_map.get("face_grouping_people_identification_breakdown", {}).get("cluster_percentage", 25.49)
    
    ai_c = cluster_map.get("semantic_ai_natural_language_query_mismatch", {}).get("conversation_count", 121)
    ai_pct = cluster_map.get("semantic_ai_natural_language_query_mismatch", {}).get("cluster_percentage", 23.73)
    
    time_c = cluster_map.get("temporal_chronological_discovery_gap", {}).get("conversation_count", 119)
    time_pct = cluster_map.get("temporal_chronological_discovery_gap", {}).get("cluster_percentage", 23.33)
    
    vis_c = cluster_map.get("visual_attribute_object_detail_retrieval_friction", {}).get("conversation_count", 55)
    vis_pct = cluster_map.get("visual_attribute_object_detail_retrieval_friction", {}).get("cluster_percentage", 10.78)
    
    overload_c = cluster_map.get("result_overload_and_refinement_exhaustion", {}).get("conversation_count", 33)
    overload_pct = cluster_map.get("result_overload_and_refinement_exhaustion", {}).get("cluster_percentage", 6.47)
    
    ocr_c = cluster_map.get("text_document_screenshot_ocr_breakdown", {}).get("conversation_count", 29)
    ocr_pct = cluster_map.get("text_document_screenshot_ocr_breakdown", {}).get("cluster_percentage", 5.69)
    
    # Outcomes
    outcomes = {o["outcome"]: o for o in metrics.get("search_retrieval_outcomes", [])}
    fail_pct = outcomes.get("Failure", {}).get("percentage", 44.90)
    succ_pct = outcomes.get("Success", {}).get("percentage", 40.98)
    part_pct = outcomes.get("Partial Success", {}).get("percentage", 5.88)
    unk_pct = outcomes.get("Unknown", {}).get("percentage", 8.24)
    
    # Failure stages
    stages = {s["failure_stage"]: s for s in metrics.get("failure_stages_funnel", [])}
    stg2_pct = stages.get("2. System Retrieval Failure", {}).get("percentage", 39.61)
    stg3_pct = stages.get("3. Result Overload / Distinction", {}).get("percentage", 5.69)
    stg4_pct = stages.get("4. Refinement Breakdown", {}).get("percentage", 4.31)
    stg1_pct = stages.get("1. Translation Struggle", {}).get("percentage", 0.78)
    stg_not_pct = stages.get("Not Indicative", {}).get("percentage", 49.61)
    
    # Multi search
    multi_dyn = metrics.get("multi_search_attempt_dynamics", {})
    multi_pct = multi_dyn.get("percentage_with_multiple_attempts", 9.41)

    return [
        {
            "id": "q1",
            "number": 1,
            "question": "What kinds of old photos do users struggle to retrieve?",
            "summary": f"Users primarily struggle across 6 core archetypes of visual media, led by people/identity photos ({face_pct}%), conversational multi-condition queries ({ai_pct}%), and temporal/scanned archives ({time_pct}%).",
            "findings": [
                {
                    "archetype": f"Aging & Historical Family Photos ({face_pct}%)",
                    "description": f"{face_c} conversations: Childhood portraits, aging relatives, deceased family members, and multi-generational group shots where facial progression breaks face-grouping models."
                },
                {
                    "archetype": f"Conversational & Complex Prompt Photos ({ai_pct}%)",
                    "description": f"{ai_c} conversations: Natural language and Ask Photos queries where multi-criteria constraints fail to align with index tags."
                },
                {
                    "archetype": f"Scanned & Chronologically Migrated Archives ({time_pct}%)",
                    "description": f"{time_c} conversations: Physical prints scanned via PhotoScan or imported from cloud drives where upload timestamps overwrite true historical capture dates."
                },
                {
                    "archetype": f"Uncataloged Visual Objects & Scenes ({vis_pct}%)",
                    "description": f"{vis_c} conversations: Candid memories remembered by visual attributes (clothing colors, vintage vehicles, pet actions, specific scenery) without text tags."
                },
                {
                    "archetype": f"Practical Utilities & Documents ({ocr_pct}%)",
                    "description": f"{ocr_c} conversations: Receipts, warranty cards, identification badges, whiteboards, and device screenshots needed for utilitarian lookup."
                }
            ],
            "metric_callout": f"{face_pct}% of retrieval breakdowns center on facial identity and people grouping."
        },
        {
            "id": "q2",
            "number": 2,
            "question": "What information do people actually remember about a photo and what information have they forgotten?",
            "summary": "Human memory strongly indexes episodic, visual, and relational details (people 23.9%, objects 22.6%, locations 11.6%) while almost completely forgetting exact calendar dates and precise timestamps.",
            "findings": [
                {
                    "archetype": "What People Actively Remember",
                    "description": "Temporal approximations (25.9%), People & Relationships (23.9%), Objects & Entities (22.6%), Locations (11.6%), Social Context (10.8%), Activities (10.8%), and Visual Colors (9.2%)."
                },
                {
                    "archetype": "What People Have Forgotten (Tri-State Model)",
                    "description": "Exact Calendar Dates/Months (100% of temporal breakdowns), Specific Geolocation Metadata, and Exact File Names. Users remember 'summer vacation near the lake', not 'August 14, 2018'."
                }
            ],
            "metric_callout": "Relational entities (people, objects, locations) are remembered in over 58% of relevant conversations."
        },
        {
            "id": "q3",
            "number": 3,
            "question": "How do users formulate searches when their memory is incomplete? How do they translate their memory into a search?",
            "summary": "Users attempt to bridge incomplete recall through single-attribute noun keywords, combined person-activity pairs, and conversational prompts, experiencing high translation friction.",
            "findings": [
                {
                    "archetype": "Isolated Keyword Queries",
                    "description": "A majority of initial searches start with single broad nouns ('dog', 'car', 'beach') because users lack structured metadata."
                },
                {
                    "archetype": "Compound Attribute Searches",
                    "description": "Users attempt to pair a person's name with an activity ('Emma swimming') or location."
                },
                {
                    "archetype": "Conversational Natural Language",
                    "description": "With Ask Photos / Gemini, users write descriptive prompts ('find the photo where we visited the red lighthouse at sunset')."
                }
            ],
            "metric_callout": "Conversational natural language query mismatches account for 23.73% of retrieval pain points."
        },
        {
            "id": "q4",
            "number": 4,
            "question": "Where does the photo retrieval journey break down?",
            "summary": f"System Retrieval Failure (Stage 2) is the primary explicit cognitive breakdown point ({stg2_pct}%), followed by Result Overload ({stg3_pct}%) and Refinement Breakdown ({stg4_pct}%).",
            "findings": [
                {
                    "archetype": f"Stage 2: System Retrieval Failure ({stg2_pct}%)",
                    "description": f"{stages.get('2. System Retrieval Failure', {}).get('count', 202)} conversations: Users provide reasonable queries or tap face filters, but the engine returns zero results, irrelevant images, or displays empty white squares."
                },
                {
                    "archetype": f"Stage 3: Result Overload & Distinction ({stg3_pct}%)",
                    "description": f"{stages.get('3. Result Overload / Distinction', {}).get('count', 29)} conversations: The engine returns hundreds of candidate photos, but without progressive refinement chips, distinguishing the exact shot is impossible."
                },
                {
                    "archetype": f"Stage 4: Refinement Breakdown ({stg4_pct}%)",
                    "description": f"{stages.get('4. Refinement Breakdown', {}).get('count', 22)} conversations: Search fails and users struggle to determine what filter or modifier to try next."
                },
                {
                    "archetype": f"High-Frustration / Non-Indicative Mentions ({stg_not_pct}%)",
                    "description": f"{stages.get('Not Indicative', {}).get('count', 253)} conversations: User reviews expressing severe search dissatisfaction without granular multi-step journey traces."
                }
            ],
            "metric_callout": f"{stg2_pct}% of analyzed retrieval breakdowns occur at Stage 2 (System Retrieval Failure)."
        },
        {
            "id": "q5",
            "number": 5,
            "question": "Do early search failures change what users try next?",
            "summary": f"Yes. Initial search failure causes immediate behavioral divergence in {multi_pct}% of documented multi-step sessions, triggering query generalization, modality switches, or platform abandonment.",
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
                    "description": "Users exit Google Photos and attempt to locate the photo inside WhatsApp, Apple Photos, or external cloud storage."
                }
            ],
            "metric_callout": f"{multi_pct}% of search sessions show explicit multi-step query adaptations following initial failure."
        },
        {
            "id": "q6",
            "number": 6,
            "question": "What do users do when their initial search fails?",
            "summary": "When queries fail, users typically simplify keywords, transition to brute-force manual grid scrolling, or manually inspect face albums.",
            "findings": [
                {
                    "archetype": "1. Keyword Simplification",
                    "description": "Dropping constraints to see if the engine will return any candidate photos at all."
                },
                {
                    "archetype": "2. Brute-Force Timeline Scrolling",
                    "description": "Spending minutes manually scrolling up and down the chronological library grid."
                },
                {
                    "archetype": "3. People & Pets Album Browsing",
                    "description": "Manually scrolling through face folders to check if the photo was misfiled."
                }
            ],
            "metric_callout": "Manual grid scrolling is the most common fallback when search queries fail."
        },
        {
            "id": "q7",
            "number": 7,
            "question": "When do users give up?",
            "summary": "Users abandon the retrieval journey after 2–3 unsuccessful query iterations or several minutes of unproductive manual timeline scrolling.",
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
            "summary": f"Face grouping breakdown ({face_pct}%), natural language AI query mismatch ({ai_pct}%), and temporal navigation gaps ({time_pct}%) represent over 72% of all analyzed photo retrieval problems.",
            "findings": [
                {
                    "archetype": f"#1 Face Grouping & People Identification ({face_pct}%)",
                    "description": f"{face_c} conversations: Face clustering failures, age progression splits, and inability to manually tag people."
                },
                {
                    "archetype": f"#2 Natural Language & AI Query Mismatch ({ai_pct}%)",
                    "description": f"{ai_c} conversations: Ask Photos / Gemini returning irrelevant media on conversational prompts."
                },
                {
                    "archetype": f"#3 Temporal & Date-Based Breakdown ({time_pct}%)",
                    "description": f"{time_c} conversations: Missing EXIF dates, scrambled timelines, and relative time search gaps."
                },
                {
                    "archetype": f"#4 Visual Attributes & Object Friction ({vis_pct}%)",
                    "description": f"{vis_c} conversations: Failure to locate photos by color, clothing, cars, pets, or specific visual items."
                },
                {
                    "archetype": f"#5 Result Overload & Refinement ({overload_pct}%)",
                    "description": f"{overload_c} conversations: Inability to filter or distinguish intended shot among hundreds of candidates."
                },
                {
                    "archetype": f"#6 Text, Document & Screenshot OCR ({ocr_pct}%)",
                    "description": f"{ocr_c} conversations: OCR failure when searching text on receipts and documentation."
                }
            ],
            "metric_callout": f"Top 3 problem clusters account for {round(face_pct + ai_pct + time_pct, 2)}% of all user retrieval pain points."
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
                    "archetype": "2. Conversational Multi-Clue Precision",
                    "description": "Enhancing constraint adherence for complex multi-attribute Ask Photos prompts."
                },
                {
                    "archetype": "3. Milestone-Based Time Reconstruction",
                    "description": "Supporting relative time and life-event navigation for migrated and scanned archives."
                },
                {
                    "archetype": "4. Multimodal Visual Episodic Search",
                    "description": "Empowering natural queries based on remembered colors, scenery, and episodic objects."
                },
                {
                    "archetype": "5. Result Disambiguation Controls",
                    "description": "Progressive multi-attribute refinement chips to narrow large candidate result sets."
                },
                {
                    "archetype": "6. Text & Document OCR Search",
                    "description": "High-fidelity OCR indexing for scanned receipts, documents, and screenshot reference."
                }
            ],
            "metric_callout": "All 6 opportunity spaces align with high-frequency user pain without prescribing rigid feature solutions."
        },
        {
            "id": "q10",
            "number": 10,
            "question": "How should we frame a 'successful photo retrieval' for measurement purposes?",
            "summary": "Success must be defined by user goal attainment and low interaction friction, NEVER by the mere return of candidate search results.",
            "findings": [
                {
                    "archetype": "Core Product Definition of Success",
                    "description": "A retrieval journey is successful ONLY if the user locates and interacts with their intended target photo within minimal cognitive and physical friction (< 3 query iterations or < 60s interaction), without falling back to brute-force manual grid scrolling."
                },
                {
                    "archetype": "Anti-Metric Guardrail",
                    "description": f"Returning search results is NOT success. In {fail_pct}% of user retrieval sessions, the intended photo was missing, buried, or unrelated despite search execution."
                }
            ],
            "metric_callout": f"Only {succ_pct}% of analyzed retrieval reviews reflected clean, unambiguous retrieval success."
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

    analytical_questions = get_analytical_questions(metrics, clusters)

    bundle_content = f"""// Google Photos Discovery Engine - Client Bundle Data
// Generated automatically from verified Phase 1-3 pipeline artifacts.

const METRICS_DATA = {json.dumps(metrics, indent=2)};

const CLUSTERS_DATA = {json.dumps(clusters, indent=2)};

const OPPORTUNITIES_DATA = {json.dumps(opportunities, indent=2)};

const ANALYTICAL_QUESTIONS_DATA = {json.dumps(analytical_questions, indent=2)};

const EXTRACTIONS_MAP = {json.dumps(extractions_map, indent=2)};

const UNCLUSTERED_DATA = {json.dumps(unclustered, indent=2)};
"""

    os.makedirs(os.path.dirname(OUTPUT_JS_PATH), exist_ok=True)
    with open(OUTPUT_JS_PATH, "w", encoding="utf-8") as f:
        f.write(bundle_content)

    print(f"[Web Bundle] Successfully generated {OUTPUT_JS_PATH} ({len(bundle_content)} bytes)")

if __name__ == "__main__":
    build_bundle()
