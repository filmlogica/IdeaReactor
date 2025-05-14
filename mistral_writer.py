import requests
import json
import os
import sys

# Load URL from env or use default Render server
MISTRAL_API_URL = os.getenv("MISTRAL_API_URL", "https://mistral-api-server-p6ho.onrender.com/api/generate")

def generate_description(topic, product_name):
    prompt = (
        f"Write a premium, SEO-optimized product description for a digital product called '{product_name}' "
        f"based on the trending topic: {topic}. Target tech-savvy buyers interested in automation and AI."
    )

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    print("🧠 [Mistral] Sending prompt...")
    try:
        response = requests.post(MISTRAL_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        description = result.get("response", "[No response]")
        print("✅ [Mistral Response Received]")
        print(description)

        # Save description to product file
        os.makedirs("products", exist_ok=True)
        filepath = f"products/{product_name}.json"
        if os.path.exists(filepath):
            with open(filepath, "r+") as f:
                data = json.load(f)
                data["description"] = description
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
        else:
            with open(filepath, "w") as f:
                json.dump({"title": product_name, "description": description}, f, indent=2)

    except requests.exceptions.RequestException as e:
        print(f"❌ [Error] Could not connect to Mistral server: {e}")
    except json.JSONDecodeError:
        print("❌ [Error] Invalid JSON response from Mistral.")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        generate_description(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python mistral_writer.py <topic> <product_name>")
