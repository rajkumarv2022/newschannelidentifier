import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import re
import csv
import webbrowser

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
    if "wikipedia.org" in url or "w/index.php" in url:
        return False
    if re.search(r'\.(jpg|jpeg|png|gif|txt|pdf)$', url):
        return False
    if "directory" in url or "reviews" in url or "file" in url.lower():
        return False
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
            full_url = base_url + href
            if is_valid_news_url(full_url):
                urls.append({"name": a_tag.get_text(strip=True), "url": full_url, "category": category, "language": language, "region": region, "state": state})
    return urls

# Function to perform scraping and update the UI
def perform_scraping():
    global all_news_data
    all_news_data = []

    directory_urls = [
        {'url': 'https://digital-directory.sabguru.com/asia/india/tamil/', 'category': 'Regional', 'language': 'Tamil', 'region': 'Southern India', 'state': 'Tamil Nadu'},
        {'url': 'https://en.wikipedia.org/wiki/List_of_newspapers_in_India', 'category': 'Various', 'language': 'Various', 'region': 'Nationwide', 'state': 'N/A'},
        {'url': 'https://www.4imn.com/in/', 'category': 'Various', 'language': 'Various', 'region': 'Nationwide', 'state': 'N/A'},
        {'url': 'https://www.newspaperslist.com/india/', 'category': 'Various', 'language': 'Various', 'region': 'Nationwide', 'state': 'N/A'},
        {'url': 'https://www.w3newspapers.com/india/', 'category': 'Various', 'language': 'Various', 'region': 'Nationwide', 'state': 'N/A'},
        {'url': 'https://www.onlinenewspapers.com/india.htm', 'category': 'Various', 'language': 'Various', 'region': 'Nationwide', 'state': 'N/A'},
    ]

    for directory in directory_urls:
        soup = fetch_page(directory['url'])
        if soup:
            base_url = "/".join(directory['url'].split("/")[:3])
            news_data = extract_urls_from_directory(soup, base_url, directory['category'], directory['language'], directory['region'], directory['state'])
            all_news_data.extend(news_data)

    unique_news_data = {entry['url']: entry for entry in all_news_data}.values()

    # Save to CSV
    file_path = 'indian_news_websites.csv'
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'url', 'category', 'language', 'region', 'state']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in unique_news_data:
            writer.writerow(data)

    messagebox.showinfo("Info", f"Data saved to {file_path}")

    update_treeview(unique_news_data)

def update_treeview(data):
    tree.delete(*tree.get_children())
    for entry in data:
        tree.insert('', tk.END, values=(entry['name'], entry['url'], entry['category'], entry['language'], entry['region'], entry['state']))

def open_link(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        url = item['values'][1]
        webbrowser.open(url)

def search():
    query = search_entry.get().lower()
    filtered_data = [entry for entry in all_news_data if query in entry['name'].lower()]
    update_treeview(filtered_data)

# Set up the Tkinter UI
root = tk.Tk()
root.title('News Website Scraper')

# Set the theme
root.configure(bg='#f0f0f0')

# Create a Frame for the UI
frame = ttk.Frame(root, padding="10")
frame.pack(fill='both', expand=True)

# Add a Button to start the scraping process
scrape_button = ttk.Button(frame, text="Scrape News Websites", command=perform_scraping)
scrape_button.pack(pady=5)

# Add Search Entry and Button
search_frame = ttk.Frame(frame)
search_frame.pack(pady=5)

search_label = ttk.Label(search_frame, text="Search:", background='#f0f0f0')
search_label.pack(side=tk.LEFT, padx=5)

search_entry = ttk.Entry(search_frame, width=50)
search_entry.pack(side=tk.LEFT, padx=5)

search_button = ttk.Button(search_frame, text="Search", command=search)
search_button.pack(side=tk.LEFT, padx=5)

# Add a Treeview to display the results
columns = ('name', 'url', 'category', 'language', 'region', 'state')
tree = ttk.Treeview(frame, columns=columns, show='headings', selectmode='browse', style='Treeview')
tree.pack(padx=5, pady=5, fill='both', expand=True)

# Define the column headings
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, width=150)

# Add style to Treeview
style = ttk.Style()
style.configure('Treeview', background='#ffffff', foreground='#000000', rowheight=25, fieldbackground='#ffffff')
style.configure('Treeview.Heading', background='#e0e0e0', font=('Arial', 10, 'bold'))

# Bind double-click event to open link
tree.bind('<Double-1>', open_link)

# Global variable to store all news data
all_news_data = []

# Run the Tkinter event loop
root.mainloop()
