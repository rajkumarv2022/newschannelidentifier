import tkinter as tk
from tkinter import scrolledtext
from googleapiclient.discovery import build

# Replace with your own API key
API_KEY = 'AIzaSyCC74lgrUF4dIAWMyOM1_3kpOOwGKFzsKg'

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

# List of channel IDs you want to get information about
channel_ids = [
    'UC16niRr50-MSBwiO3YDb3RA',  # BBC News 
    # Add more channel IDs as needed
]

# Function to get channel details
def get_channel_details(youtube, channel_ids):
    request = youtube.channels().list(
        part='id,snippet,statistics',
        id=','.join(channel_ids)
    )
    response = request.execute()

    channel_data = []
    for item in response['items']:
        channel_id = item['id']
        channel_info = {
            'Channel ID': channel_id,
            'Title': item['snippet']['title'],
            'Description': item['snippet']['description'],
            'Language': item['snippet'].get('defaultLanguage', 'unknown'),
            'Country': item['snippet'].get('country', 'unknown'),
            'Subscriber Count': item['statistics'].get('subscriberCount', 'unknown'),
            'Video Count': item['statistics'].get('videoCount', 'unknown'),
            'View Count': item['statistics'].get('viewCount', 'unknown'),
            'Channel Link': f'https://www.youtube.com/channel/{channel_id}'
        }
        channel_data.append(channel_info)
    
    return channel_data

def show_details():
    channels = get_channel_details(youtube, channel_ids)
    
    # Create the Tkinter window
    window = tk.Tk()
    window.title("YouTube Channel Details")

    # Create a ScrolledText widget to display channel details
    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=20)
    text_area.pack(padx=10, pady=10)

    # Insert channel details into the text area
    for channel in channels:
        text_area.insert(tk.END, "Channel Details:\n")
        for key, value in channel.items():
            text_area.insert(tk.END, f"{key}: {value}\n")
        text_area.insert(tk.END, "\n" + "="*40 + "\n")
    
    # Start the Tkinter event loop
    window.mainloop()

# Call the function to display details
show_details()
