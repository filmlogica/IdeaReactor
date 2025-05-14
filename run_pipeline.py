import subprocess
import os
import json
from datetime import datetime

os.makedirs("logs", exist_ok=True)

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}"
    print(entry)
    with open("logs/pipeline_log.txt", "a") as f:
        f.write(entry + "\n")

def main():
    log("🧠 Starting IdeaReactor automation pipeline...")

    try:
        subprocess.run(["python", "trends_scraper.py"], check=True)
        with open("trend.json", "r") as f:
            trend = json.load(f)
        topic = trend.get("topic", "AI Automation Tools")
        reason = trend.get("reason", "AI-generated product relevance")
        score = trend.get("score", 70)
    except Exception as e:
        log(f"⚠️ Failed to load trend.json, using fallback trend: {e}")
        topic = "Fallback Trend"
        reason = "No trend file found"
        score = 50

    log(f"🔥 Top trend identified and saved: {topic}")

    product_name = topic.replace(" ", "_") + "_Product"
    subprocess.run(["python", "mistral_writer.py", topic, product_name], check=True)
    subprocess.run(["python", "price_engine.py", product_name], check=True)
    subprocess.run(["python", "shopify_uploader.py", product_name], check=True)

    log(f"✅ Automation complete for: {product_name}")

if __name__ == "__main__":
    main()
