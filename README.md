# Auto News - Jekyll Site

A Jekyll-based automated news aggregation site that fetches RSS feeds and generates posts.

## Security Improvements

This repository has undergone a security audit. See [SECURITY.md](SECURITY.md) for detailed information about vulnerabilities found and fixes applied.

### ⚠️ Action Required

**IMPORTANT**: The Supabase API key in `_includes/bot-tracker.html` has been exposed in the repository history and should be rotated immediately.

1. Go to your Supabase dashboard
2. Generate a new anon key
3. Update the key in `_includes/bot-tracker.html`
4. Verify Row-Level Security (RLS) policies are configured

## Setup

### Prerequisites

- Python 3.7+
- Jekyll (for building the site)

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (for news_bot.py):
```bash
cp .env.example .env
# Edit .env and add your DEEPSEEK_API_KEY
```

3. Run the news bot:
```bash
python scripts/news_bot.py
```

### Building the Site

```bash
jekyll build
jekyll serve
```

## Security Best Practices

- Never commit API keys or secrets to version control
- Use environment variables for sensitive configuration
- Keep dependencies up to date
- Run security scans regularly
- See [SECURITY.md](SECURITY.md) for more details

## Files

- `scripts/news_bot.py` - RSS feed aggregator with DeepSeek AI content rewriting
- `_includes/bot-tracker.html` - Bot detection tracking script
- `.env.example` - Example environment variables configuration
- `requirements.txt` - Python dependencies
- `SECURITY.md` - Security audit report and recommendations
