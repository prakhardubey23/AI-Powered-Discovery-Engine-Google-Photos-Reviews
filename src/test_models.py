import os
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
client = Groq(api_key=os.environ.get("GROQ_API_KEY_1", ""))

system_prompt = "You are a qualitative research analyst. Always respond in valid JSON format only."
user_prompt = """Review: "I tried searching for my wedding photos from 2022 in Italy, but it only shows pictures of my dog."

Output strictly JSON:
{
  "remembered_clues": [{"dimension": "event", "extracted_detail": "wedding", "verbatim_evidence_span": "wedding photos"}, {"dimension": "time", "extracted_detail": "2022", "verbatim_evidence_span": "2022"}, {"dimension": "location", "extracted_detail": "Italy", "verbatim_evidence_span": "Italy"}],
  "tri_state_memory": {
    "time": {"state": "explicitly_remembered", "verbatim_evidence": "2022"},
    "location": {"state": "explicitly_remembered", "verbatim_evidence": "Italy"},
    "people": {"state": "not_mentioned", "verbatim_evidence": null},
    "objects": {"state": "not_mentioned", "verbatim_evidence": null},
    "activity": {"state": "not_mentioned", "verbatim_evidence": null},
    "event": {"state": "explicitly_remembered", "verbatim_evidence": "wedding"},
    "visuals": {"state": "not_mentioned", "verbatim_evidence": null},
    "text_ocr": {"state": "not_mentioned", "verbatim_evidence": null}
  },
  "search_attempts": {
    "query_sequence": ["wedding photos 2022 Italy"],
    "reformulation_tactics": ["none"],
    "strategy_shifts": "Direct query"
  },
  "retrieval_outcome": {
    "outcome": "Failure",
    "verbatim_evidence_span": "only shows pictures of my dog",
    "confidence": 0.95
  },
  "failure_breakdown": {
    "failure_stage": "2. System Retrieval Failure",
    "breakdown_reasoning": "Wrong image returned instead of target event.",
    "emotional_sentiment": "Frustrated"
  }
}"""

for m in ["qwen/qwen3.8-27b", "openai/gpt-oss-20b"]:
    print(f"\n--- Testing full prompt with {m} ---")
    try:
        r = client.chat.completions.create(
            model=m,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=350
        )
        content = r.choices[0].message.content
        parsed = json.loads(content)
        print("SUCCESS! Clues extracted:", len(parsed.get("remembered_clues", [])))
        print("Retrieval Outcome:", parsed.get("retrieval_outcome", {}).get("outcome"))
    except Exception as e:
        print("FAILED:", e)
