import csv
import requests

# Function to get Cloudflare D1 endpoint URL
def get_d1_endpoint_url():
    return 'https://newsapp.rajkumar-v2022cse.workers.dev/addnews'  # Replace with your actual endpoint URL

def get_headers():
    return {
        'Authorization': 'Bearer YOUR_API_KEY',  # Replace with your actual API key or token, if needed
        'Content-Type': 'application/json'
    }

# Function to execute SQL queries with debugging
def execute_query(query, params=None):
    d1_url = get_d1_endpoint_url()
    headers = get_headers()
    payload = {'query': query, 'params': params} if params else {'query': query}
    print(f"URL: {d1_url}")
    print(f"Headers: {headers}")
    print(f"Payload: {payload}")
    
    response = requests.post(d1_url, headers=headers, json=payload)
    
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Function to insert data into the table
def insert_news_website(name, url, category, language, region, state):
    query = '''
        INSERT INTO news_websites (name, url, category, language, region, state)
        VALUES (?, ?, ?, ?, ?, ?)
    '''
    params = (name, url, category, language, region, state)
    execute_query(query, params)

# Read data from CSV and insert into the database
file_path = r'E:\Desktop\newsbackend\newsapp\src\newswebsites\indian_news_websites.csv'
with open(file_path, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['name']
        url = row['url']
        category = row['category']
        language = row['language']
        region = row['region']
        state = row['state']
        insert_news_website(name, url, category, language, region, state)

print("Data inserted successfully.")
