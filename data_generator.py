import random
from datetime import datetime, timedelta
import json

# Sample tweet templates
TWEET_TEMPLATES = [
    "Just finished working on my new project! #coding #python",
    "Learning about data science and machine learning. #datascience #ml",
    "Beautiful day for coding! #programming #developer",
    "Working on my portfolio website. #webdev #frontend",
    "Just solved a challenging algorithm problem! #algorithms #coding",
    "Attending a tech conference today! #tech #conference",
    "New laptop setup complete! #tech #setup",
    "Learning about cloud computing. #cloud #aws",
    "Working on a new data visualization project. #dataviz #python",
    "Just deployed my first web application! #webdev #deployment"
]

# Sample hashtags
HASHTAGS = [
    "#coding", "#python", "#datascience", "#ml", "#programming",
    "#developer", "#webdev", "#frontend", "#algorithms", "#tech",
    "#conference", "#cloud", "#aws", "#dataviz", "#deployment"
]

def generate_mock_tweet():
    """Generate a mock tweet with random data."""
    # Randomly select a template
    tweet_text = random.choice(TWEET_TEMPLATES)
    
    # Add some random hashtags
    num_hashtags = random.randint(1, 3)
    additional_hashtags = random.sample(HASHTAGS, num_hashtags)
    tweet_text += " " + " ".join(additional_hashtags)
    
    # Generate random sentiment (-1 to 1)
    sentiment = random.uniform(-1, 1)
    
    # Generate random timestamp within last 24 hours
    timestamp = datetime.now() - timedelta(
        hours=random.randint(0, 24),
        minutes=random.randint(0, 60)
    )
    
    return {
        'tweet_id': str(random.randint(1000000, 9999999)),
        'text': tweet_text,
        'sentiment_score': sentiment,
        'created_at': timestamp,
        'hashtags': ','.join(additional_hashtags)
    }

def get_mock_tweets(count=100):
    """Generate a list of mock tweets."""
    return [generate_mock_tweet() for _ in range(count)]

def get_trending_topics(tweets):
    """Extract trending topics from mock tweets."""
    hashtag_counts = {}
    for tweet in tweets:
        if tweet['hashtags']:
            for tag in tweet['hashtags'].split(','):
                hashtag_counts[tag] = hashtag_counts.get(tag, 0) + 1
    return sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)[:10] 