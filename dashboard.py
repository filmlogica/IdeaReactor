from flask import Flask, render_template_string, request
from datetime import datetime
import os

app = Flask(__name__)
LOG_FILE = "logs/pipeline_log.txt"
PAYMENT_LOG = "logs/paypal_payments.txt"

@app.route("/")
def dashboard():
    log_output = ""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            log_output = f.read()
    payment_output = ""
    if os.path.exists(PAYMENT_LOG):
        with open(PAYMENT_LOG, "r") as f:
            payment_output = f.read()
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>IdeaReactor Dashboard</title>
    <style>
        body { font-family: monospace; background: #111; color: #0f0; padding: 20px; }
        h1 { color: #0ff; }
        pre { background: #000; border: 1px solid #0f0; padding: 10px; max-height: 400px; overflow-y: scroll; }
    </style>
</head>
<body>
    <h1>🧠 IdeaReactor Automation Log</h1>
    <pre>{{ log_output }}</pre>
    <h1>💰 PayPal Deposits</h1>
    <pre>{{ payment_output }}</pre>
</body>
</html>
""", log_output=log_output, payment_output=payment_output)

@app.route("/paypal/ipn", methods=["POST"])
def paypal_ipn():
    data = request.form.to_dict()
    if data.get("payment_status") == "Completed":
        with open(PAYMENT_LOG, "a") as f:
            f.write(f"[{datetime.now()}] Payment received: ${data.get('mc_gross')} from {data.get('payer_email')}\n")
    return "", 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
