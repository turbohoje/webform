#!/usr/bin/env python3

import requests
import hashlib
import time
import os

headers = {
        'authority': 'www.slr.aero',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,fr;q=0.8',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

def get_website_content(url):
    """Fetch website content and return its hash."""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        #print(response.content)
        response.raise_for_status()  # Raises an HTTPError if the status is 4xx, 5xx
        return hashlib.sha256(response.content).hexdigest()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def monitor_website_changes(url, check_interval=60):
    """Monitor website for changes and alert when content changes."""
    print(f"Monitoring {url} for changes every {check_interval} seconds...")
    previous_hash = get_website_content(url)
    
    while True:
        time.sleep(check_interval)
        current_hash = get_website_content(url)
        
        if current_hash != previous_hash:
            print(f"Change detected in {url}!")
            for i in range(20):
                os.system("say 'the page has changed'")
            # Here you could add your own alert mechanism (e.g., send an email or SMS)
            previous_hash = current_hash
        else:
            print(f"No changes detected in {url}.")

# Example usage
url_to_monitor = 'https://www.slr.aero/news/'  # Replace with the URL you want to monitor
check_interval_seconds = 300  # Check every 5 minutes

monitor_website_changes(url_to_monitor, check_interval_seconds)
