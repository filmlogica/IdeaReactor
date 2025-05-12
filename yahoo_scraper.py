import requests
from bs4 import BeautifulSoup
import json
import datetime

YAHOO_LOSERS_URL = "https://finance.yahoo.com/losers"

def scrape_top_losers(limit=5):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(YAHOO_LOSERS_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    rows = table.find_all("tr")[1:]  # Skip header

    scraped_data = []
    for row in rows[:limit]:
        cols = row.find_all("td")
        if len(cols) < 6:
            continue
        symbol = cols[0].text.strip()
        name = cols[1].text.strip()
        price = cols[2].text.strip()
        change = cols[4].text.strip()
        percent_change = cols[5].text.strip()

        data = {
            "symbol": symbol,
            "name": name,
            "price": price,
            "change": change,
            "percent_change": percent_change,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        scraped_data.append(data)

    print("🔍 [Yahoo Finance] Top Stock Losers Detected:")
    for d in scraped_data:
        print(f"- {d['name']} ({d['symbol']}): {d['percent_change']} drop")

    return scraped_data


def save_trending_companies(data, filename="yahoo_trends.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ [Yahoo Scraper] Saved data to {filename}")


if __name__ == "__main__":
    companies = scrape_top_losers()
    save_trending_companies(companies)
