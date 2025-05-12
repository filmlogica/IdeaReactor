import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load credentials from .env
load_dotenv()
EMAIL = os.getenv("GUMROAD_EMAIL")
PASSWORD = os.getenv("GUMROAD_PASSWORD")

# Product setup
PRODUCT_NAME = 'IdeaReactor_20250510_223424'  # Or use the most recent folder name
PRODUCT_DESCRIPTION = 'This is a high-ticket B2B automation blueprint, built to sell.'
PRODUCT_PRICE = '15.87'
PRODUCT_ZIP_PATH = os.path.abspath(f'products/{PRODUCT_NAME}.zip')

# Start Selenium
options = Options()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)

try:
    print("🔐 Logging into Gumroad...")
    driver.get('https://gumroad.com/login')
    wait = WebDriverWait(driver, 20)

    email_input = wait.until(EC.presence_of_element_located((By.NAME, "user[email]")))
    email_input.send_keys(EMAIL)

    password_input = wait.until(EC.presence_of_element_located((By.NAME, "user[password]")))
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)

    print("🧭 Navigating to New Product page...")
    driver.get('https://gumroad.com/products/new')
    time.sleep(3)

    print("🖱️ Selecting 'Digital product'...")
    digital_product_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Digital product')]"))
    )
    digital_product_button.click()
    time.sleep(3)

    print("📝 Filling in product details...")
    driver.find_element(By.NAME, 'product[name]').send_keys(PRODUCT_NAME)
    driver.find_element(By.NAME, 'product[description]').send_keys(PRODUCT_DESCRIPTION)

    price_input = driver.find_element(By.NAME, 'product[price]')
    price_input.clear()
    price_input.send_keys(PRODUCT_PRICE)

    print("📤 Uploading ZIP file...")
    upload_input = driver.find_element(By.NAME, 'product[files][]')
    upload_input.send_keys(PRODUCT_ZIP_PATH)
    time.sleep(15)  # Wait for upload to complete

    print("🚀 Publishing product...")
    publish_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Publish')]"))
    )
    publish_button.click()
    time.sleep(5)

    print("✅ Product uploaded and published successfully.")

except Exception as e:
    print(f"❌ An error occurred: {e}")
finally:
    driver.quit()

