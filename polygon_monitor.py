import os
import requests
from datetime import datetime

# Load API keys from environment variables
POLYGON_API_KEY = os.getenv('POLYGON_API_KEY')
SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY')
SHOPIFY_PASSWORD = os.getenv('SHOPIFY_PASSWORD')
SHOPIFY_STORE_NAME = os.getenv('SHOPIFY_STORE_NAME')

# Define the list of stock symbols to monitor
STOCK_SYMBOLS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'SHOP']

def fetch_stock_data(symbol):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/prev?adjusted=true&apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]
    return None

def create_shopify_product(symbol, price_change):
    product_data = {
        "product": {
            "title": f"{symbol} Stock Alert Product",
            "body_html": f"<strong>{symbol}</strong> stock has changed by {price_change}%.",
            "vendor": "IdeaReactor",
            "product_type": "Stock Alert",
            "tags": [symbol, "Stock Alert"]
        }
    }
    url = f"https://{SHOPIFY_API_KEY}:{SHOPIFY_PASSWORD}@{SHOPIFY_STORE_NAME}.myshopify.com/admin/api/2021-04/products.json"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=product_data, headers=headers)
    if response.status_code == 201:
        print(f"Product for {symbol} created successfully.")
    else:
        print(f"Failed to create product for {symbol}. Status Code: {response.status_code}")

def monitor_stocks():
    for symbol in STOCK_SYMBOLS:
        data = fetch_stock_data(symbol)
        if data:
            open_price = data['o']
            close_price = data['c']
            price_change = ((close_price - open_price) / open_price) * 100
            print(f"{symbol}: {price_change:.2f}% change.")
            # Trigger product creation if price drops more than 2%
            if price_change <= -2:
                create_shopify_product(symbol, round(price_change, 2))

if __name__ == "__main__":
    monitor_stocks()
