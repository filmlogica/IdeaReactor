import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

SHOP_NAME = os.getenv("SHOPIFY_STORE")
API_KEY = os.getenv("SHOPIFY_API_KEY")
PASSWORD = os.getenv("SHOPIFY_PASSWORD")

BASE_URL = f"https://{API_KEY}:{PASSWORD}@{SHOP_NAME}.myshopify.com/admin/api/2023-10"

def upload_to_shopify(product_name, description, price, zip_path):
    print(f"🛒 Uploading {product_name} to Shopify...")

    product_data = {
        "product": {
            "title": product_name,
            "body_html": description,
            "vendor": "IdeaReactor",
            "product_type": "Digital",
            "status": "active",
            "variants": [{"price": price}]
        }
    }

    product_resp = requests.post(
        f"{BASE_URL}/products.json",
        json=product_data
    )

    if product_resp.status_code != 201:
        print("❌ Failed to create product:", product_resp.text)
        return

    product = product_resp.json()["product"]
    product_id = product["id"]
    print(f"✅ Product created with ID {product_id}")

    # Attach ZIP as file (Digital Downloads app handles the link after purchase)
    print("📦 Upload the ZIP manually in the Digital Downloads app")

if __name__ == "__main__":
    from trend import get_latest_trend
    trend = get_latest_trend()
    name = trend["topic"].replace(" ", "_")
    description = trend["reason"]
    price = trend.get("price", "14.99")
    zip_path = f"products/{name}/{name}.zip"

    upload_to_shopify(name, description, price, zip_path)

