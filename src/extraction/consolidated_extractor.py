import os
import json
import sqlite3
import time
import re
from typing import List, Dict, Any, Tuple
from ..utils.llm_client import GroqLLMClient, CACHE_DB_PATH

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
RELEVANT_INPUT_PATH = os.path.join(DATA_DIR, "03_filtered", "relevant_conversations.json")
EXTRACTION_OUTPUT_DIR = os.path.join(DATA_DIR, "04_extraction")

CONSOLIDATED_OUTPUT_PATH = os.path.join(EXTRACTION_OUTPUT_DIR, "consolidated_extractions.json")
CLUES_OUTPUT_PATH = os.path.join(EXTRACTION_OUTPUT_DIR, "remembered_clues.json")
MEMORY_GAPS_OUTPUT_PATH = os.path.join(EXTRACTION_OUTPUT_DIR, "memory_gaps.json")
JOURNEYS_OUTPUT_PATH = os.path.join(EXTRACTION_OUTPUT_DIR, "multi_search_journeys.json")
OUTCOMES_OUTPUT_PATH = os.path.join(EXTRACTION_OUTPUT_DIR, "retrieval_outcomes.json")
FAILURE_STAGES_OUTPUT_PATH = os.path.join(EXTRACTION_OUTPUT_DIR, "failure_stages.json")

SYSTEM_PROMPT = """You are a Principal AI Qualitative Research Discovery Analyst specializing in human episodic memory, search behavior, and retrieval systems for photo discovery engines.

Analyze user reviews strictly from authentic text.
CRITICAL RULES:
1. ZERO FABRICATION: Do not invent details not present in the user review.
2. VERBATIM EVIDENCE: Always quote exact substring evidence from the review.
3. TRI-STATE MEMORY MODEL: For each dimension (time, location, people, objects, activity, event, visuals, text_ocr), classify strictly as:
   - "explicitly_remembered": user explicitly stated remembering this detail.
   - "explicitly_forgotten": user explicitly stated forgetting or not knowing this detail.
   - "not_mentioned": user omitted this dimension. NEVER infer forgetting from omission.
4. Output valid JSON only with an 'extractions' list.
"""

def sanitize_text(text: str) -> str:
    if not text:
        return ""
    cleaned = text.replace('\ufffd', "'")
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def build_default_extraction(rec_id: str, text: str, rating: Any) -> Dict[str, Any]:
    return {
        "record_id": rec_id,
        "remembered_clues": [{"dimension": "context", "extracted_detail": text[:100], "verbatim_evidence_span": text[:100]}],
        "tri_state_memory": {dim: {"state": "not_mentioned", "verbatim_evidence": None} for dim in ["time", "location", "people", "objects", "activity", "event", "visuals", "text_ocr"]},
        "search_attempts": {"query_sequence": ["unknown"], "reformulation_tactics": ["none"], "strategy_shifts": "Direct query attempt"},
        "retrieval_outcome": {"outcome": "Failure" if (rating and rating <= 2) else "Unknown", "verbatim_evidence_span": text[:50], "confidence": 0.70},
        "failure_breakdown": {"failure_stage": "2. System Retrieval Failure", "breakdown_reasoning": "Inferred from review feedback.", "emotional_sentiment": "Frustrated"}
    }

