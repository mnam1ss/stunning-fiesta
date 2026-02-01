# How to Check & Submit URLs to Google Indexing API

This guide explains how to use the new Indexing API tools.

## Quick Start

### Check if Indexing API is Working

1. Go to your repository on GitHub
2. Click the **"Actions"** tab at the top
3. Click **"Indexing API Tools"** in the left sidebar
4. Click the **"Run workflow"** button (top right)
5. Select **"check_api"** from the dropdown
6. Click **"Run workflow"**
7. Wait a few seconds, then click on the workflow run to see results

**What it checks:**
- ✅ Your Google service account credentials are valid
- ✅ Can connect to Google Indexing API
- ✅ Can submit URLs successfully
- ✅ Can retrieve URL status

### Submit All Old URLs to Google

1. Go to your repository on GitHub
2. Click the **"Actions"** tab at the top
3. Click **"Indexing API Tools"** in the left sidebar
4. Click the **"Run workflow"** button (top right)
5. Select **"submit_old_urls"** from the dropdown
6. Click **"Run workflow"**
7. The workflow will submit all existing posts to Google Indexing API

**What it does:**
- 📊 Finds all posts in `_posts/` directory
- 📤 Submits each URL to Google Indexing API
- ⏱️ Respects rate limits (0.5s between requests)
- 📈 Shows progress and statistics

## Expected Results

### Successful Check Output

```
============================================================
Google Indexing API - Health Check
============================================================

1. Checking credentials...
   ✅ Credentials configured for: your-bot@project.iam.gserviceaccount.com

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

### Successful Batch Submission Output

```
======================================================================
Submit All Old URLs to Google Indexing API
======================================================================

✅ Connected to Google Indexing API
📁 Scanning posts directory: _posts
📊 Found 25 posts to submit

Starting submission...
----------------------------------------------------------------------
[1/25] ✅ 2026-01-31-article-one.md     | ✅ Success
[2/25] ✅ 2026-01-31-article-two.md     | ✅ Success
[3/25] ✅ 2026-01-31-article-three.md   | ✅ Success
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

✅ Completed at: 2026-02-01 10:30:45
```

## Common Issues

### ❌ "GOOGLE_SERVICE_ACCOUNT_JSON not set"

**Problem:** Service account credentials are not configured.

**Solution:**
1. Go to Settings → Secrets and variables → Actions
2. Add a secret named `GOOGLE_SERVICE_ACCOUNT_JSON`
3. Paste your entire service account JSON as the value
4. See main README.md for detailed setup instructions

### ❌ "Permission denied"

**Problem:** Service account doesn't have proper permissions.

**Solution:**
1. Enable "Indexing API" in Google Cloud Console
2. Add service account email as **Owner** in Google Search Console
3. Grant "Indexing API Publisher" role to service account

### ❌ "Rate limit exceeded"

**Problem:** You've hit the daily quota (200 requests/day for free tier).

**Solution:**
- Wait 24 hours for quota to reset
- Or upgrade to paid tier in Google Cloud Console
- The script automatically handles rate limiting with pauses

### ⚠️ "URL not found in Indexing API"

**Not necessarily a problem!** This means:
- URL was never submitted before, OR
- URL was submitted but expired from cache

This is expected for old URLs that haven't been submitted yet. Running the "submit_old_urls" action will fix this.

## Rate Limits & Quotas

### Free Tier Limits
- **200 requests per day**
- Quota resets at midnight Pacific Time
- Shared across all API operations (submit + check)

### Script Rate Limiting
The `submit_old_urls.py` script includes built-in rate limiting:
- 0.5 seconds between each request
- 60 seconds pause every 50 requests
- Shows progress for each submission

**Example:** Submitting 100 URLs takes approximately:
- (100 × 0.5s) + (2 batches × 60s) = 50s + 120s = ~3 minutes

## When to Use Each Tool

### Use "check_api" when:
- ✅ You just configured the API for the first time
- ✅ You're troubleshooting indexing issues
- ✅ You want to verify credentials are working
- ✅ You changed service account settings

### Use "submit_old_urls" when:
- ✅ You just enabled the Indexing API feature
- ✅ You have existing posts that weren't submitted yet
- ✅ You want to re-submit all URLs after fixing configuration
- ✅ You migrated from another domain

## Automatic Indexing for New Posts

New posts are **automatically submitted** to Google Indexing API when they're created by `news_bot.py`. You don't need to do anything!

The tools in this guide are for:
1. **Checking** if the API is working correctly
2. **Submitting old posts** that existed before you enabled indexing

## Need Help?

1. Check the [main README.md](../README.md) for setup instructions
2. Check [scripts/README.md](scripts/README.md) for technical details
3. Review GitHub Actions logs for detailed error messages
4. Verify your Google Cloud Console and Search Console settings

## Next Steps After Running Tools

1. ✅ Run "check_api" to verify everything works
2. ✅ Run "submit_old_urls" to submit existing posts
3. ✅ Monitor your Google Search Console for indexing status
4. ✅ New posts will be automatically submitted going forward

**Note:** Indexing is not instant. It may take hours or days for Google to actually crawl and index your URLs after submission. The Indexing API just notifies Google that your content exists.
