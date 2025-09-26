"""
Gmail Service Module
Handles Gmail API integration for parsing recruiter emails
"""

import os
import re
import base64
from datetime import datetime, timedelta
from typing import List, Dict, Any
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup

class GmailService:
    """Gmail API service for interview email processing"""
    
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.modify'
    ]
    
    def __init__(self):
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Gmail API with enhanced error handling"""
        creds = None
        
        # Check for existing token
        if os.path.exists('token.json'):
            try:
                creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
                print("✅ Found existing Gmail token")
            except Exception as e:
                print(f"⚠️  Error reading token.json: {e}")
                # Remove corrupted token
                try:
                    os.remove('token.json')
                except:
                    pass
                creds = None
        
        # If no valid credentials, request authorization
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    print("✅ Gmail token refreshed successfully")
                except Exception as e:
                    print(f"⚠️  Error refreshing token: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists('credentials.json'):
                    print("⚠️  credentials.json not found - Gmail will use mock data")
                    return None
                
                try:
                    print("🔑 Starting Gmail OAuth flow...")
                    print("⚠️  Note: App is in testing mode - contact developer for access")
                    print("🌐 Opening browser for authentication...")
                    print("⏰ You have 5 minutes to complete authentication")
                    
                    try:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            'credentials.json', self.SCOPES)
                        # Use port 8080 to match your Google Cloud Console setting
                        creds = flow.run_local_server(port=8080, open_browser=True)
                        print("✅ Gmail authentication successful!")
                    except Exception as auth_error:
                        if "access_denied" in str(auth_error) or "403" in str(auth_error):
                            print("❌ Gmail app not verified by Google")
                            print("💡 Using mock email data for demonstration")
                        else:
                            print(f"❌ Gmail authentication failed: {auth_error}")
                        return None
                        
                except Exception as e:
                    print(f"❌ Gmail OAuth setup failed: {e}")
                    print("💡 Using mock email data for demonstration")
                    return None
        
        # Save credentials for future use
        if creds:
            try:
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
                print("💾 Gmail credentials saved")
            except Exception as e:
                print(f"⚠️  Could not save credentials: {e}")
        
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            print("🔗 Gmail service connected successfully")
            return self.service
        except Exception as e:
            print(f"❌ Failed to build Gmail service: {e}")
            return None
    
    def fetch_recent_emails(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Fetch recent emails that might contain interview invitations"""
        if not self.service:
            return []
        
        try:
            # Calculate date range
            since_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y/%m/%d')
            
            # Search query for potential interview emails
            query = f'after:{since_date} (subject:interview OR subject:"phone call" OR subject:meeting OR subject:"video call" OR subject:screening OR body:interview OR body:"schedule a call" OR body:"available for")'
            
            # Get message list
            result = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=50
            ).execute()
            
            messages = result.get('messages', [])
            emails = []
            
            for message in messages:
                email_data = self.get_email_details(message['id'])
                if email_data:
                    emails.append(email_data)
            
            print(f"📧 Found {len(emails)} potential interview emails")
            return emails
            
        except HttpError as error:
            print(f"❌ Error fetching emails: {error}")
            return []
    
    def get_email_details(self, message_id: str) -> Dict[str, Any]:
        """Get detailed information from a specific email"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            # Extract headers
            headers = {header['name']: header['value'] 
                      for header in message['payload'].get('headers', [])}
            
            # Extract body
            body = self.extract_email_body(message['payload'])
            
            return {
                'id': message_id,
                'subject': headers.get('Subject', ''),
                'sender': headers.get('From', ''),
                'date': headers.get('Date', ''),
                'body': body,
                'headers': headers
            }
            
        except HttpError as error:
            print(f"❌ Error getting email details: {error}")
            return None
    
    def extract_email_body(self, payload: Dict) -> str:
        """Extract text body from email payload"""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body += base64.urlsafe_b64decode(data).decode('utf-8')
                elif part['mimeType'] == 'text/html':
                    data = part['body']['data']
                    html_content = base64.urlsafe_b64decode(data).decode('utf-8')
                    # Convert HTML to text
                    soup = BeautifulSoup(html_content, 'html.parser')
                    body += soup.get_text()
        else:
            if payload['mimeType'] == 'text/plain':
                data = payload['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8')
            elif payload['mimeType'] == 'text/html':
                data = payload['body']['data']
                html_content = base64.urlsafe_b64decode(data).decode('utf-8')
                soup = BeautifulSoup(html_content, 'html.parser')
                body = soup.get_text()
        
        return body
    
    def scan_for_interviews(self, days_back: int = 14) -> List[Dict[str, Any]]:
        """Scan emails for interview opportunities with enhanced parsing"""
        try:
            # Use the existing fetch_recent_emails method
            emails = self.fetch_recent_emails(days_back=days_back)
            
            # Filter for interview-related emails
            interview_emails = []
            interview_keywords = [
                'interview', 'phone screen', 'technical round', 'hiring manager',
                'coding challenge', 'final round', 'onsite', 'video call',
                'assessment', 'evaluation', 'selection process', 'schedule',
                'available for', 'meeting request', 'call with', 'conversation'
            ]
            
            for email in emails:
                # Check if email contains interview keywords
                subject_lower = email.get('subject', '').lower()
                body_lower = email.get('body', '').lower()
                
                if any(keyword in subject_lower or keyword in body_lower for keyword in interview_keywords):
                    # Parse detailed interview information
                    interview_details = self.parse_interview_details(email)
                    
                    interview_emails.append({
                        'id': email.get('id'),
                        'subject': email.get('subject'),
                        'sender': email.get('sender'),
                        'email_date': email.get('date'),
                        'snippet': email.get('body', '')[:200] + '...' if len(email.get('body', '')) > 200 else email.get('body', ''),
                        'type': 'interview_invitation',
                        # Enhanced details
                        'company': interview_details['company'],
                        'position': interview_details['position'],
                        'interview_date': interview_details['date'],
                        'interview_time': interview_details.get('time', 'Time TBD'),
                        'platform': interview_details['platform'],
                        'interviewer': interview_details['interviewer'],
                        'status': 'pending',  # Default status
                        'priority': self.determine_email_priority(email)
                    })
            
            print(f"📧 Found {len(interview_emails)} interview-related emails")
            return interview_emails
            
        except Exception as e:
            print(f"❌ Error scanning for interviews: {e}")
            return []
    
    def parse_interview_details(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """Parse interview details from email content"""
        subject = email.get('subject', '').lower()
        body = email.get('body', '').lower()
        sender = email.get('sender', '')
        
        # Extract company name from sender email
        company = self.extract_company_name(sender)
        
        # Extract position/role
        position = self.extract_position(subject, body)
        
        # Extract interview date/time
        interview_date = self.extract_interview_date(body)
        interview_time = self.extract_interview_time(body)
        
        # Extract meeting platform
        platform = self.extract_meeting_platform(body)
        
        # Extract interviewer name
        interviewer = self.extract_interviewer_name(email)
        
        return {
            'company': company,
            'position': position,
            'date': interview_date,
            'time': interview_time,
            'platform': platform,
            'interviewer': interviewer,
            'subject': email.get('subject', ''),
            'sender': sender,
            'email_id': email.get('id')
        }
    
    def extract_company_name(self, sender_email: str) -> str:
        """Extract company name from sender email"""
        # Try to extract from email domain
        if '@' in sender_email:
            domain = sender_email.split('@')[-1].lower()
            # Remove common email domains and subdomains
            if domain not in ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'icloud.com']:
                # Handle subdomains (e.g., recruiting.company.com)
                domain_parts = domain.split('.')
                if len(domain_parts) >= 2:
                    # Skip common subdomains
                    if domain_parts[0] in ['www', 'mail', 'email', 'recruiting', 'hr', 'careers', 'jobs']:
                        if len(domain_parts) > 2:
                            company = domain_parts[1]
                        else:
                            company = domain_parts[0]
                    else:
                        company = domain_parts[0]
                    
                    # Clean up and format company name
                    company = company.replace('-', ' ').replace('_', ' ')
                    return company.title()
        
        # Try to extract from sender name part
        if '<' in sender_email:
            name_part = sender_email.split('<')[0].strip()
            # Look for company indicators in name
            company_indicators = ['HR', 'Recruiting', 'Talent', 'People', 'Team']
            for indicator in company_indicators:
                if indicator in name_part:
                    parts = name_part.split()
                    for i, part in enumerate(parts):
                        if indicator.lower() in part.lower() and i > 0:
                            return parts[i-1]
        
        return "Unknown Company"
    
    def extract_position(self, subject: str, body: str) -> str:
        """Extract job position from email content"""
        # Common position keywords
        position_patterns = [
            r'(?:for|as|the)\s+([a-zA-Z\s]+(?:engineer|developer|manager|analyst|designer|lead|director|coordinator|specialist))',
            r'(?:position|role):\s*([a-zA-Z\s]+)',
            r'([a-zA-Z\s]+(?:engineer|developer|manager|analyst|designer|lead|director))\s+(?:position|role|opportunity)'
        ]
        
        text = f"{subject} {body}"
        
        for pattern in position_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip().title()
        
        return "Unknown Position"
    
    def extract_interview_date(self, body: str) -> str:
        """Extract interview date from email body"""
        # Enhanced date patterns
        date_patterns = [
            r'(?:on|for|scheduled?\s+for)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday),?\s+([a-zA-Z]+\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s+\d{4})?)',
            r'(\d{1,2}/\d{1,2}/\d{2,4})',
            r'(\d{4}-\d{1,2}-\d{1,2})',
            r'([a-zA-Z]+\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4})',
            r'(\d{1,2}\s+[a-zA-Z]+\s+\d{4})',
            r'(?:available|free)\s+(?:on\s+)?([a-zA-Z]+\s+\d{1,2}(?:st|nd|rd|th)?)',
            r'(?:next|this)\s+(monday|tuesday|wednesday|thursday|friday)',
            r'tomorrow|today',
            r'(\d{1,2}(?:st|nd|rd|th)?\s+of\s+[a-zA-Z]+)'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                date_str = match.group(1) if match.lastindex and match.lastindex > 0 else match.group(0)
                return date_str.strip()
        
        return "Date TBD"
    
    def extract_meeting_platform(self, body: str) -> str:
        """Extract meeting platform from email body"""
        platforms = {
            'zoom': r'zoom\.us|zoom meeting|zoom call',
            'teams': r'teams\.microsoft|microsoft teams|teams meeting',
            'meet': r'meet\.google|google meet|meet call',
            'skype': r'skype|skype\.com',
            'webex': r'webex|cisco webex',
            'phone': r'phone call|phone interview|call you at',
            'in-person': r'in person|on-site|at our office|visit our office'
        }
        
        body_lower = body.lower()
        
        for platform, pattern in platforms.items():
            if re.search(pattern, body_lower):
                return platform.title()
        
        return "Platform TBD"
    
    def extract_interviewer_name(self, email: Dict[str, Any]) -> str:
        """Extract interviewer name from email"""
        sender = email.get('sender', '')
        
        # Try to extract name from sender
        if '<' in sender:
            name_part = sender.split('<')[0].strip()
            if name_part and not '@' in name_part:
                return name_part
        
        # Try to extract from email body
        body = email.get('body', '')
        name_patterns = [
            r'best regards,\s*([a-zA-Z\s]+)',
            r'thanks,\s*([a-zA-Z\s]+)',
            r'sincerely,\s*([a-zA-Z\s]+)',
            r'from\s+([a-zA-Z\s]+)(?:\s+at|\s+from)'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if len(name.split()) <= 3:  # Reasonable name length
                    return name.title()
        
        return "Unknown Interviewer"
    
    def extract_interview_time(self, body: str) -> str:
        """Extract interview time from email body"""
        # Time patterns
        time_patterns = [
            r'(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm))',
            r'(\d{1,2}\s*(?:AM|PM|am|pm))',
            r'at\s+(\d{1,2}:\d{2})',
            r'(\d{1,2}:\d{2})',
            r'(?:between|from)\s+(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm))\s+(?:to|and|-)\s+(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm))',
            r'(?:morning|afternoon|evening)',
            r'(\d{1,2}\s*o\'?clock)'
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                if match.lastindex and match.lastindex > 1:
                    # Handle time ranges
                    return f"{match.group(1)} - {match.group(2)}"
                else:
                    return match.group(1).strip()
        
        return "Time TBD"
    
    def determine_email_priority(self, email: Dict[str, Any]) -> str:
        """Determine priority of interview email"""
        subject = email.get('subject', '').lower()
        body = email.get('body', '').lower()
        
        # High priority indicators
        high_priority = ['urgent', 'asap', 'immediate', 'final round', 'offer', 'decision']
        medium_priority = ['phone screen', 'first round', 'initial', 'screening']
        
        if any(indicator in subject or indicator in body for indicator in high_priority):
            return 'high'
        elif any(indicator in subject or indicator in body for indicator in medium_priority):
            return 'medium'
        else:
            return 'normal'
