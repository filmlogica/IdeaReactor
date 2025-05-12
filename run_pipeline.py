import subprocess
import os
import json
from datetime import datetime

# Setup
print("🧠 [IdeaReactor] Starting full automation sequence...")

# Step 1: Run trends_scraper.py
print("📈 [Step 1] Running trends_scraper.py...")
subprocess.run(["python", "trends_scraper.py"], check=True)

# Load trend data
with open("trend.json", "r") as f:
    trend_data = json.load(f)

trend_topic = trend_data["topic"]
print(f"\n🔥 [Top Wealth-Weighted Trend]\n   Topic         : {trend_topic}\n   Reason        : {trend_data['reason']}\n   Adjusted Score: {trend_data['score']}")

# Create product name
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
product_name = f"IdeaReactor_{timestamp}"
print(f"\n📦 [Product Name] {product_name}")

# Step 2: Run product_builder.py
print("🛠️ [Step 2] Building product...")
subprocess.run(["python", "product_builder.py", product_name], check=True)

# Step 3: Run price_engine.py
print("💰 [Step 3] Calculating price...")
subprocess.run(["python", "price_engine.py", product_name], check=True)

# Step 4: Run product_packer.py
print("📦 [Step 4] Packaging product...")
subprocess.run(["python", "product_packer.py", product_name], check=True)

# Step 5: Save product metadata for upload
latest_product_metadata = {
    "title": product_name.replace("_", " "),
    "description": open(f"products/{product_name}/README.md").read(),
    "price": open(f"products/{product_name}/price.txt").read().strip(),
    "tags": [trend_topic.lower(), "ai", "automation", "digital"],
    "images": []  # Optional: Add hosted image URLs if available
}

with open("products/latest_product.json", "w") as f:
    json.dump(latest_product_metadata, f, indent=2)

# Step 6: Upload to Shopify
print("🌐 [Step 5] Uploading to Shopify...")
subprocess.run(["python", "shopify_uploader.py"], check=True)

print("✅ [DONE] Full pipeline execution complete.")

