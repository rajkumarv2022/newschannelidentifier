# newschannelidentifier
displaying news youtube channlels

# Documentation: `news.py`

## Overview
The `news.py` script is a Python-based web scraper that collects and organizes a list of Indian news websites. The script uses the Tkinter library to create a graphical user interface (GUI) that allows users to scrape, view, and search through the collected news website data. The scraped data is saved into a CSV file named `indian_news_websites.csv`, which includes information such as the website's name, URL, category, language, region, and state. Users can search for specific websites within the application and open them directly in their web browser.

## Dependencies
To run the script, ensure that the following Python libraries are installed:

- `tkinter` (Standard Python library for GUI applications)
- `requests` (For sending HTTP requests)
- `bs4` (BeautifulSoup for parsing HTML)
- `re` (For regular expression operations)
- `csv` (For writing CSV files)
- `webbrowser` (For opening URLs in the default web browser)

You can install missing dependencies using pip:

```bash
pip install requests beautifulsoup4

