import requests
import os
import json
from datetime import datetime

# Load the API key from .env (set this as POLYGON_API_KEY in your GitHub/Render secrets)
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

def get_movers(limit=5):
    print("📈 [Polygon Scraper] Fetching market movers...")

    url = f"https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers?apiKey={POLYGON_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        tickers = data.get("tickers", [])
        top_movers = sorted(tickers, key=lambda x: abs(x["day"]["change"]), reverse=True)[:limit]

        for t in top_movers:
            print(f"🔍 {t['ticker']}: {t['day']['change']} ({t['day']['percent_change']}%)")

        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "top_movers": top_movers
        }

        with open("polygon_data.json", "w") as f:
            json.dump(result, f, indent=4)

        print("✅ [Polygon Scraper] Data saved to polygon_data.json")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    get_movers()
