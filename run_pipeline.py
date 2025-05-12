import json
import subprocess
import os
from datetime import datetime
import trends_scraper

def main():
    print("🧠 [IdeaReactor] Starting full automation sequence...")

    # Step 1: Update trends
    trends_scraper.update_trends()

    # Step 2: Read trend data
    with open("trend.json", "r") as f:
        trend = json.load(f)

    print(f"""
🔥 [Top Trend Identified]
   Topic : {trend['topic']}
   Reason: {trend['reason']}
   Score : {trend['score']}
""")

    # Step 3: Generate product name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    product_name = f"IdeaReactor_{timestamp}"
    print(f"📦 [Product Name] {product_name}")

    # Step 4: Build product
    subprocess.run(["python", "product_builder.py", product_name], check=True)

    # Step 5: Upload product
    subprocess.run(["python", "shopify_uploader.py", product_name], check=True)

    print("🚀 [DONE] All steps completed.")

if __name__ == "__main__":
    main()
