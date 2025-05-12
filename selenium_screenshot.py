import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def take_gumroad_screenshot(product_url, product_name):
    print(f"👁️ [Screenshot] Opening browser for: {product_url}")

    # Setup headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # 'new' for Chrome 109+
    chrome_options.add_argument("--window-size=1280x1000")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(product_url)
        driver.implicitly_wait(10)  # wait for content to load

        # Screenshot filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{product_name}_{timestamp}.png"
        screenshot_path = os.path.join("products", product_name, "screenshots", filename)

        # Create folder if not exists
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

        driver.save_screenshot(screenshot_path)
        print(f"✅ [Screenshot Saved] {screenshot_path}")

    except Exception as e:
        print(f"❌ [Error] Could not take screenshot: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("❌ Usage: python selenium_screenshot.py <product_url> <product_name>")
        exit(1)

    product_url = sys.argv[1]
    product_name = sys.argv[2]
    take_gumroad_screenshot(product_url, product_name)

