# Reddit Data Collection Scripts

This repository contains scripts for collecting Reddit data using the Reddit API.


- [Reddit Data Collection Scripts](#reddit-data-collection-scripts)
  - [Setup - Step 2 and 3 can be skipped but will have different functionality, see Notes for details](#setup---step-2-and-3-can-be-skipped-but-will-have-different-functionality-see-notes-for-details)
    - [1. Install Dependencies](#1-install-dependencies)
    - [2. Set Up Reddit API Credentials (you must have a Reddit account to do this)](#2-set-up-reddit-api-credentials-you-must-have-a-reddit-account-to-do-this)
    - [3. Create Environment File](#3-create-environment-file)
    - [4. Run Scripts](#4-run-scripts)
  - [Scripts](#scripts)
    - [`reddit_auth_test.py`](#reddit_auth_testpy)
    - [`claude_utah_posts_demo.py`](#claude_utah_posts_demopy)
    - [`praw_demo.py`](#praw_demopy)
  - [Output](#output)
  - [Notes](#notes)



## Setup - Step 2 and 3 can be skipped but will have different functionality, see Notes for details

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Reddit API Credentials (you must have a Reddit account to do this)

1. Go to https://www.reddit.com/prefs/apps 
2. Create a new app (select "script" type)
3. Enter any url into the redirect uri (You can use http://localhost:8080)
4. Note your `client_id` and `client_secret`

### 3. Create Environment File

Create a `.env` file in the root directory with your Reddit API credentials received in the previous step:

```
REDDIT_CLIENT_ID=your_client_id_hereKv
REDDIT_CLIENT_SECRET=your_client_secret_here
```
The `.env` file is ignored by git to protect your credentials

### 4. Run Scripts

```bash
# Run the Claude Utah posts demo
python demo_scripts/claude_utah_posts_demo.py
```

## Scripts
### `reddit_auth_test.py`

This script tests your Reddit API Credentials and will print whether they are valid to be used or not.

### `claude_utah_posts_demo.py`

This script performs three tasks:

1. Collects the 100 newest posts from **r/ClaudeAI**
2. Fetches comments for the 10 newest posts in **r/ClaudeAI**
3. Searches for the 50 newest posts in **r/Utah** with keywords like `"ai"` or `"chat gpt"` and then excluded matches like `"said"` or `"email"`

### `praw_demo.py`

This is the exact same as the `claude_utah_posts_demo.py` script except it uses the Python Reddit API Wrapper package named praw for simplification. This script will not run if you do not follow steps 2 & 3.

## Output

CSV files are saved to the `demo_data/` directory with timestamps.

## Notes

- Scripts will fall back to public reddit API if credentials are not provided
- Only the 100 new posts from Claude will be able to run without the credentials (not the comment or search funcitons).
- I figured it would be nice for someone to be able to run at least one of the use cases without registering with Reddit Dev.