import tkinter as tk
from tkinter import ttk, messagebox
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
        self.root.geometry('1000x600')
        self.root.configure(bg='#f0f0f0')

        # Create a Frame for the UI
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill='both', expand=True)

        # Add a Button to start the search
        search_frame = ttk.Frame(frame)
        search_frame.pack(pady=5)

        self.search_entry = ttk.Entry(search_frame, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_button = ttk.Button(search_frame, text="Search", command=self.search_channels)
        search_button.pack(side=tk.LEFT)

        # Add a Treeview to display the results
        columns = ('Channel ID', 'Title', 'Language', 'Country', 'Open Channel')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')
        self.tree.pack(padx=5, pady=5, fill='both', expand=True)

        # Define the column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Add style to Treeview
        style = ttk.Style()
        style.configure('Treeview', background='#ffffff', foreground='#000000', rowheight=25, fieldbackground='#ffffff')
        style.configure('Treeview.Heading', background='#e0e0e0', font=('Arial', 10, 'bold'))

        # Bind double-click event to open link
        self.tree.bind('<Double-1>', self.open_link)

        # Load initial data
        self.load_data()

    def load_data(self):
        channels = get_news_channels(API_KEY)
        self.update_treeview(channels)
    
    def search_channels(self):
        keyword = self.search_entry.get()
        channels = get_news_channels(API_KEY, keyword=keyword)
        self.update_treeview(channels)

    def update_treeview(self, channels):
        self.tree.delete(*self.tree.get_children())
        for channel in channels:
            self.tree.insert('', tk.END, values=(
                channel['Channel ID'],
                channel['Title'],
                channel['Language'],
                channel['Country'],
                'Open Channel'
            ))

    def open_link(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            url = f"https://www.youtube.com/channel/{item['values'][0]}"
            webbrowser.open(url)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeApp(root)
    root.mainloop()
