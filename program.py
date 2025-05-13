Python 3.12.5 (tags/v3.12.5:ff3bc82, Aug  6 2024, 20:45:27) [MSC v.1940 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import tweepy
from textblob import TextBlob
from nrclex import NRCLex
import pandas as pd
import matplotlib.pyplot as plt

... # Twitter API credentials (Replace with your own)
... API_KEY = 'your_api_key'
... API_SECRET = 'your_api_secret'
... ACCESS_TOKEN = 'your_access_token'
... ACCESS_SECRET = 'your_access_secret'
... 
... # Authenticate with Twitter API
... auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
... auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
... api = tweepy.API(auth)
... 
... # Function to clean tweet text
... def clean_text(text):
...     return ' '.join(word for word in text.split() if not word.startswith('http') and not word.startswith('@') and word.isalpha())
... 
... # Function to analyze sentiment and emotion
... def analyze_tweet(tweet):
...     cleaned = clean_text(tweet)
...     blob = TextBlob(cleaned)
...     polarity = blob.sentiment.polarity
...     subjectivity = blob.sentiment.subjectivity
...     emotion = NRCLex(cleaned).top_emotions
...     return polarity, subjectivity, emotion
... 
... # Fetch tweets about a topic
... def fetch_and_analyze(query, count=50):
...     tweets = api.search_tweets(q=query, lang='en', count=count)
...     data = []
...     for tweet in tweets:
...         text = tweet.text
...         polarity, subjectivity, emotions = analyze_tweet(text)
...         data.append({
...             'Tweet': text,
...             'Polarity': polarity,
...             'Subjectivity': subjectivity,
...             'Emotions': emotions
...         })
...     return pd.DataFrame(data)
... 
# Run analysis
query = "mental health"
df = fetch_and_analyze(query)

# Display sample results
print(df[['Tweet', 'Polarity', 'Subjectivity', 'Emotions']].head())

# Plot common emotions
emotion_counts = {}
for row in df['Emotions']:
    for emotion, score in row:
        if emotion in emotion_counts:
            emotion_counts[emotion] += 1
        else:
            emotion_counts[emotion] = 1

# Plot
plt.bar(emotion_counts.keys(), emotion_counts.values(), color='skyblue')
plt.title(f"Emotion Distribution in '{query}' Tweets")
plt.xlabel("Emotions")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
