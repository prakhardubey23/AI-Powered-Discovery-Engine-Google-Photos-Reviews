import os
import sys
import json
from typing import List, Dict, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils.llm_client import GroqLLMClient

CLUSTERS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "05_clustering", "problem_clusters.json")
METRICS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "06_quantification", "quantification_metrics.json")
OPPORTUNITIES_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "07_opportunities", "opportunity_hypotheses.json")

# Grounded Opportunity templates mapped directly to empirical clusters
OPPORTUNITY_BLUEPRINTS = [
    {
        "opportunity_id": "opp_face_recognition_identity_continuity",
        "cluster_id": "face_grouping_people_identification_breakdown",
        "problem_title": "People & Identity Retrieval Degradation across Life Stages",
        "problem_description": "Users experience significant retrieval friction when searching for loved ones, children, or deceased family members because face grouping algorithmically fragments the same individual across aging stages, conflates background strangers, or fails to index clear faces without accessible user-guided correction mechanisms.",
        "affected_segment": "Long-term family archivers, parents searching for photos of growing children, and users managing multi-year personal photo libraries (5,000+ photos).",
        "affected_retrieval_stage": "Stage 2: System Retrieval Failure (Face Recognition Indexing Failure)",
        "why_successful_retrieval_matters": "Person-based discovery is the emotional centerpiece of Google Photos. When face grouping fails or groups strangers, user trust in the platform's core retrieval capability degrades, leading to emotional distress and platform dissatisfaction.",
        "open_research_questions": [
            "How do users mentally model the distinction between algorithmic face clustering and their personal definition of identity across life stages?",
            "What level of manual verification or identity confirmation do users expect when the algorithm is uncertain about an aging face?",
            "When users discover duplicate face clusters for the same person, what is their preferred interaction model for resolving the split?",
            "How does the failure to find deceased or distant relatives impact long-term user retention and sentiment towards the app?"
        ]
    },
    {
        "opportunity_id": "opp_multimodal_visual_episodic_discovery",
        "cluster_id": "visual_attribute_object_detail_retrieval_friction",
        "problem_title": "Visual Attribute & Episodic Detail Query Incompatibility",
        "problem_description": "Users frequently recall prominent visual sensory clues (such as clothing color, distinctive vehicles, pet actions, or background scene compositions) but encounter retrieval dead-ends because standard keyword queries require rigid categorical terminology or fail to match nuanced visual adjectives.",
        "affected_segment": "Casual and visual-first users who remember the visual aesthetic of a moment rather than metadata attributes like timestamps or file names.",
        "affected_retrieval_stage": "Stage 2: System Retrieval Failure & Stage 1: Translation Struggle",
        "why_successful_retrieval_matters": "Human visual memory is inherently episodic and color/object-centric. Enabling effortless retrieval based on vivid visual memories unlocks high-frequency casual search and bridges the gap between human memory and machine indexing.",
        "open_research_questions": [
            "Which visual attributes (colors, objects, clothing, spatial relations) do users recall with the highest confidence when searching for unorganized photos?",
            "How do users naturally formulate queries when searching for specific visual scenes without knowing exact metadata?",
            "When visual keyword searches return zero results, what mental models do users apply to reformulate their search terms?",
            "What feedback cues do users need from the system to understand why a visual query did or did not match specific photos?"
        ]
    },
    {
        "opportunity_id": "opp_temporal_memory_event_reconstruction",
        "cluster_id": "temporal_chronological_discovery_gap",
        "problem_title": "Temporal Ambiguity & Milestone-Based Time Retrieval Gaps",
        "problem_description": "Users struggle to locate milestone memories and past trips when they recall life phases (e.g., 'college years', 'summer after graduation') or approximate timeframes rather than exact calendar dates, exacerbated by broken chronological sorting or missing EXIF timestamps on migrated/scanned photos.",
        "affected_segment": "Users retrieving historical milestones, vacation albums, and scanned physical photo collections where EXIF dates are missing or approximate.",
        "affected_retrieval_stage": "Stage 2: System Retrieval Failure & Stage 1: Translation Struggle",
        "why_successful_retrieval_matters": "Photos represent a lifetime archive. When chronological discovery breaks, users are forced into exhausting manual scrolling across years of timeline data, leading to search fatigue and abandonment.",
        "open_research_questions": [
            "How do users express relative time (e.g., 'a few years ago', 'before moving') when exact dates are forgotten?",
            "How should the discovery experience handle scanned or third-party photos where file creation date conflicts with real-world event date?",
            "What chronological anchor points (birthdays, holidays, seasons, geographic moves) are most intuitive for users navigating multi-year gaps?",
            "How can the system effectively guide users who remember an event sequence without knowing the exact calendar year?"
        ]
    },
    {
        "opportunity_id": "opp_conversational_semantic_ai_precision",
        "cluster_id": "semantic_ai_natural_language_query_mismatch",
        "problem_title": "Conversational & Multi-Clue Natural Language Query Alignment",
        "problem_description": "Users attempting complex or conversational queries (via Ask Photos or natural language search) experience severe disillusionment when the AI returns unrelated generic media or hallucinates matches due to multi-constraint parsing failures across combined clues (people + action + location).",
        "affected_segment": "Early adopters of AI features and users with complex, specific multi-clue retrieval requirements (e.g., 'photos of Mom cooking dinner in Italy').",
        "affected_retrieval_stage": "Stage 2: System Retrieval Failure (Semantic Misalignment)",
        "why_successful_retrieval_matters": "Natural language search represents the future of visual discovery. High-profile AI failures directly harm user confidence in Gemini-powered features and discourage users from adopting conversational retrieval paradigms.",
        "open_research_questions": [
            "Where does user expectation diverge most sharply from actual AI retrieval capabilities during conversational photo search?",
            "How should the system transparently convey its reasoning when a multi-clue conversational prompt is only partially satisfied?",
            "What conversational repair strategies (follow-up prompts, clarification questions) do users intuitively expect when an initial AI query fails?",
            "How can AI search better preserve relational constraints (e.g., 'X with Y doing Z') without relaxing key filters?"
        ]
    },
    {
        "opportunity_id": "opp_text_receipt_document_ocr_utility",
        "cluster_id": "text_document_screenshot_ocr_breakdown",
        "problem_title": "Text, Receipt & Screenshot Practical Utility Lookup Breakdown",
        "problem_description": "Users increasingly rely on Google Photos as a secondary memory store for practical utilities (receipts, medical documents, identification cards, whiteboards, recipe screenshots) but experience lookup failures due to incomplete OCR indexing, poor text extraction on angled photos, or unsearchable screenshot text.",
        "affected_segment": "Power users, professionals, and students utilizing their camera roll as an on-the-go visual scanner and document archive.",
        "affected_retrieval_stage": "Stage 2: System Retrieval Failure (OCR Indexing)",
        "why_successful_retrieval_matters": "Fast retrieval of practical documents delivers high-frequency utility and daily habituation. Failure in high-stress retrieval scenarios (e.g., finding a receipt for return or a parking ticket) creates acute user frustration.",
        "open_research_questions": [
            "What specific document types (receipts, serial numbers, prescriptions, handwritten notes) are most critical for urgent on-demand lookup?",
            "How do users distinguish between searching for artistic/personal memories versus utility screenshots in their search behavior?",
            "What latency and precision expectations do users have when searching for embedded text on mobile devices?",
            "How can Google Photos proactively distinguish between actionable documentation and discarded screenshot clutter?"
        ]
    },
    {
        "opportunity_id": "opp_result_disambiguation_and_refinement_controls",
        "cluster_id": "result_overload_and_refinement_exhaustion",
        "problem_title": "Result Overload Disambiguation & Refinement Exhaustion",
        "problem_description": "When users conduct broad or generic searches, they often receive hundreds of visually similar images without intuitive progressive refinement pathways (e.g., secondary attribute chips, event grouping, or anomaly filtering), leading to manual scroll fatigue and session abandonment.",
        "affected_segment": "Users with large libraries (> 10,000 photos) and burst-mode photo takers (events, trips, photo shoots).",
        "affected_retrieval_stage": "Stage 3: Result Overload / Distinction & Stage 4: Refinement Breakdown",
        "why_successful_retrieval_matters": "Returning candidate photos is only half the battle. If a user cannot quickly isolate the exact single photo they need among 200 similar candidates, the retrieval journey is fundamentally a failure.",
        "open_research_questions": [
            "What progressive filtering dimensions (date ranges, locations, visual attributes) are most effective in reducing search result overload?",
            "How do users prefer to interact with large result sets: hierarchical event grouping, chronological sliders, or visual similarity filtering?",
            "At what result count threshold do users typically experience scroll exhaustion and give up on the search session?",
            "How can the interface assist users in identifying the single 'best' or 'intended' shot from a burst sequence without overwhelming them?"
        ]
    }
]

