# Reddit Data Collection Scripts

This repository contains scripts for collecting Reddit data using the Reddit API.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Reddit API Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Create a new app (select "script" type)
3. Note your `client_id` and `client_secret`

### 3. Create Environment File

Create a `.env` file in the root directory with your Reddit API credentials:

```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
```

### 4. Run Scripts

```bash
# Run the Claude Utah posts demo
python demo_scripts/claude_utah_posts_demo.py
```

## Scripts

- `demo_scripts/claude_utah_posts_demo.py` - Collects posts from r/ClaudeAI and r/Utah
- `test_scripts/` - Additional test and analysis scripts

## Output

CSV files are saved to the `demo_data/` directory with timestamps.

## Notes

- The `.env` file is ignored by git to protect your credentials
- Scripts will fall back to public API if credentials are not provided
- Some features require authentication (like comment collection) 