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

# YouTube News Channels Search Application

This Python application uses Tkinter for the graphical user interface (GUI) and the YouTube Data API to fetch and display information about YouTube news channels. The application allows users to search for channels by keyword and view the channel details, including the ability to open the channel directly in a web browser.

## Features

- **Search YouTube News Channels**: Users can enter a keyword to search for YouTube channels related to news.
- **Display Channel Information**: The application displays the Channel ID, Title, Language, Country, and a link to open the channel.
- **Interactive Interface**: Users can double-click on a channel entry to open the channel in their default web browser.

## Dependencies

The following Python libraries are required for this application:

- `tkinter`: Standard Python interface to the Tk GUI toolkit.
- `googleapiclient`: Python client library for accessing Google APIs, including the YouTube Data API.
- `webbrowser`: Python library for opening web pages.

You can install the `googleapiclient` library using pip:

```bash
pip install google-api-python-client

