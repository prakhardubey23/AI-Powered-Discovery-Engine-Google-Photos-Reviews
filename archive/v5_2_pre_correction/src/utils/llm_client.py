import os
import json
import sqlite3
import hashlib
import time
import sys
import re
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from groq import Groq

DEFAULT_GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
DEFAULT_GROQ_KEYS = [
    k for k in [
        os.environ.get("GROQ_API_KEY_1", ""),
        os.environ.get("GROQ_API_KEY_2", "")
    ] if k
]
CACHE_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", ".llm_cache.sqlite")

class GroqLLMClient:
    """Universal LLM Client backed by Gemini 3.5 Flash Lite REST API with SQLite caching."""
    def __init__(self, api_keys: Optional[List[str]] = None, models: Optional[List[str]] = None, cache_path: str = CACHE_DB_PATH):
        self.gemini_key = DEFAULT_GEMINI_KEY
        self.groq_keys = api_keys if api_keys else list(DEFAULT_GROQ_KEYS)
        self.groq_clients = [Groq(api_key=k) for k in self.groq_keys]
        self.groq_models = models if models else ["qwen/qwen3.8-27b"]

        self.cache_path = os.path.abspath(cache_path)
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        self._init_cache()
        self.total_tokens_used = 0
        self.total_calls_made = 0
        self.cache_hits = 0

    def _init_cache(self):
        conn = sqlite3.connect(self.cache_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS llm_cache (
                prompt_hash TEXT PRIMARY KEY,
                model TEXT,
                prompt TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def _get_hash(self, prompt: str) -> str:
        return hashlib.sha256(prompt.encode('utf-8')).hexdigest()

    def _call_gemini_rest(self, prompt: str, system_prompt: str) -> Dict[str, Any]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={self.gemini_key}"
        full_text = f"{system_prompt}\n\n{prompt}"
        payload = {
            "contents": [{"parts": [{"text": full_text}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.1
            }
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            content_str = body["candidates"][0]["content"]["parts"][0]["text"].strip()
            return json.loads(content_str)

    def call_json(self, prompt: str, system_prompt: str = "You are an AI qualitative research discovery analyst. Always respond in valid JSON format.") -> Dict[str, Any]:
        prompt_hash = self._get_hash(prompt)
        
        # Check SQLite Cache first
        try:
            with sqlite3.connect(self.cache_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT response FROM llm_cache WHERE prompt_hash = ? OR prompt = ? LIMIT 1", (prompt_hash, prompt))
                row = cursor.fetchone()
                if row:
                    self.cache_hits += 1
                    try:
                        return json.loads(row[0])
                    except Exception:
                        pass
        except Exception:
            pass

        # 1. Gemini REST API with retry
        for attempt in range(10):
            try:
                parsed = self._call_gemini_rest(prompt, system_prompt)
                self.total_calls_made += 1
                
                # Cache response
                try:
                    with sqlite3.connect(self.cache_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT OR REPLACE INTO llm_cache (prompt_hash, model, prompt, response)
                            VALUES (?, ?, ?, ?)
                        """, (prompt_hash, "gemini-3.5-flash-lite", prompt, json.dumps(parsed, ensure_ascii=False)))
                        conn.commit()
                except Exception:
                    pass

                return parsed
            except Exception as e:
                err_str = str(e)
                if "429" in err_str:
                    time.sleep(4.0)
                else:
                    time.sleep(1.5)

        # 2. Fallback to Groq
        max_retries = 8
        for attempt in range(max_retries):
            key_index = (self.total_calls_made + attempt) % len(self.groq_clients)
            client = self.groq_clients[key_index]
            model = self.groq_models[0]
            
            try:
                time.sleep(1.0)
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1,
                    max_tokens=400
                )
                content = response.choices[0].message.content
                self.total_calls_made += 1
                parsed = json.loads(content)
                
                # Cache response
                try:
                    with sqlite3.connect(self.cache_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT OR REPLACE INTO llm_cache (prompt_hash, model, prompt, response)
                            VALUES (?, ?, ?, ?)
                        """, (prompt_hash, model, prompt, json.dumps(parsed, ensure_ascii=False)))
                        conn.commit()
                except Exception:
                    pass
                
                return parsed
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "rate limit" in err_str.lower():
                    time.sleep(10.0)
                else:
                    time.sleep(2.0)
        
        raise RuntimeError("Failed to get valid JSON response from LLM after all attempts.")
