import os
import json
import sqlite3
import hashlib

def check_cache():
    data_path = "data/03_filtered/relevant_conversations.json"
    cache_path = "data/.llm_cache.sqlite"
    
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    conn = sqlite3.connect(cache_path)
    cursor = conn.cursor()
    
    hits = 0
    missing = []
    
    for i, r in enumerate(data):
        rec_id = r["record_id"]
        # Check if record id exists in any prompt in llm_cache
        cursor.execute("SELECT response FROM llm_cache WHERE prompt LIKE ? LIMIT 1", (f"%{rec_id}%",))
        row = cursor.fetchone()
        if row:
            hits += 1
        else:
            missing.append((i, rec_id, r.get("source", "unknown"), (r.get("cleaned_text") or r.get("original_text", ""))[:40]))
            
    print(f"Total relevant records: {len(data)}")
    print(f"Direct cache matches by record_id: {hits} / {len(data)}")
    print(f"Missing count: {len(missing)}")
    if missing:
        print("\nMissing records to extract:")
        for idx, rid, src, txt in missing:
            print(f"  [{idx}] {rid} ({src}): {txt}")

if __name__ == "__main__":
    check_cache()