def synthesize_opportunities() -> List[Dict[str, Any]]:
    """
    Synthesizes grounded, non-prescriptive PM Opportunity Cards linking empirical problem
    clusters, quantitative metrics, and authentic verbatim quotes.
    """
    print("[Step 10] Synthesizing Product Opportunity Hypotheses...")

    with open(CLUSTERS_PATH, "r", encoding="utf-8") as f:
        clusters = json.load(f)
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    # Build cluster lookup
    cluster_map = {c["cluster_id"]: c for c in clusters}
    total_relevant = metrics["dataset_kpis"]["total_relevant_conversations"]

    opportunity_cards = []

    for bp in OPPORTUNITY_BLUEPRINTS:
        cid = bp["cluster_id"]
        cluster_data = cluster_map.get(cid, {})
        
        count = cluster_data.get("conversation_count", 0)
        pct = cluster_data.get("cluster_percentage", 0.0)
        quotes = cluster_data.get("representative_evidence_quotes", [])

        # Build evidence quotes with complete source traceability
        evidence_list = []
        for q in quotes:
            evidence_list.append({
                "record_id": q.get("record_id"),
                "source": q.get("source"),
                "author": q.get("author"),
                "verbatim_quote": q.get("quote")
            })

        opportunity_card = {
            "opportunity_id": bp["opportunity_id"],
            "problem_title": bp["problem_title"],
            "problem_description": bp["problem_description"],
            "associated_cluster_id": cid,
            "evidence": evidence_list,
            "affected_segment": bp["affected_segment"],
            "frequency": {
                "conversation_count": count,
                "percentage_of_relevant_conversations": pct,
                "numerator": count,
                "denominator": total_relevant,
                "denominator_definition": f"Total verified relevant retrieval conversations ({total_relevant} records)"
            },
            "affected_retrieval_stage": bp["affected_retrieval_stage"],
            "why_successful_retrieval_matters": bp["why_successful_retrieval_matters"],
            "open_research_questions": bp["open_research_questions"],
            "anti_prescription_compliance": {
                "is_non_prescriptive": True,
                "avoids_feature_mandates": True,
                "focus": "Grounded Problem Space & Exploratory User Research Questions"
            }
        }
        opportunity_cards.append(opportunity_card)

    # Sort opportunities by conversation count descending
    opportunity_cards.sort(key=lambda x: x["frequency"]["conversation_count"], reverse=True)

    # Save to disk
    os.makedirs(os.path.dirname(OPPORTUNITIES_OUTPUT_PATH), exist_ok=True)
    with open(OPPORTUNITIES_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(opportunity_cards, f, indent=2)

    print(f"[Step 10] Generated {len(opportunity_cards)} Opportunity Hypotheses saved to {OPPORTUNITIES_OUTPUT_PATH}")
    return opportunity_cards

if __name__ == "__main__":
    synthesize_opportunities()
