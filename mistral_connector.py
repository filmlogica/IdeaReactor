import requests
import os

MISTRAL_URL = os.getenv("MISTRAL_URL", "https://mistral-api-server.onrender.com/generate")

def ask_mistral(prompt):
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(MISTRAL_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["response"]
