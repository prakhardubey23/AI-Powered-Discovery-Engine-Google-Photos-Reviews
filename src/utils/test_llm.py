import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
GROQ_API_KEY = os.environ.get("GROQ_API_KEY_1", "")

def test_models():
    client = Groq(api_key=GROQ_API_KEY)
    models = [m.id for m in client.models.list().data]
    print("Available models:", models)
    
    candidate_models = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b"]
    for model_name in candidate_models:
        if model_name in models:
            print(f"\nTesting model: {model_name}")
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant. Always output valid JSON."},
                        {"role": "user", "content": "Return a JSON object with key 'status' equal to 'connected' and 'model' equal to your model name."}
                    ],
                    response_format={"type": "json_object"},
                    max_tokens=100
                )
                print("Response:", response.choices[0].message.content)
                print("SUCCESS with", model_name)
                return model_name
            except Exception as e:
                print(f"Failed with {model_name}: {e}")
    return None

if __name__ == "__main__":
    best_model = test_models()
    print("\nBest working model:", best_model)
