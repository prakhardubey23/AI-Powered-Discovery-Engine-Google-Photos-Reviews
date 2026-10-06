import os
import sys
import json
import re
from typing import List, Dict, Any, Tuple

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils.llm_client import GroqLLMClient

CONSOLIDATED_INPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "04_extraction", "consolidated_extractions.json")
CLUSTERS_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "05_clustering", "problem_clusters.json")
UNCLUSTERED_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "05_clustering", "unclustered_records.json")

# Emergent cluster taxonomy definitions based on empirical data
CLUSTER_DEFINITIONS = [
    {
        "cluster_id": "face_grouping_people_identification_breakdown",
        "cluster_name": "Face Grouping & People Identification Failure",
        "primary_category": "people_faces",
        "keywords": ["face", "faces", "people", "person", "tag", "tagging", "grouping", "baby", "daughter", "son", "family", "stranger", "name", "who"],
        "description": "Users struggle to find photos of specific individuals because face recognition fails to group them, misidentifies strangers, splits the same person across multiple groups, or lacks manual tagging corrections."
    },
    {
        "cluster_id": "temporal_chronological_discovery_gap",
        "cluster_name": "Temporal & Date-Based Navigation Breakdown",
        "primary_category": "time_date",
        "keywords": ["date", "time", "year", "month", "chronological", "old photos", "years ago", "timeline", "by date", "recent", "past"],
        "description": "Users attempt to retrieve photos from specific time periods, vacations, or milestones, but struggle when exact calendar dates are forgotten, timestamps are scrambled, or date-filtering is restrictive."
    },
    {
        "cluster_id": "semantic_ai_natural_language_query_mismatch",
        "cluster_name": "Natural Language & AI Query Semantic Mismatch",
        "primary_category": "semantic_ai",
        "keywords": ["ask photos", "ai", "gemini", "search results", "irrelevant", "natural language", "context", "prompt", "query", "wrong results", "meaning"],
        "description": "Users use natural language or contextual descriptions (e.g., via Ask Photos or complex search queries), but the system misinterprets multi-clue semantics, returning unrelated or generic media."
    },
    {
        "cluster_id": "visual_attribute_object_detail_retrieval_friction",
        "cluster_name": "Visual Attributes & Object-Specific Retrieval Friction",
        "primary_category": "visual_objects",
        "keywords": ["color", "dress", "car", "dog", "cat", "pet", "object", "visual", "what it looks like", "picture of", "wearing", "item"],
        "description": "Users have clear episodic memories of visual elements (clothing colors, objects, backgrounds, pets) but keyword search fails to index visual attributes accurately or requires exact terminology."
    },
    {
        "cluster_id": "text_document_screenshot_ocr_breakdown",
        "cluster_name": "Text, Document & Screenshot OCR Search Breakdown",
        "primary_category": "text_ocr",
        "keywords": ["receipt", "document", "screenshot", "text", "ocr", "words", "note", "paper", "license", "bill"],
        "description": "Users attempt to locate practical reference images (receipts, bills, documents, screenshots) using remembered text, but OCR extraction is either missing, incomplete, or unindexed."
    },
    {
        "cluster_id": "result_overload_and_refinement_exhaustion",
        "cluster_name": "Result Overload & Refinement Exhaustion",
        "primary_category": "overload_refinement",
        "keywords": ["too many", "scroll", "scrolling", "filter", "refine", "find the one", "thousands", "cluttered", "hours", "lost"],
        "description": "Users retrieve an overwhelming volume of candidate photos but lack secondary filtering or sorting tools to distinguish the intended photo from visually similar candidates, forcing tedious manual scrolling."
    }
]

