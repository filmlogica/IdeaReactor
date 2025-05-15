import os
import json
import requests
import certifi
from datetime import datetime

# Load from environment
SHOP_NAME = os.getenv("SHOPIFY_STORE")
API_KEY = os.getenv("SHOPIFY_API_KEY")
PASSWORD = os.getenv("SHOPIFY_PASSWORD")
BASE_URL = f"https://{API_KEY}:{PASSWORD}@{SHOP_NAME}/admin/api/2023-10"

LOG_PATH = "logs/shopify_upload.txt"

def get_latest_product():
    products_dir = "products"
    product_files = sorted(
        [f for f in os.listdir(products_dir) if f.endswith(".json")],
        reverse=True
    )
    if not product_files:
        return None, None
    product_file = product_files[0]
    with open(os.path.join(products_dir, product_file), "r") as f:
        data = json.load(f)
    return product_file.replace(".json", ""), data

def upload_to_shopify(product_name, product_data):
    description = product_data.get("description", "No description")
    price = product_data.get("price", "14.99")

    log(f"🛒 Uploading {product_name} to Shopify...")

    payload = {
        "product": {
            "title": product_name,
            "body_html": description,
            "vendor": "IdeaReactor",
            "product_type": "Digital",
            "status": "active",
            "variants": [{"price": price}]
        }
    }

    response = requests.post(f"{BASE_URL}/products.json", json=payload, verify=False)

    if response.status_code != 201:
        log(f"❌ Failed to create product: {response.text}")
        return

    product_id = response.json()["product"]["id"]
    log(f"✅ Product created on Shopify with ID {product_id}")

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(entry)
    os.makedirs("logs", exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(entry + "\n")

if __name__ == "__main__":
    name, data = get_latest_product()
    if not data:
        log("⚠️ No product JSON found.")
    else:
        upload_to_shopify(name, data)
