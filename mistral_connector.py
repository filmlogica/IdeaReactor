# mistral_connector.py
import requests
import os

MISTRAL_URL = f"http://localhost:{os.getenv('PORT', '11434')}/api/generate"
MODEL = os.getenv("MISTRAL_MODEL", "mistral")
OLLAMA_PATH = os.getenv("OLLAMA_PATH", "ollama")

def generate_from_mistral(prompt):
    print(f"🧠 [Mistral] Sending prompt to model '{MODEL}':\n{prompt}\n")

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(MISTRAL_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        print(f"🧠 [Mistral] Response received.")
        return result.get("response", "❌ No response from Mistral.")
    except requests.RequestException as e:
        print(f"❌ [Mistral] Connection failed: {e}")
        return "❌ Mistral API unreachable."
