import json
import requests
from collections import Counter
from dotenv import load_dotenv
import os

load_dotenv()

MISTRAL_URL = "http://localhost:11434/api/generate"
MISTRAL_MODEL = "mistral"

def load_trends():
    with open('trending_topics.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def find_overlapping_themes(trends):
    word_counts = Counter()
    for trend in trends:
        for word in trend.lower().split():
            word_counts[word] += 1

    common_keywords = [word for word, count in word_counts.items() if count >= 3]
    return common_keywords[:10]  # Top 10 repeated ideas

def ask_mistral_for_predictions(seeds):
    prompt = (
        f"Based on these rising trend terms: {', '.join(seeds)}, "
        f"what are likely to be the most searched topics over the next 7–14 days? "
        f"Think about global events, AI, business, tech, finance, and tools. "
        f"Give me a list of 5 predicted topics or product ideas."
    )

    payload = {
        "model": MISTRAL_MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(MISTRAL_URL, json=payload)
        result = response.json()
        return result.get("response", "").strip().split("\n")
    except Exception as e:
        print(f"❌ Error querying Mistral: {e}")
        return []

def save_forecast(forecast):
    with open("forecasted_trends.json", "w", encoding="utf-8") as f:
        json.dump(forecast, f, indent=4)
    print("📈 Forecast saved to forecasted_trends.json")

def main():
    print("🔮 [Market Radar] Analyzing rising topics...")
    trends = load_trends()
    overlapping = find_overlapping_themes(trends)
    print(f"💡 [Seed Ideas] {overlapping}")

    predictions = ask_mistral_for_predictions(overlapping)
    forecast = [p.lstrip("-•123. ").strip() for p in predictions if p.strip()]

    print("🔭 [Forecasted Trends]")
    for idea in forecast:
        print(f"   • {idea}")

    save_forecast(forecast)

if __name__ == "__main__":
    main()

