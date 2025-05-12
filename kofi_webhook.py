from flask import Flask, request
import os
import subprocess
import json
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route("/kofi-webhook", methods=["POST"])
def kofi_webhook():
    print("🧾 Incoming Headers:")
    print(json.dumps(dict(request.headers), indent=2))

    token = request.headers.get("Authorization") or request.headers.get("X-Api-Key")
    expected_token = os.getenv("KOFI_VERIFICATION_TOKEN")

    if token != expected_token:
        print("⚠️  Warning: Token mismatch. Accepting request anyway for testing.")

    # ✅ Accept application/x-www-form-urlencoded
    if request.content_type == "application/x-www-form-urlencoded":
        data = request.form.to_dict()
    else:
        try:
            data = request.get_json(force=True)
        except Exception:
            data = {}

    print("🎉 Ko-Fi Support Received!")
    print(json.dumps(data, indent=2))

    message = data.get("message", "Generate a product based on trending AI topics.")
    supporter = data.get("from_name", "Anonymous")

    print(f"🚀 Triggering IdeaReactor pipeline for: {supporter}")
    print(f"💬 Ko-Fi message: {message}")

    # Save message for generation use
    with open("donation_prompt.txt", "w") as f:
        f.write(message)

    try:
        subprocess.run(["python", "run_pipeline.py"], check=True)
        print("✅ Pipeline executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running pipeline: {e}")

    return "Webhook received. Processing started.", 200

if __name__ == "__main__":
    app.run(port=5000)

