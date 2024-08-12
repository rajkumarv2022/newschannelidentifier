import requests
from bs4 import BeautifulSoup
import re
import csv

# Function to fetch and parse a page
def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None

# Function to determine if a URL is a valid news website link
def is_valid_news_url(url):
    # Exclude URLs that point to Wikipedia pages, images, or non-news content
    if "wikipedia.org" in url or "w/index.php" in url:
        return False
    if re.search(r'\.(jpg|jpeg|png|gif|txt|pdf)$', url):
        return False
    if "directory" in url or "reviews" in url or "file" in url.lower():
        return False
    # Additional filtering rules as needed
    return True

# Function to extract URLs from a directory page
def extract_urls_from_directory(soup, base_url="", category="", language="", region="", state=""):
    urls = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('http'):
            if is_valid_news_url(href):
                urls.append({"name": a_tag.get_text(strip=True), "url": href, "category": category, "language": language, "region": region, "state": state})
        elif href.startswith('/'):
            # For relative URLs, prepend the base URL
            full_url = base_url + href
            if is_valid_news_url(full_url):
                urls.append({"name": a_tag.get_text(strip=True), "url": full_url, "category": category, "language": language, "region": region, "state": state})
    return urls

# List to store all Indian news URLs
all_news_data = []

# Expanded list of directories or pages that list Indian news websites with associated metadata
directory_urls = [
    {'url': 'https://digital-directory.sabguru.com/asia/india/tamil/', 'category': 'Regional', 'language': 'Tamil', 'region': 'Southern India', 'state': 'Tamil Nadu'},
    {'url': 'https://en.wikipedia.org/wiki/List_of_newspapers_in_India', 'category': 'Various', 'language': 'Various', 'region': 'Nationwide', 'state': 'N/A'},
    {'url': 'https://www.4imn.com/in/', 'category': 'Various', 'language': 'Various', 'region': 'Nationwide', 'state': 'N/A'},
    {'url': 'https://www.newspaperslist.com/india/', 'category': 'Various', 'language': 'Various', 'region': 'Nationwide', 'state': 'N/A'},
    {'url': 'https://www.w3newspapers.com/india/', 'category': 'Various', 'language': 'Various', 'region': 'Nationwide', 'state': 'N/A'},
    {'url': 'https://www.onlinenewspapers.com/india.htm', 'category': 'Various', 'language': 'Various', 'region': 'Nationwide', 'state': 'N/A'},
    # Add more URLs here as needed with appropriate metadata
]

# Scrape each directory for URLs
for directory in directory_urls:
    soup = fetch_page(directory['url'])
    if soup:
        base_url = "/".join(directory['url'].split("/")[:3])  # Extract base URL
        news_data = extract_urls_from_directory(soup, base_url, directory['category'], directory['language'], directory['region'], directory['state'])
        all_news_data.extend(news_data)

# Filter out duplicates based on URLs
unique_news_data = {entry['url']: entry for entry in all_news_data}.values()

# Save to a CSV file
file_path = r'E:\Desktop\newsbackend\newsapp\src\newswebsites\indian_news_websites.csv'
with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['name', 'url', 'category', 'language', 'region', 'state']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for data in unique_news_data:
        writer.writerow(data)

print(f"Total unique news websites found: {len(unique_news_data)}")
print(f"Data saved to {file_path}")
