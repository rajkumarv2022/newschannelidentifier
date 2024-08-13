import tkinter as tk
from tkinter import scrolledtext, ttk
from googleapiclient.discovery import build

# Replace with your own API key
API_KEY = '################################'

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

def open_link(url):
    import webbrowser
    webbrowser.open(url)

def show_details():
    channels = get_channel_details(youtube, channel_ids)
    
    # Create the Tkinter window
    window = tk.Tk()
    window.title("YouTube Channel Details")
    window.configure(bg='#f0f0f0')  # Light background color

    # Center Title Label
    title_label = tk.Label(window, text="Channel Details", font=("Helvetica", 18, "bold"), bg='#f0f0f0')
    title_label.pack(pady=(10, 20))

    # Create a frame for the details
    details_frame = tk.Frame(window, bg='#f0f0f0')
    details_frame.pack(padx=20, pady=10, fill='x')

    # Create a ScrolledText widget to display channel details
    text_area = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD, width=80, height=20, bg='white', fg='black', font=("Helvetica", 12))
    text_area.pack(side='left', padx=(0, 10), fill='both', expand=True)

    # Create a scrollbar for the text area
    scrollbar = tk.Scrollbar(details_frame, orient='vertical', command=text_area.yview)
    scrollbar.pack(side='right', fill='y')
    text_area.config(yscrollcommand=scrollbar.set)

    # Insert channel details into the text area
    for channel in channels:
        text_area.insert(tk.END, f"Channel ID: {channel['Channel ID']}\n")
        text_area.insert(tk.END, f"Title: {channel['Title']}\n")
        text_area.insert(tk.END, f"Language: {channel['Language']}\n")
        text_area.insert(tk.END, f"Country: {channel['Country']}\n")
        text_area.insert(tk.END, f"Description: {channel['Description']}\n")
        text_area.insert(tk.END, f"Subscriber Count: {channel['Subscriber Count']}\n")
        text_area.insert(tk.END, f"Video Count: {channel['Video Count']}\n")
        text_area.insert(tk.END, f"View Count: {channel['View Count']}\n")
        
        # Create a button to open the channel link
        link_button = tk.Button(window, text="Open Channel", command=lambda url=channel['Channel Link']: open_link(url), bg='#4CAF50', fg='white', font=("Helvetica", 12))
        link_button.pack(pady=5)

        text_area.insert(tk.END, "\n")
    
    # Start the Tkinter event loop
    window.mainloop()

# Call the function to display details
show_details()
