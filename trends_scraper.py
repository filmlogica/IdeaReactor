import json, os, time
import requests
from bs4 import BeautifulSoup
from mistral_connector import generate_with_mistral
from dotenv import load_dotenv

load_dotenv()

def fetch_google_trends():
    url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    return [item.title.text for item in soup.find_all("item")]

def fetch_amazon_best_sellers():
    url = "https://www.amazon.com/Best-Sellers/zgbs"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return [tag.text.strip() for tag in soup.select("div.p13n-sc-truncate-desktop-type2")][:10]

def fetch_techcrunch_rss():
    url = "https://techcrunch.com/tag/rss/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    return [item.title.text for item in soup.find_all("item")]

def fetch_producthunt_trends():
    # Placeholder
    return ["AI meeting tools", "no-code GPT apps", "autonomous agents"]

def gather_trends():
    print("📊 [Trend Scraper] Gathering global trends...")

    sources = {
        "Google Trends": fetch_google_trends(),
        "Amazon Best Sellers": fetch_amazon_best_sellers(),
        "TechCrunch": fetch_techcrunch_rss(),
        "ProductHunt": fetch_producthunt_trends()
    }

    all_trends = []
    for name, trends in sources.items():
        print(f"🔍 {name}: {len(trends)} items found")
        all_trends.extend(trends)

    return all_trends

def find_hot_trend(trends):
    if top_trend is not None:
        top_trend = top_trend.strip()
    else:
        top_trend = "Default Trend"
    prompt = f"From this list of trends, which one represents the best opportunity for a high-priced digital product targeting wealthy professionals? Return only one:\n\n{trends}"
    response = generate_with_mistral(prompt)
    return response.strip()

def main():
    print("📈 [Trend Scanner] Analyzing the market...")
    trends = gather_trends()
    time.sleep(1)
    top_trend = find_hot_trend(trends)
    data = {
        "top_trend": top_trend,
        "all_trends": trends
    }

    with open("trend.json", "w") as f:
        json.dump(data, f, indent=4)

    print(f"\n🔥 [Top Global Trend Identified]\n   ↳ {top_trend}\n✅ [Saved] trend.json updated.")

if __name__ == "__main__":
    main()
