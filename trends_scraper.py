import requests
from bs4 import BeautifulSoup
import feedparser
import json
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_reddit_trends():
    logging.info("Fetching Reddit trends...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = 'https://www.reddit.com/r/popular/.json'
        response = requests.get(url, headers=headers)
        data = response.json()
        trends = [post['data']['title'] for post in data['data']['children']]
        return trends
    except Exception as e:
        logging.error(f"Reddit fetch error: {e}")
        return []

def fetch_twitter_trends():
    logging.info("Fetching Twitter trends...")
    try:
        # Placeholder for Twitter trends fetching logic
        # Implement using Twitter API or scraping as per your setup
        trends = ["#ExampleTrend1", "#ExampleTrend2"]
        return trends
    except Exception as e:
        logging.error(f"Twitter fetch error: {e}")
        return []

def fetch_youtube_trends():
    logging.info("Fetching YouTube trends...")
    try:
        # Placeholder for YouTube trends fetching logic
        # Implement using YouTube Data API or scraping as per your setup
        trends = ["YouTube Trend 1", "YouTube Trend 2"]
        return trends
    except Exception as e:
        logging.error(f"YouTube fetch error: {e}")
        return []

def fetch_producthunt_trends():
    logging.info("Fetching Product Hunt trends...")
    try:
        url = 'https://www.producthunt.com/feed'
        feed = feedparser.parse(url)
        trends = [entry.title for entry in feed.entries]
        return trends
    except Exception as e:
        logging.error(f"Product Hunt fetch error: {e}")
        return []

def fetch_github_trends():
    logging.info("Fetching GitHub trends...")
    try:
        url = 'https://github.com/trending'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        repo_tags = soup.find_all('h1', {'class': 'h3 lh-condensed'})
        trends = [tag.text.strip().replace('\n', '').replace(' ', '') for tag in repo_tags]
        return trends
    except Exception as e:
        logging.error(f"GitHub fetch error: {e}")
        return []

def fetch_amazon_trends():
    logging.info("Fetching Amazon Best Sellers...")
    try:
        url = 'https://www.amazon.com/Best-Sellers/zgbs'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.select('div.p13n-sc-truncate')
        trends = [title.get_text(strip=True) for title in titles]
        return trends
    except Exception as e:
        logging.error(f"Amazon fetch error: {e}")
        return []

def fetch_linkedin_trends():
    logging.info("Fetching LinkedIn trends...")
    try:
        # Placeholder for LinkedIn trends fetching logic
        # Implement using LinkedIn API or scraping as per your setup
        trends = ["LinkedIn Trend 1", "LinkedIn Trend 2"]
        return trends
    except Exception as e:
        logging.error(f"LinkedIn fetch error: {e}")
        return []

def fetch_etsy_trends():
    logging.info("Fetching Etsy trends...")
    try:
        url = 'https://www.etsy.com/trending-items'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.find_all('h3', {'class': 'text-gray text-truncate mb-xs-0 text-body'})
        trends = [title.get_text(strip=True) for title in titles]
        return trends
    except Exception as e:
        logging.error(f"Etsy fetch error: {e}")
        return []

def fetch_techcrunch_trends():
    logging.info("Fetching TechCrunch trends...")
    try:
        url = 'https://techcrunch.com/feed/'
        feed = feedparser.parse(url)
        trends = [entry.title for entry in feed.entries]
        return trends
    except Exception as e:
        logging.error(f"TechCrunch fetch error: {e}")
        return []

def fetch_quora_trends():
    logging.info("Fetching Quora trends...")
    try:
        # Placeholder for Quora trends fetching logic
        # Implement using Quora API or scraping as per your setup
        trends = ["Quora Trend 1", "Quora Trend 2"]
        return trends
    except Exception as e:
        logging.error(f"Quora fetch error: {e}")
        return []

def aggregate_trends():
    all_trends = []
    all_trends.extend(fetch_reddit_trends())
    all_trends.extend(fetch_twitter_trends())
    all_trends.extend(fetch_youtube_trends())
    all_trends.extend(fetch_producthunt_trends())
    all_trends.extend(fetch_github_trends())
    all_trends.extend(fetch_amazon_trends())
    all_trends.extend(fetch_linkedin_trends())
    all_trends.extend(fetch_etsy_trends())
    all_trends.extend(fetch_techcrunch_trends())
    all_trends.extend(fetch_quora_trends())
    unique_trends = list(set(all_trends))
    logging.info(f"Total unique trends fetched: {len(unique_trends)}")
    return unique_trends

if __name__ == "__main__":
    trends = aggregate_trends()
    for trend in trends:
        print(trend)

