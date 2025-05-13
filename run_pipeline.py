import json
import subprocess
import os
from datetime import datetime
import trends_scraper
import mistral_writer
import price_engine

def main():
    print("[IdeaReactor] Starting full automation sequence...")

    # Step 1: Scrape Trends
    trends_scraper.main()

    # Step 2: Load trending topic
    with open("trend.json", "r") as f:
        trend = json.load(f)

    topic = trend['topic']
    reason = trend['reason']
    score = trend['score']
    print(f"""
[Top Trend Identified]
   Topic : {topic}
   Reason: {reason}
   Score : {score}
""")

    # Step 3: Generate timestamped product name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    product_name = f"IdeaReactor_{timestamp}"
    print(f"[Product Name] {product_name}")

    # Step 4: Generate content using Mistral
    print("[Generating product description using Mistral]")
    mistral_writer.generate_description(topic, product_name)

    # Step 5: Determine dynamic price
    print("[Running price engine]")
    price = price_engine.calculate_price(score)
    print(f"[Suggested Price] ${price:.2f}")

    # Save price info
    with open(f"products/{product_name}.json", "r+") as f:
        product_data = json.load(f)
        product_data['price'] = price
        f.seek(0)
        json.dump(product_data, f, indent=2)
        f.truncate()

    # Step 6: Build product package
    subprocess.run(["python", "product_builder.py", product_name], check=True)

    # Step 7: Upload to Shopify
    subprocess.run(["python", "shopify_uploader.py", product_name], check=True)

    # Step 8: Optional Gumroad upload
    try:
        subprocess.run(["python", "gumroad_auto_upload.py", product_name], check=True)
        print("[Gumroad Upload] Success")
    except Exception as e:
        print(f"[Gumroad Upload] Skipped or failed: {e}")

    print("[DONE] All automation steps completed successfully.")

if __name__ == "__main__":
    main()
