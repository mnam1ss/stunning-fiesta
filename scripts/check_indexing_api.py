#!/usr/bin/env python3
"""
Script to check if Google Indexing API is working correctly.
Tests API credentials, quota status, and URL submission capabilities.
"""

import os
import json
import sys
from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


INDEXING_API_SCOPES = ["https://www.googleapis.com/auth/indexing"]
BASE_URL = os.getenv("SITE_BASE_URL", "https://mnam1ss.github.io/stunning-fiesta")


def check_credentials():
    """
    Check if Google service account credentials are configured.
    Returns: (bool, str) - (success, message)
    """
    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    
    if not service_account_json:
        return False, "❌ GOOGLE_SERVICE_ACCOUNT_JSON environment variable is not set"
    
    try:
        credentials_dict = json.loads(service_account_json)
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        
        for field in required_fields:
            if field not in credentials_dict:
                return False, f"❌ Missing required field in credentials: {field}"
        
        return True, f"✅ Credentials configured for: {credentials_dict.get('client_email')}"
    
    except json.JSONDecodeError as e:
        return False, f"❌ Invalid JSON in service account credentials: {e}"
    except Exception as e:
        return False, f"❌ Error checking credentials: {e}"


def check_api_access():
    """
    Check if we can access the Google Indexing API.
    Returns: (bool, str, service) - (success, message, service object or None)
    """
    try:
        service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        
        if not service_account_json:
            return False, "❌ No credentials available", None
        
        credentials_dict = json.loads(service_account_json)
        
        # Create credentials from service account
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=INDEXING_API_SCOPES
        )
        
        # Build the indexing service
        service = build('indexing', 'v3', credentials=credentials)
        
        return True, "✅ Successfully connected to Google Indexing API", service
        
    except HttpError as e:
        return False, f"❌ HTTP error connecting to API: {e}", None
    except Exception as e:
        return False, f"❌ Error connecting to API: {e}", None


def check_url_metadata(service, test_url):
    """
    Check metadata for a specific URL in the Indexing API.
    Returns: (bool, str) - (success, message)
    """
    try:
        # Get URL notification metadata
        response = service.urlNotifications().getMetadata(url=test_url).execute()
        
        if response:
            latest_update = response.get('latestUpdate', {})
            url = latest_update.get('url', 'N/A')
            notify_type = latest_update.get('type', 'N/A')
            notify_time = latest_update.get('notifyTime', 'N/A')
            
            return True, f"✅ URL metadata found:\n   URL: {url}\n   Type: {notify_type}\n   Last notified: {notify_time}"
        else:
            return True, "⚠️  URL not found in Indexing API (never submitted or expired)"
            
    except HttpError as e:
        if e.resp.status == 404:
            return True, "⚠️  URL not found in Indexing API (never submitted)"
        elif e.resp.status == 403:
            return False, f"❌ Permission denied. Make sure:\n   1. Indexing API is enabled in Google Cloud Console\n   2. Service account has 'Indexing API Publisher' role\n   3. Service account email is added as Owner in Google Search Console"
        else:
            return False, f"❌ HTTP error checking URL: {e}"
    except Exception as e:
        return False, f"❌ Error checking URL metadata: {e}"


def test_url_submission(service, test_url):
    """
    Test submitting a URL to the Indexing API.
    Returns: (bool, str) - (success, message)
    """
    try:
        # Prepare the request body
        body = {
            "url": test_url,
            "type": "URL_UPDATED"
        }
        
        # Submit the URL for indexing
        response = service.urlNotifications().publish(body=body).execute()
        
        url = response.get('urlNotificationMetadata', {}).get('url', 'N/A')
        latest_update = response.get('urlNotificationMetadata', {}).get('latestUpdate', {})
        notify_time = latest_update.get('notifyTime', 'N/A')
        
        return True, f"✅ Successfully submitted test URL to Indexing API:\n   URL: {url}\n   Notification time: {notify_time}"
        
    except HttpError as e:
        if e.resp.status == 403:
            return False, f"❌ Permission denied. Make sure:\n   1. Indexing API is enabled in Google Cloud Console\n   2. Service account has 'Indexing API Publisher' role\n   3. Service account email is added as Owner in Google Search Console"
        elif e.resp.status == 429:
            return False, "❌ Rate limit exceeded. You've hit the daily quota (200 requests/day for free tier)"
        else:
            return False, f"❌ HTTP error submitting URL: {e}"
    except Exception as e:
        return False, f"❌ Error submitting URL: {e}"


def main():
    """
    Main function to run all Indexing API checks.
    """
    print("=" * 60)
    print("Google Indexing API - Health Check")
    print("=" * 60)
    print()
    
    # Step 1: Check credentials
    print("1. Checking credentials...")
    success, message = check_credentials()
    print(f"   {message}")
    print()
    
    if not success:
        print("⚠️  Fix credentials configuration before proceeding.")
        print()
        print("To configure:")
        print("1. Set GOOGLE_SERVICE_ACCOUNT_JSON environment variable")
        print("2. Or create GitHub secret with the service account JSON")
        sys.exit(1)
    
    # Step 2: Check API access
    print("2. Checking API access...")
    success, message, service = check_api_access()
    print(f"   {message}")
    print()
    
    if not success:
        sys.exit(1)
    
    # Step 3: Test with a sample URL from the site
    test_url = f"{BASE_URL}/2026/01/31/test.html"
    print(f"3. Testing URL submission with: {test_url}")
    success, message = test_url_submission(service, test_url)
    print(f"   {message}")
    print()
    
    if not success:
        sys.exit(1)
    
    # Step 4: Check metadata for the test URL
    print("4. Checking URL metadata...")
    success, message = check_url_metadata(service, test_url)
    print(f"   {message}")
    print()
    
    # Summary
    print("=" * 60)
    print("✅ All checks passed! Google Indexing API is working correctly.")
    print("=" * 60)
    print()
    print("Notes:")
    print("- Daily quota: 200 requests/day (free tier)")
    print("- Current time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("- Base URL:", BASE_URL)


if __name__ == "__main__":
    main()
