#!/usr/bin/env python3
"""
Advanced Gmail scanner for real internship applications
Searches comprehensively for actual job application emails
"""
import sys
import os
from dotenv import load_dotenv
import re
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def scan_gmail_comprehensively():
    """Comprehensive Gmail scan for real internship/job applications"""
    try:
        print("🔍 COMPREHENSIVE Gmail scan for your real internship applications...")
        
        from src.email_parser.gmail_service import GmailService
        
        # Initialize Gmail service
        gmail_service = GmailService()
        
        if not gmail_service or not gmail_service.service:
            print("❌ Gmail service not available")
            return []
            
        print("✅ Gmail service connected!")
        
        # Advanced search queries for internship/job applications
        search_queries = [
            # Application confirmations
            'subject:"thank you for applying"',
            'subject:"application received"',
            'subject:"your application"',
            'subject:"application confirmation"',
            'subject:"we have received your application"',
            
            # Internship specific
            'subject:"internship" "application"',
            'subject:"intern" "position"',
            'subject:"summer internship"',
            'subject:"graduate program"',
            
            # Interview invitations
            'subject:"interview" "invitation"',
            'subject:"interview" "scheduled"',
            'subject:"would like to interview"',
            'subject:"next steps"',
            
            # Job boards and platforms
            'from:linkedin.com "application"',
            'from:indeed.com "application"',
            'from:glassdoor.com "application"',
            'from:jobs.com "application"',
            
            # Company responses
            'subject:"position" "status"',
            'subject:"update" "application"',
            'subject:"regarding your"',
            
            # Rejection emails (also important to track)
            'subject:"unfortunately"',
            'subject:"not moving forward"',
            'subject:"not selected"',
            'subject:"thank you for your interest"'
        ]
        
        all_emails = []
        
        print(f"🔍 Running {len(search_queries)} advanced search queries...")
        
        for i, query in enumerate(search_queries):
            try:
                print(f"   Query {i+1}: {query[:50]}...")
                
                # Search with this query (last 6 months for comprehensive search)
                results = gmail_service.service.users().messages().list(
                    userId='me',
                    q=f'{query} newer_than:6m',
                    maxResults=50
                ).execute()
                
                messages = results.get('messages', [])
                print(f"      Found {len(messages)} emails")
                
                for msg in messages:
                    try:
                        # Get full message details
                        message = gmail_service.service.users().messages().get(
                            userId='me',
                            id=msg['id'],
                            format='full'
                        ).execute()
                        
                        # Extract email details
                        headers = message['payload'].get('headers', [])
                        
                        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                        date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
                        
                        # Get email body
                        body = ""
                        if 'parts' in message['payload']:
                            for part in message['payload']['parts']:
                                if part['mimeType'] == 'text/plain':
                                    if 'data' in part['body']:
                                        body = part['body']['data']
                                        break
                        elif message['payload'].get('body', {}).get('data'):
                            body = message['payload']['body']['data']
                        
                        # Decode body if present
                        if body:
                            import base64
                            try:
                                body = base64.urlsafe_b64decode(body).decode('utf-8')
                            except:
                                body = "Could not decode body"
                        
                        email_data = {
                            'id': msg['id'],
                            'subject': subject,
                            'sender': sender,
                            'date': date,
                            'body': body[:500],  # First 500 chars
                            'search_query': query
                        }
                        
                        # Avoid duplicates
                        if not any(e['id'] == msg['id'] for e in all_emails):
                            all_emails.append(email_data)
                            
                    except Exception as e:
                        print(f"      Error processing message: {e}")
                        continue
                        
            except Exception as e:
                print(f"   Error with query: {e}")
                continue
        
        print(f"\n📧 Total unique emails found: {len(all_emails)}")
        
        # Filter and categorize emails
        real_applications = []
        
        for email in all_emails:
            # Check if this looks like a real application email
            if is_real_application_email(email):
                company = extract_company_name(email)
                position = extract_position(email)
                
                real_applications.append({
                    'email_id': email['id'],
                    'subject': email['subject'],
                    'sender': email['sender'],
                    'date': email['date'],
                    'company': company,
                    'position': position,
                    'body_snippet': email['body'][:200],
                    'source_query': email['search_query']
                })
        
        print(f"✅ Identified {len(real_applications)} REAL application emails!")
        
        # Display found applications
        if real_applications:
            print("\n" + "="*80)
            print("🎯 YOUR REAL INTERNSHIP APPLICATIONS FOUND:")
            print("="*80)
            
            for i, app in enumerate(real_applications):
                print(f"\nApplication {i+1}:")
                print(f"  🏢 Company: {app['company']}")
                print(f"  💼 Position: {app['position']}")
                print(f"  📧 From: {app['sender']}")
                print(f"  📝 Subject: {app['subject']}")
                print(f"  📅 Date: {app['date']}")
                print(f"  📄 Snippet: {app['body_snippet']}...")
                print(f"  🔍 Found via: {app['source_query'][:50]}...")
        else:
            print("\n❌ No real application emails found.")
            print("💡 This could mean:")
            print("   1. You applied but companies didn't send confirmation emails")
            print("   2. Applications are older than 6 months")
            print("   3. Emails are in different Gmail labels/folders")
            print("   4. You used a different email address for applications")
        
        return real_applications
        
    except Exception as e:
        print(f"❌ Error scanning Gmail: {e}")
        return []

