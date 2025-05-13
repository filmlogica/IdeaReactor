import os
import requests
import feedparser
from mistral_connector import generate_with_mistral

def fetch_google_trends():
    print("🔍 Google Trends: Checking RSS feed...")
    url = 'https://trends.google.com/trends/trendingsearches/daily/rss?geo=US'
    feed = feedparser.parse(url)
    return [entry.title for entry in feed.entries]

def fetch_amazon_best_sellers():
    print("🔍 Amazon Best Sellers: Checking page...")
    return []  # Placeholder for future scraping logic

def fetch_techcrunch():
    print("🔍 TechCrunch: Checking RSS feed...")
    url = 'https://techcrunch.com/tag/rss/'
    feed = feedparser.parse(url)
    return [entry.title for entry in feed.entries]

def fetch_producthunt():
    print("🔍 ProductHunt: Checking RSS feed...")
    url = 'https://www.producthunt.com/feed'
    feed = feedparser.parse(url)
    return [entry.title for entry in feed.entries]

def gather_all_trends():
    return (
        fetch_google_trends() +
        fetch_amazon_best_sellers() +
        fetch_techcrunch() +
        fetch_producthunt()
    )

def find_hot_trend(trends):
    prompt = f"From this list of trends, which one represents the best opportunity for a high-priced digital product targeting wealthy professionals? Return only one:\n\n{trends}"
    response = generate_with_mistral(prompt)

    if response:
        return response.strip()
    else:
        print("⚠️ Mistral API returned no result. Using fallback trend.")
        return "Premium Financial Tools"

def main():
    print("📈 [Trend Scanner] Analyzing the market...")
    print("📊 [Trend Scraper] Gathering global trends...")
    trends = gather_all_trends()
    print(f"🌍 Total trends gathered: {len(trends)}")

    top_trend = find_hot_trend(trends)

    with open("trend.json", "w") as f:
        f.write(f'{{"top_trend": "{top_trend}"}}')
    print(f"🔥 Top trend identified and saved: {top_trend}")

if __name__ == "__main__":
    main()
