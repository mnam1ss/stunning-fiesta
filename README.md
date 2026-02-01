# Auto News - Automated News Aggregator with Google Indexing

This repository automatically fetches news from RSS feeds, rewrites them using DeepSeek AI, and publishes them as Jekyll posts. **New posts are instantly submitted to Google Indexing API** for faster search engine indexing.

## Features

- 📰 Fetches news from BBC and CNN RSS feeds every 10 minutes
- 🤖 Rewrites articles using DeepSeek AI to create original content
- 📝 Publishes posts to a Jekyll-based GitHub Pages site
- ⚡ **Instantly submits new posts to Google Indexing API** (no delay!)
- 🔄 Maintains state to avoid duplicate posts

## Setup

### 1. DeepSeek API Key

Set the `DEEPSEEK_API_KEY` secret in your GitHub repository:
- Go to Settings → Secrets and variables → Actions
- Add a new secret named `DEEPSEEK_API_KEY`
- Paste your DeepSeek API key

### 2. Google Indexing API Setup

To enable instant indexing with Google:

#### Step 1: Create a Service Account
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable the **Indexing API**:
   - Go to APIs & Services → Library
   - Search for "Indexing API"
   - Click "Enable"

#### Step 2: Create Service Account Credentials
1. Go to APIs & Services → Credentials
2. Click "Create Credentials" → "Service Account"
3. Name it (e.g., "indexing-bot")
4. Grant it the role: "Indexing API Publisher"
5. Click "Done"
6. Click on the created service account
7. Go to "Keys" tab → "Add Key" → "Create new key"
8. Choose "JSON" format and download the file

#### Step 3: Add Service Account to Search Console
1. Copy the email address from the JSON file (looks like `xyz@project.iam.gserviceaccount.com`)
2. Go to [Google Search Console](https://search.google.com/search-console)
3. Select your property
4. Go to Settings → Users and permissions
5. Add the service account email as an **Owner**

#### Step 4: Add Secret to GitHub
1. Open the downloaded JSON file
2. Copy its entire contents (the whole JSON object)
3. Go to your GitHub repository → Settings → Secrets and variables → Actions
4. Add a new secret named `GOOGLE_SERVICE_ACCOUNT_JSON`
5. Paste the JSON contents as the value

### Configuration

Edit `scripts/news_bot.py` to customize:
- `FEEDS`: Add or remove RSS feed URLs
- `MAX_POSTS_PER_RUN`: Number of posts to create per run (default: 1)
- `BASE_URL`: Your GitHub Pages URL (default: https://mnam1ss.github.io/stunning-fiesta)

## How It Works

1. **Fetch**: The bot fetches RSS feeds from configured sources
2. **Filter**: Checks against seen posts (stored in `scripts/state.json`)
3. **Rewrite**: Uses DeepSeek AI to create original content
4. **Publish**: Creates a Jekyll markdown post in `_posts/`
5. **Index**: **Instantly submits the new post URL to Google Indexing API**
6. **Commit**: GitHub Actions commits and pushes the changes

## Workflow

The automation runs via GitHub Actions:
- **Schedule**: Every 10 minutes
- **Manual**: Can be triggered manually via "Actions" tab

## Dependencies

- `requests`: HTTP requests for RSS feeds and DeepSeek API
- `google-auth`: Authentication for Google APIs
- `google-api-python-client`: Google Indexing API client

## Notes

- The Indexing API helps Google discover your content faster
- Submission happens instantly after post creation (no delay)
- If the service account JSON is not configured, the bot will still work but skip indexing
- The API has quotas: 200 requests per day for free

## License

Open source - feel free to use and modify!
