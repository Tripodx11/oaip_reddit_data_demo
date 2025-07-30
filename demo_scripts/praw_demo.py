#!/usr/bin/env python3
"""
Reddit scraper using PRAW.
1. Get 100 newest posts from r/ClaudeAI.
2. Get comments from the 10 newest posts in r/ClaudeAI.
3. Search for AI/ChatGPT mentions in r/Utah and save 10 matches.
"""

import praw
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Create Reddit instance
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="ai_econ_data_scraper_simple/1.0 by ai_eco_data_man11"
)

def make_dir_if_not_exists():
    if not os.path.exists('demo_data'):
        os.makedirs('demo_data')

def timestamped_filename(prefix):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{prefix}_{timestamp}.csv"

def get_100_new_claude_posts():
    print("Getting 100 newest posts from r/ClaudeAI...")
    make_dir_if_not_exists()
    posts = reddit.subreddit("ClaudeAI").new(limit=100)

    data = []
    for post in posts:
        data.append({
            'title': post.title,
            'author': str(post.author),
            'score': post.score,
            'num_comments': post.num_comments,
            'created_utc': post.created_utc,
            'url': post.url,
            'permalink': post.permalink,
            'selftext': post.selftext
        })

    df = pd.DataFrame(data)
    filename = timestamped_filename("100_new_claude_posts")
    df.to_csv(f"demo_data/{filename}", index=False)
    print(f"✅ Saved {len(df)} posts to {filename}")

def get_comments_for_latest_10_claude_posts():
    print("Getting comments for 10 newest ClaudeAI posts...")
    make_dir_if_not_exists()
    posts = list(reddit.subreddit("ClaudeAI").new(limit=10))

    comments_all = []
    for post in posts:
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            comments_all.append({
                'post_title': post.title,
                'post_url': post.url,
                'comment_author': str(comment.author),
                'comment_body': comment.body,
                'comment_score': comment.score,
                'comment_created_utc': comment.created_utc,
            })

    df = pd.DataFrame(comments_all)
    filename = timestamped_filename("claude_comments_latest10")
    df.to_csv(f"demo_data/{filename}", index=False)
    print(f"✅ Saved {len(df)} comments to {filename}")

def get_10_new_utah_posts_with_ai_keywords():
    print("Getting posts in r/Utah with keywords 'AI' or 'ChatGPT'...")
    make_dir_if_not_exists()

    query = 'ai OR "chat gpt" OR chatgpt'
    keyword_pattern = re.compile(r'\b(ai|chat\s?gpt)\b', re.IGNORECASE)
    results = reddit.subreddit("Utah").search(query, sort="new", limit=50)

    matches = []
    for post in results:
        if keyword_pattern.search(post.title) or keyword_pattern.search(post.selftext):
            matches.append({
                'title': post.title,
                'author': str(post.author),
                'score': post.score,
                'num_comments': post.num_comments,
                'created_utc': post.created_utc,
                'url': post.url,
                'permalink': post.permalink,
                'selftext': post.selftext
            })

    if not matches:
        print("⚠️ No matching posts found.")
        return

    df = pd.DataFrame(matches)
    filename = timestamped_filename("utah_ai_posts")
    df.to_csv(f"demo_data/{filename}", index=False)
    print(f"✅ Saved {len(df)} posts to {filename}")

if __name__ == "__main__":
    get_100_new_claude_posts()
    get_comments_for_latest_10_claude_posts()
    get_10_new_utah_posts_with_ai_keywords()
