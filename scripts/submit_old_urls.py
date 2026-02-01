#!/usr/bin/env python3
"""
Script to submit all old URLs (existing posts) to Google Indexing API.
This ensures all previously published posts are indexed by Google.
"""

import os
import json
import time
import re
from datetime import datetime
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


POSTS_DIR = "_posts"
INDEXING_API_SCOPES = ["https://www.googleapis.com/auth/indexing"]
BASE_URL = os.getenv("SITE_BASE_URL", "https://mnam1ss.github.io/stunning-fiesta")

# Rate limiting settings
BATCH_SIZE = 50  # Process in batches
DELAY_BETWEEN_REQUESTS = 0.5  # Seconds between requests (to avoid rate limiting)
DELAY_BETWEEN_BATCHES = 60  # Seconds between batches


def get_post_url(filename):
    """
    Converts a post filename to its public URL.
    Example: 2026-01-31-some-title-120000.md -> https://mnam1ss.github.io/stunning-fiesta/2026/01/31/some-title-120000.html
    """
    basename = os.path.basename(filename).replace('.md', '')
    parts = basename.split('-')
    
    if len(parts) >= 3:
        year = parts[0]
        month = parts[1]
        day = parts[2]
        slug = '-'.join(parts[3:])
        
        return f"{BASE_URL}/{year}/{month}/{day}/{slug}.html"
    
    # Fallback
    return f"{BASE_URL}/{basename}.html"


def get_all_post_files():
    """
    Get all post markdown files from the _posts directory.
    Returns: list of file paths
    """
    posts_path = Path(POSTS_DIR)
    
    if not posts_path.exists():
        print(f"❌ Posts directory not found: {POSTS_DIR}")
        return []
    
    # Get all .md files
    post_files = list(posts_path.glob("*.md"))
    return sorted(post_files)


def setup_indexing_service():
    """
    Setup Google Indexing API service.
    Returns: service object or None
    """
    try:
        service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        
        if not service_account_json:
            print("❌ GOOGLE_SERVICE_ACCOUNT_JSON environment variable is not set")
            return None
        
        credentials_dict = json.loads(service_account_json)
        
        # Create credentials from service account
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=INDEXING_API_SCOPES
        )
        
        # Build the indexing service
        service = build('indexing', 'v3', credentials=credentials)
        
        print("✅ Connected to Google Indexing API")
        return service
        
    except Exception as e:
        print(f"❌ Error setting up Indexing API: {e}")
        return None


def submit_url(service, url):
    """
    Submit a single URL to Google Indexing API.
    Returns: (bool, str) - (success, message)
    """
    try:
        body = {
            "url": url,
            "type": "URL_UPDATED"
        }
        
        response = service.urlNotifications().publish(body=body).execute()
        return True, "✅ Success"
        
    except HttpError as e:
        if e.resp.status == 403:
            return False, "❌ Permission denied"
        elif e.resp.status == 429:
            return False, "❌ Rate limit exceeded"
        elif e.resp.status == 400:
            return False, "❌ Bad request"
        else:
            return False, f"❌ HTTP {e.resp.status}"
    except Exception as e:
        return False, f"❌ Error: {str(e)[:50]}"


def main():
    """
    Main function to submit all old URLs.
    """
    print("=" * 70)
    print("Submit All Old URLs to Google Indexing API")
    print("=" * 70)
    print()
    
    # Setup service
    service = setup_indexing_service()
    if not service:
        print("\n⚠️  Cannot proceed without valid API credentials.")
        return
    
    # Get all post files
    print(f"📁 Scanning posts directory: {POSTS_DIR}")
    post_files = get_all_post_files()
    
    if not post_files:
        print("⚠️  No posts found to submit.")
        return
    
    print(f"📊 Found {len(post_files)} posts to submit")
    print()
    
    # Statistics
    total = len(post_files)
    successful = 0
    failed = 0
    skipped = 0
    
    # Process all posts
    print("Starting submission...")
    print("-" * 70)
    
    for i, post_file in enumerate(post_files, 1):
        url = get_post_url(str(post_file))
        
        # Progress indicator
        progress = f"[{i}/{total}]"
        
        # Submit URL
        success, message = submit_url(service, url)
        
        if success:
            successful += 1
            status_icon = "✅"
        else:
            failed += 1
            status_icon = "❌"
            
            # If rate limited, pause and retry
            if "rate limit" in message.lower():
                print(f"{progress} ⏸️  Rate limit hit. Pausing for {DELAY_BETWEEN_BATCHES}s...")
                time.sleep(DELAY_BETWEEN_BATCHES)
                
                # Retry
                success, message = submit_url(service, url)
                if success:
                    successful += 1
                    failed -= 1
                    status_icon = "✅"
        
        # Print status
        filename = os.path.basename(post_file)
        print(f"{progress} {status_icon} {filename[:50]:<50} | {message}")
        
        # Rate limiting delay
        if i < total:
            time.sleep(DELAY_BETWEEN_REQUESTS)
        
        # Batch delay (every BATCH_SIZE requests)
        if i % BATCH_SIZE == 0 and i < total:
            print(f"\n⏸️  Batch {i // BATCH_SIZE} complete. Pausing {DELAY_BETWEEN_BATCHES}s to respect rate limits...\n")
            time.sleep(DELAY_BETWEEN_BATCHES)
    
    # Summary
    print("-" * 70)
    print()
    print("=" * 70)
    print("Submission Summary")
    print("=" * 70)
    print(f"Total posts:      {total}")
    print(f"✅ Successful:    {successful} ({successful * 100 // total if total > 0 else 0}%)")
    print(f"❌ Failed:        {failed}")
    print(f"⏭️  Skipped:       {skipped}")
    print("=" * 70)
    print()
    
    if failed > 0:
        print("⚠️  Some URLs failed to submit. Common reasons:")
        print("   - Rate limit exceeded (200 requests/day limit)")
        print("   - Permission issues (check Search Console settings)")
        print("   - Network errors (temporary, try again later)")
        print()
    
    print(f"✅ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
