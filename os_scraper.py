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

def scrape_windows_releases():
    url = "https://learn.microsoft.com/en-us/windows/release-health/"
    data = []
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        updates = soup.find_all("li")
        for update in updates:
            text = update.get_text(strip=True)
            if "Windows 11" in text or "Windows 10" in text:
                data.append({
                    "Platform": "Windows",
                    "Release": text,
                    "Date": datetime.today().strftime("%Y-%m-%d")
                })
    except Exception as e:
        print(f"❌ Error scraping Windows releases: {e}")
    return data

def compile_os_updates():
    all_data = []
    all_data.extend(scrape_apple_releases())
    all_data.extend(fetch_chromebook_schedule())
    all_data.extend(scrape_windows_releases())

    df = pd.DataFrame(all_data)

    # Ensure CSV is created even if no data is scraped
    if df.empty:
        df = pd.DataFrame(columns=["Platform", "Release", "Date", "Checked_On"])

    df["Checked_On"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    df.to_csv("latest_os_versions.csv", index=False)
    print("✅ OS update data saved to latest_os_versions.csv")

if __name__ == "__main__":
    compile_os_updates()
