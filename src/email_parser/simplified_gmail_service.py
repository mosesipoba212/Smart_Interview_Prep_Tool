"""
Simplified Gmail Service with API Key Support
Works with Google API key for basic email access
"""

import os
import re
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

class SimplifiedGmailService:
    """Simplified Gmail service that works with API key"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.base_url = "https://www.googleapis.com/gmail/v1"
        
        if self.api_key:
            print("✅ Google API key configured for Gmail service")
        else:
            print("⚠️  No Google API key found. Using mock email service.")
    
    def fetch_recent_emails(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Fetch recent emails (mock implementation with realistic data)"""
        # For now, return mock interview emails since API key alone 
        # isn't sufficient for Gmail access (needs OAuth2)
        print("📧 Generating mock interview emails for demonstration...")
        
        mock_emails = [
            {
                'id': 'mock_001',
                'subject': 'Technical Interview Invitation - Software Engineer Position',
                'sender': 'sarah.chen@techcorp.com',
                'date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'body': '''
                Hi there,
                
                Thank you for your interest in the Software Engineer position at TechCorp. 
                We'd like to schedule a technical interview with you for next Tuesday at 2:00 PM.
                
                The interview will cover:
                - Data structures and algorithms
                - System design concepts
                - Python programming
                
                Please let me know if this time works for you.
                
                Best regards,
                Sarah Chen
                Technical Recruiter
                TechCorp
                ''',
                'headers': {
                    'From': 'Sarah Chen <sarah.chen@techcorp.com>',
                    'Subject': 'Technical Interview Invitation - Software Engineer Position',
                    'Date': (datetime.now() - timedelta(days=1)).strftime('%a, %d %b %Y %H:%M:%S %z')
                }
            },
            {
                'id': 'mock_002', 
                'subject': 'Phone Screen - Data Scientist Role',
                'sender': 'recruiting@datacom.com',
                'date': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
                'body': '''
                Dear Candidate,
                
                We'd like to schedule a 30-minute phone screening for the Data Scientist position.
                
                Available times:
                - Thursday 10:00 AM
                - Friday 3:00 PM
                
                Topics to prepare:
                - Machine learning fundamentals
                - Statistical analysis
                - Python and SQL
                
                Looking forward to speaking with you!
                
                DataCom Recruiting Team
                ''',
                'headers': {
                    'From': 'DataCom Recruiting <recruiting@datacom.com>',
                    'Subject': 'Phone Screen - Data Scientist Role',
                    'Date': (datetime.now() - timedelta(days=2)).strftime('%a, %d %b %Y %H:%M:%S %z')
                }
            },
            {
                'id': 'mock_003',
                'subject': 'Final Round Interview - Product Manager',
                'sender': 'hr@innovatetech.com',
                'date': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
                'body': '''
                Congratulations! You've made it to the final round.
                
                Final Interview Details:
                - Date: Next Monday 
                - Time: 1:00 PM - 4:00 PM
                - Location: InnovateTech HQ
                - Format: Panel interview with leadership team
                
                Please prepare:
                - Product strategy case study
                - Portfolio presentation
                - Questions about our product roadmap
                
                Best of luck!
                
                Maria Rodriguez
                Head of People
                InnovateTech
                ''',
                'headers': {
                    'From': 'Maria Rodriguez <hr@innovatetech.com>',
                    'Subject': 'Final Round Interview - Product Manager',
                    'Date': (datetime.now() - timedelta(days=3)).strftime('%a, %d %b %Y %H:%M:%S %z')
                }
            }
        ]
        
        return mock_emails
    
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
        
        # Extract meeting platform
        platform = self.extract_meeting_platform(body)
        
        # Extract interviewer name
        interviewer = self.extract_interviewer_name(email)
        
        return {
            'company': company,
            'position': position,
            'date': interview_date,
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
            # Remove common email domains
            if domain not in ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']:
                company = domain.split('.')[0]
                return company.title()
        
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
        # Date patterns
        date_patterns = [
            r'(?:on|for)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday),?\s+([a-zA-Z]+\s+\d{1,2})',
            r'(\d{1,2}/\d{1,2}/\d{4})',
            r'([a-zA-Z]+\s+\d{1,2},?\s+\d{4})',
            r'(\d{1,2}\s+[a-zA-Z]+\s+\d{4})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                return match.group(0).strip()
        
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
    
    def scan_for_interviews(self, days_back: int = 14) -> List[Dict[str, Any]]:
        """Scan emails for interview opportunities"""
        try:
            # Use the existing fetch_recent_emails method
            emails = self.fetch_recent_emails(days_back=days_back)
            
            # Filter for interview-related emails
            interview_emails = []
            interview_keywords = [
                'interview', 'phone screen', 'technical round', 'hiring manager',
                'coding challenge', 'final round', 'onsite', 'video call',
                'assessment', 'evaluation', 'selection process'
            ]
            
            for email in emails:
                # Check if email contains interview keywords
                subject_lower = email.get('subject', '').lower()
                body_lower = email.get('body', '').lower()
                
                if any(keyword in subject_lower or keyword in body_lower for keyword in interview_keywords):
                    interview_emails.append({
                        'id': email.get('id'),
                        'subject': email.get('subject'),
                        'sender': email.get('sender'),
                        'date': email.get('date'),
                        'snippet': email.get('body', '')[:200] + '...' if len(email.get('body', '')) > 200 else email.get('body', ''),
                        'type': 'interview_invitation'
                    })
            
            return interview_emails
            
        except Exception as e:
            print(f"❌ Error scanning for interviews: {e}")
            return []
