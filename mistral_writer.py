import requests
import json

# Configure the local Mistral server (adjust if needed)
MISTRAL_API_URL = "http://localhost:11434/api/generate"

# Define the prompt you'd like Mistral to complete
prompt = "Write a premium product description for a digital AI investing toolkit targeting high-net-worth individuals."

# Build the JSON payload
payload = {
    "model": "mistral",
    "prompt": prompt,
    "stream": False
}

print("🧠 [Mistral] Sending prompt...")
try:
    response = requests.post(MISTRAL_URL, json=payload)
    response.raise_for_status()
    result = response.json()
    print("✅ [Mistral Response Received]")
    print("-" * 60)
    print(result.get("response", "[No response text found]"))
    print("-" * 60)
except requests.exceptions.RequestException as e:
    print(f"❌ [Error] Could not connect to Mistral server: {e}")
except json.JSONDecodeError:
    print("❌ [Error] Invalid JSON response from Mistral.")

