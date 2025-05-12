import yfinance as yf
import time
import subprocess
from datetime import datetime

# Settings
STOCK_SYMBOLS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NFLX', 'NVDA']
DROP_THRESHOLD = 3.0  # Percent drop to trigger product generation
CHECK_INTERVAL = 3600  # Seconds (1 hour)

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def check_stock_drops():
    for symbol in STOCK_SYMBOLS:
        ticker = yf.Ticker(symbol)
        try:
            df = ticker.history(period="1d", interval="1m")
            if df.empty:
                log(f"No data for {symbol}. Skipping.")
                continue

            open_price = df['Open'].iloc[0]
            latest_price = df['Close'].iloc[-1]
            drop_pct = ((open_price - latest_price) / open_price) * 100

            log(f"{symbol} dropped {drop_pct:.2f}% today.")

            if drop_pct >= DROP_THRESHOLD:
                log(f"🚨 {symbol} exceeded drop threshold. Triggering IdeaReactor...")
                subprocess.run(["python", "run_pipeline.py"], check=True)
        except Exception as e:
            log(f"Error checking {symbol}: {e}")

if __name__ == "__main__":
    while True:
        log("🔍 Monitoring stock prices for distress signals...")
        check_stock_drops()
        log(f"⏳ Waiting {CHECK_INTERVAL // 60} minutes until next check...\n")
        time.sleep(CHECK_INTERVAL)
