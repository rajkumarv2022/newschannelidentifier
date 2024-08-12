import tkinter as tk
from tkinter import ttk
from googleapiclient.discovery import build
import webbrowser

# Replace with your actual API key
API_KEY = 'AIzaSyCC74lgrUF4dIAWMyOM1_3kpOOwGKFzsKg'

def get_news_channels(api_key, region_code='IN', max_results=50, keyword='news'):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part='snippet',
        type='channel',
        regionCode=region_code,
        maxResults=max_results,
        q=keyword
    )
    response = request.execute()
    
    channels = []
    for item in response['items']:
        channel_info = {
            'Channel ID': item['id']['channelId'],
            'Title': item['snippet']['title'],
            'Description': item['snippet']['description'],
            'Language': item['snippet'].get('defaultLanguage', 'unknown'),
            'Country': item['snippet'].get('country', 'unknown'),
            'Channel Link': f"https://www.youtube.com/channel/{item['id']['channelId']}"
        }
        channels.append(channel_info)
    
    return channels

class YouTubeApp:
    def __init__(self, root):
        self.root = root
        self.root.title('YouTube News Channels')
        
        # Search Frame
        search_frame = ttk.Frame(self.root, padding="10")
        search_frame.pack(fill='x')
        
        # Search Entry
        self.search_entry = ttk.Entry(search_frame, width=50)
        self.search_entry.pack(side='left', padx=5)
        
        # Search Button
        search_button = ttk.Button(search_frame, text="Search", command=self.search_channels)
        search_button.pack(side='left')
        
        # Results Frame
        self.results_frame = ttk.Frame(self.root)
        self.results_frame.pack(padx=10, pady=10)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.results_frame)
        self.scrollbar.pack(side='right', fill='y')
        
        # Results Text Widget
        self.results_text = tk.Text(self.results_frame, wrap='word', height=20, width=80, yscrollcommand=self.scrollbar.set)
        self.results_text.pack(side='left')
        self.scrollbar.config(command=self.results_text.yview)
        
        # Load initial data
        self.load_data()

    def load_data(self):
        channels = get_news_channels(API_KEY)
        self.display_channels(channels)
    
    def search_channels(self):
        keyword = self.search_entry.get()
        channels = get_news_channels(API_KEY, keyword=keyword)
        self.display_channels(channels)

    def display_channels(self, channels):
        self.results_text.delete('1.0', tk.END)
        for channel in channels:
            self.results_text.insert(tk.END, "Channel Details:\n")
            for key, value in channel.items():
                self.results_text.insert(tk.END, f"{key}: {value}\n")
            
            # Add the open link button
            channel_link = channel['Channel Link']
            open_button = ttk.Button(self.results_text, text="Open Channel", command=lambda link=channel_link: webbrowser.open(link))
            self.results_text.window_create(tk.END, window=open_button)
            
            self.results_text.insert(tk.END, "\n" + "="*40 + "\n")
        self.results_text.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeApp(root)
    root.mainloop()
