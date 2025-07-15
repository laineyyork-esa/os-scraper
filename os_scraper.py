import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Common headers to avoid being blocked
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def scrape_apple_releases():
    url = "https://developer.apple.com/news/releases/"
    data = []
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        releases = soup.find_all("li")
        for release in releases:
            text = release.get_text(strip=True)
            if "iPadOS" in text or "macOS" in text:
                data.append({
                    "Platform": "iPadOS" if "iPadOS" in text else "macOS",
                    "Release": text,
                    "Date": datetime.today().strftime("%Y-%m-%d")
                })
    except Exception as e:
        print(f"❌ Error scraping Apple releases: {e}")
    return data

def fetch_chromebook_schedule():
    url = "https://chromiumdash.appspot.com/fetch_schedule"
    data = []
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        schedule = response.json()
        for item in schedule:
            if item.get("milestone"):
                data.append({
                    "Platform": "ChromeOS",
                    "Release": f"Milestone {item['milestone']}",
                    "Date": item.get("stable_date", "Unknown")
                })
    except Exception as e:
        print(f"❌ Error fetching Chromebook schedule: {e}")
    return data