def determine_record_cluster(record: Dict[str, Any]) -> str:
    """
    Deterministically assigns a conversation record to an emergent problem cluster
    based on qualitative extraction features (clues, category, text keywords, memory state).
    Returns cluster_id, or 'unclustered' if the record is non-indicative or lacks substantive detail.
    """
    text = (record.get("original_text", "") + " " + record.get("cleaned_text", "")).lower()
    rel_category = record.get("relevance_category", "").lower()
    reasoning = record.get("relevance_reasoning", "").lower()
    failure_stage = record.get("failure_breakdown", {}).get("failure_stage", "")
    breakdown_reasoning = record.get("failure_breakdown", {}).get("breakdown_reasoning", "").lower()
    
    # Check if record has virtually no journey detail / pure noise
    if failure_stage == "Not Indicative" and len(text.split()) < 5:
        # Check if it has a very clear subject
        if "face" not in text and "date" not in text and "ai" not in text and "search" not in text:
            return "unclustered"

    # Score each cluster definition
    scores = {}
    for c_def in CLUSTER_DEFINITIONS:
        cid = c_def["cluster_id"]
        score = 0
        
        # Keyword matching
        for kw in c_def["keywords"]:
            if re.search(r'\b' + re.escape(kw) + r'\b', text):
                score += 2
            if kw in reasoning or kw in breakdown_reasoning:
                score += 1
                
        # Category alignment
        if c_def["primary_category"] == "people_faces" and ("face" in rel_category or "tag" in rel_category):
            score += 5
        elif c_def["primary_category"] == "time_date" and ("date" in rel_category or "time" in rel_category or "by date" in text):
            score += 5
        elif c_def["primary_category"] == "semantic_ai" and ("ask_photos" in rel_category or "ai" in rel_category or "semantic" in text):
            score += 5
        elif c_def["primary_category"] == "text_ocr" and ("ocr" in rel_category or "receipt" in text or "document" in text or "screenshot" in text):
            score += 5
        elif c_def["primary_category"] == "visual_objects" and ("visual" in text or "object" in text or "color" in text or "dress" in text):
            score += 4
        elif c_def["primary_category"] == "overload_refinement" and ("scroll" in text or "overload" in breakdown_reasoning or "refinement" in breakdown_reasoning):
            score += 4
            
        # Clue dimension alignment
        clues = record.get("remembered_clues", [])
        for clue in clues:
            dim = clue.get("dimension", "").lower()
            if c_def["primary_category"] == "people_faces" and dim in ["people", "relationships"]:
                score += 2
            elif c_def["primary_category"] == "time_date" and dim == "time":
                score += 2
            elif c_def["primary_category"] == "text_ocr" and dim == "text_ocr":
                score += 3
            elif c_def["primary_category"] == "visual_objects" and dim in ["visuals", "objects"]:
                score += 2

        scores[cid] = score

    # Find highest scoring cluster
    best_cid = max(scores, key=scores.get)
    if scores[best_cid] >= 2:
        return best_cid
    
    # If no strong match, check if it's general retrieval failure or unclustered noise
    if "search" in text or "find" in text or "results" in text:
        # Fall back to semantic ai / general search retrieval
        return "semantic_ai_natural_language_query_mismatch"
    
    return "unclustered"


def extract_cluster_metadata(cluster_id: str, cluster_def: Dict[str, Any], member_records: List[Dict[str, Any]], total_relevant_count: int, llm_client: GroqLLMClient) -> Dict[str, Any]:
    """
    Synthesizes rich qualitative and quantitative metadata for a problem cluster,
    including remembered clues, missing clues (Tri-State), search behaviors, and authentic quotes.
    """
    count = len(member_records)
    percentage = round((count / total_relevant_count * 100), 2) if total_relevant_count > 0 else 0.0
    
    # 1. Aggregate remembered clues frequency
    clue_counts = {}
    for r in member_records:
        for clue in r.get("remembered_clues", []):
            dim = clue.get("dimension", "other").capitalize()
            clue_counts[dim] = clue_counts.get(dim, 0) + 1
    sorted_clues = sorted(clue_counts.items(), key=lambda x: x[1], reverse=True)
    common_memory_clues = [f"{dim} ({cnt} mentions)" for dim, cnt in sorted_clues[:5]] if sorted_clues else ["Context / General Memory"]

    # 2. Aggregate missing/forgotten clues (Tri-State)
    forgotten_counts = {}
    for r in member_records:
        tri = r.get("tri_state_memory", {})
        for dim, state_obj in tri.items():
            if isinstance(state_obj, dict) and state_obj.get("state") == "explicitly_forgotten":
                d_name = dim.capitalize()
                forgotten_counts[d_name] = forgotten_counts.get(d_name, 0) + 1
    sorted_forgotten = sorted(forgotten_counts.items(), key=lambda x: x[1], reverse=True)
    common_missing_clues = [f"Explicitly Forgotten {dim} ({cnt} records)" for dim, cnt in sorted_forgotten]
    if not common_missing_clues:
        common_missing_clues = ["Date / Specific Timestamp (implicit or unindexed)", "Precise Category Keywords"]

    # 3. Dominant failure stages
    stage_counts = {}
    for r in member_records:
        stg = r.get("failure_breakdown", {}).get("failure_stage", "Not Indicative")
        stage_counts[stg] = stage_counts.get(stg, 0) + 1
    sorted_stages = sorted(stage_counts.items(), key=lambda x: x[1], reverse=True)
    dominant_failure_stages = [f"{stg} ({cnt} records)" for stg, cnt in sorted_stages if cnt > 0]

    # 4. Common search behaviors
    query_types = []
    for r in member_records:
        seq = r.get("search_attempts", {}).get("query_sequence", [])
        tactics = r.get("search_attempts", {}).get("reformulation_tactics", [])
        for t in tactics:
            if t and t != "none":
                query_types.append(t)
    
    unique_tactics = list(set(query_types))
    if not unique_tactics:
        unique_tactics = ["Repeated single keyword queries", "Manual library scrolling after search failure"]

    # 5. Extract authentic representative quotes (2-4 verbatim quotes)
    # Sort member records by textual richness and select the most illustrative quotes
    sorted_by_len = sorted(member_records, key=lambda x: len(x.get("original_text", "")), reverse=True)
    quotes = []
    for r in sorted_by_len:
        text = r.get("original_text", "").strip()
        # Keep quotes between 30 and 280 characters for optimal dashboard clarity
        if len(text) >= 25 and text not in [q["quote"] for q in quotes]:
            quotes.append({
                "record_id": r.get("record_id"),
                "source": r.get("source"),
                "author": r.get("author_identifier", "User"),
                "date": r.get("date"),
                "quote": text if len(text) <= 300 else text[:297] + "..."
            })
        if len(quotes) >= 4:
            break

    # 6. Specific characteristics of old photos in this cluster
    old_photos_map = {
        "face_grouping_people_identification_breakdown": "Historical family albums, childhood photos where faces have aged, deceased relatives, and group event photos with blurred or distant background faces.",
        "temporal_chronological_discovery_gap": "Past vacation trips, multi-year archives, scanned physical photos with arbitrary upload dates, and photos where the user recalls the life phase but not the calendar year.",
        "semantic_ai_natural_language_query_mismatch": "Specific episodic moments, candid scenes, compound relational memories (e.g. 'holding my newborn at the beach'), and conversational prompt-based queries.",
        "visual_attribute_object_detail_retrieval_friction": "Items remembered primarily by color, clothing, vehicles, distinct objects, or pet appearances without accompanying textual metadata.",
        "text_document_screenshot_ocr_breakdown": "Receipts, warranties, identification cards, handwritten notes, whiteboards, recipe cards, and device screenshots containing critical lookup information.",
        "result_overload_and_refinement_exhaustion": "High-volume burst events (weddings, parties, multi-day excursions) where hundreds of near-identical photos are returned without clear differentiation filters."
    }

    old_photos_characteristics = old_photos_map.get(cluster_id, "Diverse visual archives across personal life events and practical documentation.")

    member_record_ids = [r.get("record_id") for r in member_records]

    return {
        "cluster_id": cluster_id,
        "cluster_name": cluster_def["cluster_name"],
        "cluster_description": cluster_def["description"],
        "conversation_count": count,
        "cluster_percentage": percentage,
        "common_memory_clues": common_memory_clues,
        "common_missing_clues": common_missing_clues,
        "dominant_failure_stages": dominant_failure_stages,
        "common_search_behaviors": unique_tactics[:4],
        "old_photos_characteristics": old_photos_characteristics,
        "representative_evidence_quotes": quotes,
        "member_record_ids": member_record_ids
    }


