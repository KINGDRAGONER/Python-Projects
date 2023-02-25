import requests
import json
import csv

# Replace YOUR_API_KEY with your API key
API_KEY = 'AIzaSyDNnRmPlk-_KPmpCWJWZ8odNWcsWKBidt4'

# Replace VIDEO_ID with the ID of the YouTube video for which you want to retrieve the comments
VIDEO_ID = 'kpJdwKAx5p4'

# Define the API endpoint URL
url = 'https://www.googleapis.com/youtube/v3/commentThreads'

# Define the request parameters
params = {
    'part': 'snippet',
    'videoId': VIDEO_ID,
    'key': API_KEY,
    'textFormat': 'plainText',
    'maxResults': 100  # maximum number of comments to retrieve per API request
}

# Make an initial API request to get the total number of comments for the video
response = requests.get(url, params=params)
data = json.loads(response.text)
total_results = data['pageInfo']['totalResults']

# Initialize the list of comments
comments = []

# Make additional API requests if there are more than 100 comments
while len(comments) < total_results:
    response = requests.get(url, params=params)
    data = json.loads(response.text)
    comments.extend(data['items'])
    if 'nextPageToken' in data:
        params['pageToken'] = data['nextPageToken']
    else:
        break

# Sort the comments by most recent first
comments = sorted(comments, key=lambda x: x['snippet']['topLevelComment']['snippet']['publishedAt'], reverse=True)

# Write the comments to a CSV file
with open('comments.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Author', 'Date', 'Comment'])
    for comment in comments:
        author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
        text = comment['snippet']['topLevelComment']['snippet']['textOriginal']
        date = comment['snippet']['topLevelComment']['snippet']['publishedAt']
        writer.writerow([author, date, text])
        print(f'{author} ({date}): {text}\n')

print('Comments written to comments.csv')
