import feedparser
import tweepy
import os
import sys
import time

# --- CONFIGURATION ---
RSS_URL = "https://boringnews.ca/manitoba/feed/"
HASHTAGS = "#manitoba #news"
LOG_FILE = "posted.log"

# --- AUTHENTICATE ---
try:
    client = tweepy.Client(
        consumer_key=os.environ['CONSUMER_KEY'],
        consumer_secret=os.environ['CONSUMER_SECRET'],
        access_token=os.environ['ACCESS_TOKEN'],
        access_token_secret=os.environ['ACCESS_TOKEN_SECRET']
    )
except Exception as e:
    print(f"Authentication Error: {e}")
    sys.exit(1)

# --- LOAD HISTORY ---
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'r') as f:
        posted_urls = [line.strip() for line in f.readlines()]
else:
    posted_urls = []

# --- PARSE FEED ---
print(f"Checking feed: {RSS_URL}")
feed = feedparser.parse(RSS_URL)
new_posts = []

# Iterate in reverse (oldest first)
for entry in reversed(feed.entries):
    link = entry.link
    title = entry.title

    if link not in posted_urls:
        print(f"Found new story: {title}")
        tweet_text = f"{title}\n\n{link}\n\n{HASHTAGS}"

        try:
            client.create_tweet(text=tweet_text)
            print(f"✅ Posted!")
            new_posts.append(link)
            time.sleep(2) # Wait 2 seconds between posts to be safe
        except Exception as e:
            print(f"❌ Failed to post: {e}")

# --- SAVE HISTORY ---
if new_posts:
    with open(LOG_FILE, 'a') as f:
        for link in new_posts:
            f.write(f"{link}\n")
else:
    print("No new stories found.")
