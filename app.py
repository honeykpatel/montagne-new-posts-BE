"""
Fetch the latest 5 posts from the r/learnpython.
"""
import time
import threading

from flask import Flask, jsonify
from flask_cors import CORS
import praw
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

reddit = praw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'),
                     client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                     user_agent=os.getenv('REDDIT_USER_AGENT'))

latest_posts = []
LEN = 50

def fetch_reddit_posts():
    global latest_posts
    while True:
        # Fetch the latest 5 posts
        new_posts = []
        for submission in reddit.subreddit('montagneparfums').new(limit=LEN):
            new_posts.append({
                'title': submission.title,
                'url': submission.url,
                'upvotes': submission.ups,
                'author': submission.author.name if submission.author else 'Deleted',
            })

        # Add new posts to the beginning of the list
        latest_posts = new_posts + latest_posts

        # Keep only the last LEN posts
        if len(latest_posts) > LEN:
            latest_posts = latest_posts[:LEN]

        # Wait for 30 seconds before fetching again
        time.sleep(30)

# Start the background thread to fetch posts
threading.Thread(target=fetch_reddit_posts, daemon=True).start()

@app.route('/reddit', methods=['GET'])
def posts():
    return jsonify(latest_posts)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
