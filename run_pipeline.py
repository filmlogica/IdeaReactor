import trends_scraper
import polygon_monitor
import shopify_uploader
import mistral_connector

def main():
    # Step 1: Update trends
    trends_scraper.update_trends()

    # Step 2: Monitor stock data
    stock_data = polygon_monitor.fetch_stock_data()

    # Step 3: Process data with Mistral
    processed_data = mistral_connector.process_data(stock_data)

    # Step 4: Upload products to Shopify
    shopify_uploader.upload_products(processed_data)

if __name__ == "__main__":
    main()
