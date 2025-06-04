from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from utils.data_generator import get_mock_tweets, get_trending_topics

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tweets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Database Models
class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.String(50), unique=True)
    text = db.Column(db.Text)
    sentiment_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    hashtags = db.Column(db.String(200))

# Create database tables and populate with initial data
with app.app_context():
    db.create_all()
    # Only populate if the database is empty
    if Tweet.query.count() == 0:
        mock_tweets = get_mock_tweets(100)
        for tweet in mock_tweets:
            db_tweet = Tweet(
                tweet_id=tweet['tweet_id'],
                text=tweet['text'],
                sentiment_score=tweet['sentiment_score'],
                created_at=tweet['created_at'],
                hashtags=tweet['hashtags']
            )
            db.session.add(db_tweet)
        db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tweets')
def get_tweets():
    tweets = Tweet.query.order_by(Tweet.created_at.desc()).limit(100).all()
    return jsonify([{
        'id': tweet.tweet_id,
        'text': tweet.text,
        'sentiment': tweet.sentiment_score,
        'created_at': tweet.created_at.isoformat(),
        'hashtags': tweet.hashtags
    } for tweet in tweets])

@app.route('/api/trending')
def get_trending():
    tweets = Tweet.query.order_by(Tweet.created_at.desc()).limit(100).all()
    hashtags = {}
    for tweet in tweets:
        if tweet.hashtags:
            for tag in tweet.hashtags.split(','):
                hashtags[tag] = hashtags.get(tag, 0) + 1
    return jsonify(sorted(hashtags.items(), key=lambda x: x[1], reverse=True)[:10])

@app.route('/api/refresh')
def refresh_data():
    """Endpoint to refresh the mock data"""
    # Clear existing data
    Tweet.query.delete()
    
    # Generate new mock data
    mock_tweets = get_mock_tweets(100)
    for tweet in mock_tweets:
        db_tweet = Tweet(
            tweet_id=tweet['tweet_id'],
            text=tweet['text'],
            sentiment_score=tweet['sentiment_score'],
            created_at=tweet['created_at'],
            hashtags=tweet['hashtags']
        )
        db.session.add(db_tweet)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Data refreshed successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5001) 