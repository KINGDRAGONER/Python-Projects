import requests
import json

# Replace YOUR_API_KEY with your API key
API_KEY = 'API-KEY HERE'

# Replace VIDEO_ID with the ID of the YouTube video for which you want to retrieve the comments
VIDEO_ID = 'VIDEO ID HERE'

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

# Print the comments
for comment in comments:
    print(comment['snippet']['topLevelComment']['snippet']['textOriginal'])