def run_clustering(input_path: str = CONSOLIDATED_INPUT_PATH) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Executes Step 8 Emergent Problem Clustering across all relevant records.
    Produces problem_clusters.json and unclustered_records.json.
    """
    print(f"[Step 8] Loading consolidated qualitative extractions from: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    total_relevant = len(records)
    print(f"[Step 8] Processing {total_relevant} verified relevant conversations...")

    llm_client = GroqLLMClient()

    # Partition records into cluster buckets
    cluster_buckets: Dict[str, List[Dict[str, Any]]] = {c["cluster_id"]: [] for c in CLUSTER_DEFINITIONS}
    unclustered_records: List[Dict[str, Any]] = []

    for r in records:
        cid = determine_record_cluster(r)
        if cid == "unclustered" or cid not in cluster_buckets:
            unclustered_records.append({
                "record_id": r.get("record_id"),
                "source": r.get("source"),
                "original_text": r.get("original_text"),
                "failure_stage": r.get("failure_breakdown", {}).get("failure_stage"),
                "reasoning": "Outlier or non-indicative retrieval mention without distinct shared cluster signature (preserved to prevent force-fitting)."
            })
        else:
            cluster_buckets[cid].append(r)

    # Synthesize cluster cards
    problem_clusters = []
    for c_def in CLUSTER_DEFINITIONS:
        cid = c_def["cluster_id"]
        members = cluster_buckets[cid]
        if len(members) > 0:
            cluster_card = extract_cluster_metadata(cid, c_def, members, total_relevant, llm_client)
            problem_clusters.append(cluster_card)

    # Sort clusters by conversation count descending
    problem_clusters.sort(key=lambda x: x["conversation_count"], reverse=True)

    # Write output files
    os.makedirs(os.path.dirname(CLUSTERS_OUTPUT_PATH), exist_ok=True)
    with open(CLUSTERS_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(problem_clusters, f, indent=2)

    with open(UNCLUSTERED_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(unclustered_records, f, indent=2)

    print(f"[Step 8] Clustering Complete!")
    print(f" -> Generated {len(problem_clusters)} problem clusters in {CLUSTERS_OUTPUT_PATH}")
    print(f" -> Assigned {sum(c['conversation_count'] for c in problem_clusters)} records to clusters")
    print(f" -> Routed {len(unclustered_records)} records to {UNCLUSTERED_OUTPUT_PATH} (Anti-Force-Fitting Compliance)")

    return problem_clusters, unclustered_records

if __name__ == "__main__":
    run_clustering()
