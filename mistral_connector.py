import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MISTRAL_API_URL = os.getenv("MISTRAL_API_URL")

def generate_with_mistral(prompt, temperature=0.7, max_tokens=300):
    if not MISTRAL_API_URL:
        raise ValueError("MISTRAL_API_URL not set in .env file")

    payload = {
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(f"{MISTRAL_API_URL}/v1/chat/completions", json=payload)
        response.raise_for_status()
        return response.json().get("completion", "").strip()
    except requests.exceptions.RequestException as e:
        print(f"❌ Mistral API request failed: {e}")
        return None