def is_real_application_email(email):
    """Check if email looks like a real job application"""
    subject = email['subject'].lower()
    sender = email['sender'].lower()
    body = email['body'].lower()
    
    # Skip promotional/marketing emails
    skip_patterns = [
        'unsubscribe', 'newsletter', 'survey', 'reward', 'prize',
        'marketing', 'promotion', 'offer expires', 'limited time',
        'click here', 'special offer', 'discount'
    ]
    
    for pattern in skip_patterns:
        if pattern in subject or pattern in body:
            return False
    
    # Look for real application indicators
    real_indicators = [
        'application received', 'thank you for applying', 'your application',
        'next steps', 'interview', 'position', 'role', 'intern',
        'hr@', 'careers@', 'recruiting@', 'talent@', 'jobs@'
    ]
    
    for indicator in real_indicators:
        if indicator in subject or indicator in sender or indicator in body:
            return True
    
    return False

def extract_company_name(email):
    """Extract company name from email"""
    sender = email['sender']
    subject = email['subject']
    
    # Extract from sender domain
    if '@' in sender:
        domain = sender.split('@')[-1].split('>')[0]
        # Remove common email domains
        if domain not in ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com']:
            company = domain.split('.')[0]
            return company.title()
    
    # Extract from sender name
    if '<' in sender:
        name_part = sender.split('<')[0].strip()
        if '|' in name_part:
            company = name_part.split('|')[-1].strip()
            return company
    
    # Extract from subject
    subject_words = subject.split()
    for word in subject_words:
        if len(word) > 3 and word.istitle():
            return word
    
    return "Unknown Company"

def extract_position(email):
    """Extract position title from email"""
    subject = email['subject'].lower()
    body = email['body'].lower()
    
    # Common position patterns
    position_patterns = [
        r'intern(?:ship)?.*?position',
        r'software.*?intern',
        r'data.*?intern',
        r'engineer.*?intern',
        r'graduate.*?program',
        r'summer.*?intern',
        r'.*?intern.*?role'
    ]
    
    text_to_search = f"{subject} {body}"
    
    for pattern in position_patterns:
        match = re.search(pattern, text_to_search)
        if match:
            return match.group().title()
    
    # Fallback patterns
    if 'intern' in subject:
        return "Internship Position"
    elif 'graduate' in subject:
        return "Graduate Position"
    
    return "Unknown Position"

if __name__ == "__main__":
    applications = scan_gmail_comprehensively()
    
    if applications:
        print(f"\n🎉 Ready to add {len(applications)} real applications to your tracker!")
        print("Would you like me to add these to your application tracker? (Run the next script)")
    else:
        print("\n💡 If no real applications were found, you may need to:")
        print("1. Check if you used a different email address")
        print("2. Look in Gmail's Promotions/Updates/Social tabs")
        print("3. Check if companies sent confirmation emails")
        print("4. Consider manual entry for applications without email confirmations")