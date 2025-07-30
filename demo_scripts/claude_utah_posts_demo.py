#!/usr/bin/env python3
"""
Simple script to get 100 newest posts from r/ClaudeAI with Reddit API authentication.
"""

import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

def make_dir_if_not_exists():
    """Create demo_data directory if it doesn't exist."""
    if not os.path.exists('demo_data'):
        os.makedirs('demo_data')

def get_reddit_token():
    """Get Reddit access token using client credentials."""
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ No Reddit API credentials found!")
        print("Please add to .env file:")
        print("REDDIT_CLIENT_ID=your_client_id")
        print("REDDIT_CLIENT_SECRET=your_client_secret")
        #return None
    
    # Get access token
    #This url is the same for everyone, it's meant to get an access token
    #think of it like a login gateway for reddit api
    auth_url = "https://www.reddit.com/api/v1/access_token"
    #this tells the request that it is using client credentials, not web or enterprise or other possible ones
    auth_data = {
        'grant_type': 'client_credentials'
    }
    #This is meant to be descriptive to not make it think you are a bot
    auth_headers = {
        'User-Agent': 'ai_econ_data_scraper_simple/1.0 by ai_eco_data_man11'
    }
    
    try:
        response = requests.post(
            auth_url,
            data=auth_data,
            headers=auth_headers,
            auth=(client_id, client_secret)
        )
        response.raise_for_status()
        #takes json and puts it into a dictionary
        token_data = response.json()
        return token_data['access_token']
    except Exception as e:
        print(f"❌ Error getting token: {e}")
        return None

def get_100_new_claude_posts():
    """Get 100 newest posts from r/ClaudeAI."""
    print("Getting 100 newest posts from r/ClaudeAI...")
    
    # Get access token
    token = get_reddit_token()
    make_dir_if_not_exists()
    if not token:
        print("Falling back to public API (no authentication)...")
        # Use public API as fallback
        url = "https://www.reddit.com/r/ClaudeAI/new.json"
        params = {'limit': 100}
        headers = {'User-Agent': 'ai_econ_data_scraper_simple/1.0 by ai_eco_data_man11'}
    else:
        # Use authenticated API
        url = "https://oauth.reddit.com/r/ClaudeAI/new"
        params = {'limit': 100}
        headers = {
            'User-Agent': 'ai_econ_data_scraper_simple/1.0 by ai_eco_data_man11',
            'Authorization': f'Bearer {token}'
        }
    
    try:
        # Get the posts
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Extract post data
        posts = []
        for post in data['data']['children']:
            post_data = post['data']
            posts.append({
                'title': post_data.get('title', ''),
                'author': post_data.get('author', ''),
                'score': post_data.get('score', 0),
                'num_comments': post_data.get('num_comments', 0),
                'created_utc': post_data.get('created_utc', 0),
                'url': post_data.get('url', ''),
                'permalink': post_data.get('permalink', ''),
                'selftext': post_data.get('selftext', '')
            })
        
        # Save to CSV
        df = pd.DataFrame(posts)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"100_new_claude_posts_{timestamp}.csv"
        df.to_csv(f"demo_data/{filename}", index=False)

        print(f"✅ Saved {len(posts)} posts to {filename}")
    
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def get_comments_for_latest_10_claude_posts():
    """Fetch comments for the 10 newest posts in r/ClaudeAI with authentication."""
    print("Getting comments for 10 newest posts in r/ClaudeAI...")

    token = get_reddit_token()
    make_dir_if_not_exists()
    if not token:
        print("❌ Cannot fetch comments without authentication.")
        return False

    # Step 1: Get 10 newest posts
    posts_url = "https://oauth.reddit.com/r/ClaudeAI/new"
    headers = {
        'User-Agent': 'ai_econ_data_scraper_simple/1.0 by ai_eco_data_man11',
        'Authorization': f'Bearer {token}'
    }
    params = {'limit': 10}

    try:
        response = requests.get(posts_url, params=params, headers=headers)
        response.raise_for_status()
        post_data = response.json()['data']['children']

        comments_all = []

        # Step 2: For each post, fetch comments
        for post in post_data:
            post_id = post['data']['id']  # this is the t3_abc123 part without the "t3_"
            title = post['data']['title']
            permalink = post['data']['permalink']
            full_post_url = f"https://www.reddit.com{permalink}"

            comments_url = f"https://oauth.reddit.com/comments/{post_id}"
            #if you want more than the comments on the OP you need to adjust depth: params={'limit': 100, 'depth': 3}
            comments_resp = requests.get(comments_url, headers=headers, params={'limit': 100})
            comments_resp.raise_for_status()
            comments_json = comments_resp.json()

            if len(comments_json) < 2:
                continue  # No comments

            comments = comments_json[1]['data']['children']
            for comment in comments:
                if comment['kind'] != 't1':
                    continue
                c_data = comment['data']
                comments_all.append({
                    'post_title': title,
                    'post_url': full_post_url,
                    'comment_author': c_data.get('author', ''),
                    'comment_body': c_data.get('body', ''),
                    'comment_score': c_data.get('score', 0),
                    'comment_created_utc': c_data.get('created_utc', 0),
                })

        # Save to CSV
        df = pd.DataFrame(comments_all)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"claude_comments_latest10_{timestamp}.csv"
        df.to_csv(f"demo_data/{filename}", index=False)

        print(f"✅ Saved {len(comments_all)} comments from 10 posts to {filename}")
        return True

    except Exception as e:
        print(f"❌ Error fetching comments: {e}")
        return False

def get_10_new_utah_posts_with_ai_keywords():
    """Use Reddit's search endpoint to get 10 newest posts from r/Utah mentioning AI or ChatGPT with authentication."""
    print("Getting posts in r/Utah with keywords 'AI' or 'ChatGPT'...")

    token = get_reddit_token()
    make_dir_if_not_exists()
    if not token:
        print("❌ Cannot search without authentication.")
        return False

    url = "https://oauth.reddit.com/r/Utah/search"
    headers = {
        'User-Agent': 'ai_econ_data_scraper_simple/1.0 by ai_eco_data_man11',
        'Authorization': f'Bearer {token}'
    }
    
    # Combine keywords with OR, and sort by new

    query = 'ai OR "chat gpt" OR chatgpt'
    params = {
        'q': query,
        'limit': 50,
        'restrict_sr': True,
        'sort': 'new'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        posts = []
        keyword_pattern = re.compile(r'\b(ai|chat\s?gpt)\b', re.IGNORECASE)
        for post in data['data']['children']:
            post_data = post['data']
            title = post_data.get('title', '')
            selftext = post_data.get('selftext', '')

            if keyword_pattern.search(title) or keyword_pattern.search(selftext):
                posts.append({
                    'title': title,
                    'author': post_data.get('author', ''),
                    'score': post_data.get('score', 0),
                    'num_comments': post_data.get('num_comments', 0),
                    'created_utc': post_data.get('created_utc', 0),
                    'url': post_data.get('url', ''),
                    'permalink': post_data.get('permalink', ''),
                    'selftext': selftext
                })

        if not posts:
            print("⚠️ No matching posts found.")
            return False

        # Save to CSV
        df = pd.DataFrame(posts)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"utah_ai_posts_{timestamp}.csv"
        df.to_csv(f"demo_data/{filename}", index=False)

        print(f"✅ Saved {len(posts)} posts to {filename}")
        return True

    except Exception as e:
        print(f"❌ Error during Reddit search request: {e}")
        return False

if __name__ == "__main__":
    get_100_new_claude_posts() 
    get_comments_for_latest_10_claude_posts()
    get_10_new_utah_posts_with_ai_keywords()