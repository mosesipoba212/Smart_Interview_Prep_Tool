#!/usr/bin/env python3
"""
Check what emails are actually in Gmail to find real job applications
"""
import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.email_parser.gmail_service import GmailService

def check_gmail_emails():
    """Check what emails are actually in Gmail"""
    try:
        print("🔍 Checking Gmail emails...")
        gmail_service = GmailService()
        
        if not gmail_service or not gmail_service.service:
            print("❌ Gmail service not available")
            return
            
        # Get recent emails to see what we're working with
        print("📧 Scanning recent emails...")
        emails = gmail_service.scan_for_interviews(days_back=30)
        
        print(f"\n📊 Found {len(emails)} potential interview emails:")
        print("-" * 80)
        
        for i, email in enumerate(emails[:10]):  # Show first 10 emails
            print(f"Email {i+1}:")
            print(f"  From: {email.get('sender', 'Unknown')}")
            print(f"  Subject: {email.get('subject', 'No subject')}")
            print(f"  Date: {email.get('date', 'No date')}")
            print(f"  Company: {email.get('company', 'Unknown')}")
            print(f"  Interview Date: {email.get('interview_date', 'Not found')}")
            print(f"  Snippet: {email.get('body', '')[:100]}...")
            print("-" * 40)
        
    except Exception as e:
        print(f"❌ Error checking Gmail: {e}")

if __name__ == "__main__":
    check_gmail_emails()