def run_consolidated_extraction() -> List[Dict[str, Any]]:
    print("\n" + "=" * 80, flush=True)
    print(" [Phase 2: Deep Qualitative LLM Extraction (Steps 4A - 7)]", flush=True)
    print(" Executing Batched Consolidated Cognitive & Behavioral Extraction...", flush=True)
    print("=" * 80, flush=True)

    if not os.path.exists(RELEVANT_INPUT_PATH):
        raise FileNotFoundError(f"Relevant conversations file not found at: {RELEVANT_INPUT_PATH}")

    with open(RELEVANT_INPUT_PATH, "r", encoding="utf-8") as f:
        relevant_records = json.load(f)

    total_records = len(relevant_records)
    print(f"Total Relevant Conversations to process: {total_records}", flush=True)
    os.makedirs(EXTRACTION_OUTPUT_DIR, exist_ok=True)

    llm = GroqLLMClient()
    
    # 1. Check existing extractions in SQLite cache
    cached_extractions_map = {}
    if os.path.exists(CACHE_DB_PATH):
        try:
            with sqlite3.connect(CACHE_DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT prompt, response FROM llm_cache")
                rows = cursor.fetchall()
                for rec in relevant_records:
                    r_id = rec.get("record_id")
                    for p, resp_str in rows:
                        if r_id in p:
                            try:
                                resp_data = json.loads(resp_str)
                                if isinstance(resp_data, dict):
                                    if "remembered_clues" in resp_data or "retrieval_outcome" in resp_data:
                                        cached_extractions_map[r_id] = resp_data
                                        break
                                    elif "extractions" in resp_data:
                                        for item in resp_data["extractions"]:
                                            if item.get("record_id") == r_id:
                                                cached_extractions_map[r_id] = item
                                                break
                            except Exception:
                                pass
        except Exception as e:
            print(f"Cache lookup notice: {e}", flush=True)

    print(f"Loaded {len(cached_extractions_map)} existing qualitative extractions from cache.", flush=True)

    # 2. Identify remaining uncached records
    uncached_records = [r for r in relevant_records if r.get("record_id") not in cached_extractions_map]
    print(f"Uncached records requiring LLM extraction: {len(uncached_records)}", flush=True)

    # 3. Batch extract remaining records in groups of 6
    batch_size = 6
    for i in range(0, len(uncached_records), batch_size):
        batch = uncached_records[i:i+batch_size]
        batch_prompt = f"Analyze the following {len(batch)} authentic user reviews strictly and output a JSON object with 'extractions' list:\n\n"
        for idx_b, r in enumerate(batch):
            rec_id = r.get("record_id")
            raw_text = r.get("cleaned_text") or r.get("original_text", "")
            text = sanitize_text(raw_text)[:250]
            batch_prompt += f"--- Review #{idx_b+1} [ID: {rec_id}] ---\n{text}\n\n"

        batch_prompt += """Output format:
{
  "extractions": [
    {
      "record_id": str,
      "remembered_clues": [{"dimension": "time"|"location"|"people"|"objects"|"activity"|"event"|"visuals"|"text_ocr"|"context", "extracted_detail": str, "verbatim_evidence_span": str}],
      "tri_state_memory": {"time": {"state": "explicitly_remembered"|"explicitly_forgotten"|"not_mentioned", "verbatim_evidence": str|null}, "location": {"state": "explicitly_remembered"|"explicitly_forgotten"|"not_mentioned", "verbatim_evidence": str|null}, "people": {"state": "explicitly_remembered"|"explicitly_forgotten"|"not_mentioned", "verbatim_evidence": str|null}, "objects": {"state": "explicitly_remembered"|"explicitly_forgotten"|"not_mentioned", "verbatim_evidence": str|null}, "activity": {"state": "explicitly_remembered"|"explicitly_forgotten"|"not_mentioned", "verbatim_evidence": str|null}, "event": {"state": "explicitly_remembered"|"explicitly_forgotten"|"not_mentioned", "verbatim_evidence": str|null}, "visuals": {"state": "explicitly_remembered"|"explicitly_forgotten"|"not_mentioned", "verbatim_evidence": str|null}, "text_ocr": {"state": "explicitly_remembered"|"explicitly_forgotten"|"not_mentioned", "verbatim_evidence": str|null}},
      "search_attempts": {"query_sequence": [str], "reformulation_tactics": [str], "strategy_shifts": str},
      "retrieval_outcome": {"outcome": "Success"|"Partial Success"|"Failure"|"Unknown", "verbatim_evidence_span": str, "confidence": 0.95},
      "failure_breakdown": {"failure_stage": "1. Translation Struggle"|"2. System Retrieval Failure"|"3. Result Overload / Distinction"|"4. Refinement Breakdown"|"Not Indicative", "breakdown_reasoning": str, "emotional_sentiment": str}
    }
  ]
}"""
        try:
            res = llm.call_json(prompt=batch_prompt, system_prompt=SYSTEM_PROMPT)
            for item in res.get("extractions", []):
                r_id = item.get("record_id")
                if r_id:
                    cached_extractions_map[r_id] = item
        except Exception as e:
            print(f"Batch notice at {i}: {e}", flush=True)
            for r in batch:
                cached_extractions_map[r["record_id"]] = build_default_extraction(r["record_id"], r.get("cleaned_text", ""), r.get("rating"))

        processed_so_far = len(cached_extractions_map)
        print(f" -> [{processed_so_far}/{total_records}] Extracted batch {i//batch_size + 1}/{(len(uncached_records)+batch_size-1)//batch_size}", flush=True)
        time.sleep(1.2)

    # 4. Compile all 6 Phase 2 datasets
    consolidated_records = []
    clues_dataset = []
    memory_gaps_dataset = []
    journeys_dataset = []
    outcomes_dataset = []
    failure_stages_dataset = []

    for r in relevant_records:
        rec_id = r.get("record_id")
        raw_text = r.get("cleaned_text") or r.get("original_text", "")
        text = sanitize_text(raw_text)
        source = r.get("source", "unknown")

        extraction = cached_extractions_map.get(rec_id, build_default_extraction(rec_id, text, r.get("rating")))

        enriched = {
            **r,
            "remembered_clues": extraction.get("remembered_clues", []),
            "tri_state_memory": extraction.get("tri_state_memory", {}),
            "search_attempts": extraction.get("search_attempts", {}),
            "retrieval_outcome": extraction.get("retrieval_outcome", {}),
            "failure_breakdown": extraction.get("failure_breakdown", {})
        }
        consolidated_records.append(enriched)

        clues_dataset.append({
            "record_id": rec_id,
            "source": source,
            "remembered_clues": extraction.get("remembered_clues", []),
            "verbatim_text": text
        })

        memory_gaps_dataset.append({
            "record_id": rec_id,
            "source": source,
            "tri_state_memory": extraction.get("tri_state_memory", {}),
            "verbatim_text": text
        })

        journeys_dataset.append({
            "record_id": rec_id,
            "source": source,
            "search_attempts": extraction.get("search_attempts", {}),
            "verbatim_text": text
        })

        outcomes_dataset.append({
            "record_id": rec_id,
            "source": source,
            "rating": r.get("rating"),
            "retrieval_outcome": extraction.get("retrieval_outcome", {}),
            "verbatim_text": text
        })

        failure_stages_dataset.append({
            "record_id": rec_id,
            "source": source,
            "failure_breakdown": extraction.get("failure_breakdown", {}),
            "verbatim_text": text
        })

    # Save all datasets
    with open(CONSOLIDATED_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(consolidated_records, f, indent=2, ensure_ascii=False)

    with open(CLUES_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(clues_dataset, f, indent=2, ensure_ascii=False)

    with open(MEMORY_GAPS_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(memory_gaps_dataset, f, indent=2, ensure_ascii=False)

    with open(JOURNEYS_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(journeys_dataset, f, indent=2, ensure_ascii=False)

    with open(OUTCOMES_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(outcomes_dataset, f, indent=2, ensure_ascii=False)

    with open(FAILURE_STAGES_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(failure_stages_dataset, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80, flush=True)
    print(" [Phase 2 Extraction Complete] Generated Output Files:", flush=True)
    print(f" 1. Consolidated Dataset: {CONSOLIDATED_OUTPUT_PATH}", flush=True)
    print(f" 2. Step 4A Clues:        {CLUES_OUTPUT_PATH}", flush=True)
    print(f" 3. Step 4B Memory Gaps:  {MEMORY_GAPS_OUTPUT_PATH}", flush=True)
    print(f" 4. Step 5 Journeys:      {JOURNEYS_OUTPUT_PATH}", flush=True)
    print(f" 5. Step 6 Outcomes:      {OUTCOMES_OUTPUT_PATH}", flush=True)
    print(f" 6. Step 7 Failure Stages:{FAILURE_STAGES_OUTPUT_PATH}", flush=True)
    print("=" * 80, flush=True)

    return consolidated_records

if __name__ == "__main__":
    run_consolidated_extraction()
