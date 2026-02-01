# Scripts Directory

This directory contains automation scripts for the news aggregator.

## Available Scripts

### 1. `news_bot.py`

Main automation script that:
- Fetches news from RSS feeds (BBC, CNN)
- Rewrites articles using DeepSeek AI
- Publishes posts to Jekyll
- Submits new posts to Google Indexing API

**Usage:**
```bash
export DEEPSEEK_API_KEY="your-key"
export GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'
python scripts/news_bot.py
```

**Runs automatically:** Every 10 minutes via GitHub Actions

---

### 2. `check_indexing_api.py`

Health check script to verify Google Indexing API is configured correctly.

**Purpose:**
- Validate service account credentials
- Test API connectivity
- Submit a test URL
- Verify URL metadata retrieval

**Usage:**
```bash
export GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'
python scripts/check_indexing_api.py
```

**Via GitHub Actions:**
1. Go to "Actions" tab
2. Select "Indexing API Tools"
3. Click "Run workflow"
4. Choose "check_api"

**Output Example:**
```
============================================================
Google Indexing API - Health Check
============================================================

1. Checking credentials...
   ✅ Credentials configured for: bot@project.iam.gserviceaccount.com

2. Checking API access...
   ✅ Successfully connected to Google Indexing API

3. Testing URL submission...
   ✅ Successfully submitted test URL to Indexing API

4. Checking URL metadata...
   ✅ URL metadata found

============================================================
✅ All checks passed! Google Indexing API is working.
============================================================
```

---

### 3. `submit_old_urls.py`

Batch submission script to submit all existing posts to Google Indexing API.

**Purpose:**
- Submit posts that were created before indexing feature was added
- Re-submit posts if needed
- Track submission success/failure

**Features:**
- Scans all files in `_posts/` directory
- Generates proper URLs for each post
- Submits to Google Indexing API with rate limiting
- Shows progress and statistics

**Usage:**
```bash
export GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'
python scripts/submit_old_urls.py
```

**Via GitHub Actions:**
1. Go to "Actions" tab
2. Select "Indexing API Tools"
3. Click "Run workflow"
4. Choose "submit_old_urls"

**Output Example:**
```
======================================================================
Submit All Old URLs to Google Indexing API
======================================================================

✅ Connected to Google Indexing API
📁 Scanning posts directory: _posts
📊 Found 25 posts to submit

Starting submission...
----------------------------------------------------------------------
[1/25] ✅ 2026-01-31-news-article-one.md              | ✅ Success
[2/25] ✅ 2026-01-31-news-article-two.md              | ✅ Success
...
----------------------------------------------------------------------

======================================================================
Submission Summary
======================================================================
Total posts:      25
✅ Successful:    24 (96%)
❌ Failed:        1
⏭️  Skipped:       0
======================================================================
```

**Rate Limiting:**
- 0.5 seconds between requests
- 60 seconds pause every 50 requests
- Daily limit: 200 requests (Google API quota)

---

## Environment Variables

All scripts use these environment variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `DEEPSEEK_API_KEY` | For news_bot.py | DeepSeek API key for content rewriting |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | For indexing features | JSON credentials from Google Cloud Console |
| `SITE_BASE_URL` | Optional | Base URL for the site (default: https://mnam1ss.github.io/stunning-fiesta) |

## State File

`state.json` - Stores seen article IDs to prevent duplicates. Automatically managed by `news_bot.py`.

## Dependencies

Install with:
```bash
pip install requests google-auth google-api-python-client
```

## Troubleshooting

### "GOOGLE_SERVICE_ACCOUNT_JSON not set"
- Set the environment variable with your service account JSON
- In GitHub: Add as a secret in Settings → Secrets and variables → Actions

### "Permission denied" errors
1. Enable Indexing API in Google Cloud Console
2. Add service account email to Google Search Console as Owner
3. Grant "Indexing API Publisher" role to service account

### "Rate limit exceeded"
- Free tier: 200 requests/day
- Wait 24 hours for quota reset
- Or upgrade to paid tier in Google Cloud Console

### URLs not getting indexed
- Check that URLs are accessible publicly
- Verify domain ownership in Google Search Console
- Allow time for Google to crawl (indexing is not instant)
