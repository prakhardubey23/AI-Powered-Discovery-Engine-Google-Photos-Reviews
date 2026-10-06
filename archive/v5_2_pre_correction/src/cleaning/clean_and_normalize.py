import os
import json
import re
import html
import hashlib
from typing import List, Dict, Any

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
RAW_INPUT_PATH = os.path.join(DATA_DIR, "01_raw", "raw_conversations.json")
NORMALIZED_OUTPUT_PATH = os.path.join(DATA_DIR, "02_normalized", "normalized_conversations.json")

# Spam / bot indicators
SPAM_PATTERNS = [
    r'https?://(?:t\.me|wa\.me|bit\.ly|tinyurl)',
    r'\b(?:free followers|crypto|whatsapp me|hacked account recovery|call this number)\b',
    r'\b(?:contact \+?\d{10,})\b'
]

def clean_text(raw_text: str) -> str:
    if not raw_text:
        return ""
    # Unescape HTML entities
    text = html.unescape(raw_text)
    # Remove control characters except newlines/tabs
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    # Normalize multiple whitespace characters
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def calculate_spam_score(text: str) -> float:
    text_lower = text.lower()
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, text_lower):
            return 1.0
    if len(text.strip()) < 3:
        return 0.9
    return 0.0

def run_cleaning_and_normalization() -> List[Dict[str, Any]]:
    print("\n[Step 2: Cleaning & Normalisation] Processing raw conversations...")
    if not os.path.exists(RAW_INPUT_PATH):
        raise FileNotFoundError(f"Raw input file not found at: {RAW_INPUT_PATH}")
        
    with open(RAW_INPUT_PATH, "r", encoding="utf-8") as f:
        raw_records = json.load(f)
        
    normalized_records = []
    seen_hashes = set()
    duplicates_count = 0
    spam_count = 0
    
    for r in raw_records:
        original = r.get("original_text", "")
        cleaned = clean_text(original)
        
        # Skip empty
        if not cleaned:
            continue
            
        # Check spam
        spam_score = calculate_spam_score(cleaned)
        if spam_score >= 0.8:
            spam_count += 1
            continue
            
        # Deduplication using normalized content hash
        content_hash = hashlib.sha256(cleaned.lower().encode('utf-8')).hexdigest()
        if content_hash in seen_hashes:
            duplicates_count += 1
            continue
        seen_hashes.add(content_hash)
        
        normalized_record = {
            "record_id": r.get("record_id"),
            "source": r.get("source"),
            "source_type": r.get("source_type"),
            "source_url": r.get("source_url"),
            "source_id": r.get("source_id"),
            "date": r.get("date"),
            "author_identifier": r.get("author_identifier"),
            "cleaned_text": cleaned,
            "original_text": original,
            "rating": r.get("rating"),
            "language": r.get("language", "en"),
            "collection_timestamp": r.get("collection_timestamp"),
            "is_duplicate": False,
            "spam_score": spam_score,
            "provenance_status": r.get("provenance_status", "Verified Genuine")
        }
        normalized_records.append(normalized_record)
        
    os.makedirs(os.path.dirname(NORMALIZED_OUTPUT_PATH), exist_ok=True)
    with open(NORMALIZED_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(normalized_records, f, indent=2, ensure_ascii=False)
        
    print(f" -> Raw input records: {len(raw_records)}")
    print(f" -> Duplicates removed: {duplicates_count}")
    print(f" -> Spam/malformed filtered: {spam_count}")
    print(f" -> Normalized canonical records output: {len(normalized_records)}")
    print(f"Saved normalized records to: {NORMALIZED_OUTPUT_PATH}")
    return normalized_records

if __name__ == "__main__":
    run_cleaning_and_normalization()
