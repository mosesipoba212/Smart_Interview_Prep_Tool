#!/usr/bin/env python3
"""
Check Gmail for internship application emails
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def check_gmail_for_applications():
    """Check Gmail for internship application emails"""
    try:
        print("🔍 Checking Gmail for internship application emails...")
        
        # Try to import Gmail service
        try:
            from src.email_parser.gmail_service import GmailService
            
            # Initialize Gmail service
            gmail_service = GmailService()
            
            if not gmail_service or not gmail_service.service:
                print("❌ Gmail service not available")
                print("💡 This could be because:")
                print("   - No credentials.json file")
                print("   - OAuth not completed")
                print("   - API keys not configured")
                return False
                
            print("✅ Gmail service connected successfully!")
            
            # Scan for interview/application emails in the last 60 days
            print("📧 Scanning for application emails (last 60 days)...")
            emails = gmail_service.scan_for_interviews(days_back=60)
            
            print(f"\n📊 Found {len(emails)} potential application-related emails:")
            print("-" * 80)
            
            if len(emails) == 0:
                print("❌ No application emails found in your Gmail!")
                print("\n💡 This could mean:")
                print("   1. Companies didn't send confirmation emails when you applied")
                print("   2. Emails are older than 60 days")
                print("   3. Emails are in different folders (Promotions, Updates, etc.)")
                print("   4. Email subjects don't match typical application patterns")
                return False
            
            # Show details of found emails
            for i, email in enumerate(emails[:10]):  # Show first 10
                print(f"\nEmail {i+1}:")
                print(f"  📧 From: {email.get('sender', 'Unknown')}")
                print(f"  📝 Subject: {email.get('subject', 'No subject')}")
                print(f"  📅 Date: {email.get('date', 'No date')}")
                print(f"  🏢 Company: {email.get('company', 'Unknown')}")
                print(f"  💼 Position: {email.get('position', 'Unknown')}")
                print(f"  📄 Snippet: {email.get('body', '')[:100]}...")
                
            return True
            
        except ImportError as e:
            print(f"❌ Cannot import Gmail service: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking Gmail: {e}")
        return False

def check_manual_application_tracking():
    """Check if we can manually add the 15 applications"""
    print("\n" + "="*60)
    print("💡 ALTERNATIVE SOLUTION:")
    print("="*60)
    print("Since the Gmail auto-detection isn't finding your applications,")
    print("you can manually add your 15 internship applications!")
    print("")
    print("Options:")
    print("1. 📝 Manual Entry: Add each application through the web interface")
    print("2. 📊 Bulk Import: Create a CSV file and import all at once")
    print("3. 🔧 Custom Script: Create a script to add them programmatically")
    print("")
    print("Would you like me to help you with any of these options?")

if __name__ == "__main__":
    # Check Gmail first
    gmail_found = check_gmail_for_applications()
    
    # If Gmail doesn't have the data, suggest manual tracking
    if not gmail_found:
        check_manual_application_tracking()