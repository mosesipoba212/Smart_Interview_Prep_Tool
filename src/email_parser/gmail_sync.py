"""
Enhanced Gmail Integration for Real-Time Application Tracking
Automatically syncs Gmail data with application tracker
"""

import re
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from src.email_parser.gmail_service import GmailService
from src.application_tracker.tracker import ApplicationTracker

class GmailApplicationSync:
    """Syncs Gmail emails with application tracking system"""
    
    def __init__(self):
        self.gmail_service = GmailService()
        self.app_tracker = ApplicationTracker()
        
    def sync_gmail_to_applications(self, days_back: int = 30) -> Dict[str, Any]:
        """
        Scan Gmail and automatically populate application tracker
        """
        try:
            print(f"🔍 Scanning Gmail for the last {days_back} days...")
            
            # Get emails from Gmail
            emails = self.gmail_service.fetch_recent_emails(days_back)
            print(f"📧 Found {len(emails)} emails to process")
            
            # Process each email and extract application data
            processed_emails = 0
            new_applications = 0
            updated_applications = 0
            
            for email in emails:
                try:
                    # Extract application information from email
                    app_data = self.extract_application_from_email(email)
                    
                    if app_data:
                        # Check if application already exists
                        existing_app = self.find_existing_application(app_data)
                        
                        if existing_app:
                            # Update existing application
                            self.update_application_from_email(existing_app['id'], email, app_data)
                            updated_applications += 1
                        else:
                            # Create new application
                            app_id = self.create_application_from_email(app_data)
                            if app_id:
                                new_applications += 1
                        
                        processed_emails += 1
                        
                except Exception as e:
                    print(f"⚠️ Error processing email: {e}")
                    continue
            
            print(f"✅ Gmail sync complete!")
            print(f"📊 Processed: {processed_emails} emails")
            print(f"➕ New applications: {new_applications}")
            print(f"🔄 Updated applications: {updated_applications}")
            
            return {
                'success': True,
                'processed_emails': processed_emails,
                'new_applications': new_applications,
                'updated_applications': updated_applications,
                'total_emails_scanned': len(emails)
            }
            
        except Exception as e:
            print(f"❌ Gmail sync failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'processed_emails': 0,
                'new_applications': 0,
                'updated_applications': 0
            }
    
    def extract_application_from_email(self, email: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract application data from email"""
        subject = email.get('subject', '').lower()
        body = email.get('body', '').lower()
        sender = email.get('sender', '')
        date = email.get('date', datetime.now().isoformat())
        
        # Determine email type and extract data
        email_type = self.classify_email_type(subject, body)
        
        if email_type == 'unknown':
            return None
        
        # Extract company name
        company = self.extract_company_name(sender, subject, body)
        
        # Extract position
        position = self.extract_position_from_email(subject, body)
        
        # Determine application status based on email content
        status = self.determine_application_status(email_type, subject, body)
        
        return {
            'company': company,
            'position': position,
            'status': status,
            'email_type': email_type,
            'email_date': date,
            'platform': 'Gmail Detection',
            'notes': f'Auto-detected from email: {email.get("subject", "")}',
            'email_id': email.get('id')
        }
    
    def classify_email_type(self, subject: str, body: str) -> str:
        """Classify the type of job-related email"""
        text = f"{subject} {body}".lower()
        
        # Interview invitation patterns
        if any(keyword in text for keyword in [
            'interview', 'phone screen', 'video call', 'meeting request',
            'schedule a call', 'available for', 'interview invitation'
        ]):
            return 'interview_invitation'
        
        # Application confirmation patterns
        if any(keyword in text for keyword in [
            'application received', 'thank you for applying', 'application confirmation',
            'we received your application'
        ]):
            return 'application_confirmation'
        
        # Rejection patterns
        if any(keyword in text for keyword in [
            'unfortunately', 'not moving forward', 'decided to pursue',
            'not selected', 'rejection', 'thank you for your interest'
        ]) and any(keyword in text for keyword in ['position', 'role', 'opportunity']):
            return 'rejection'
        
        # Offer patterns
        if any(keyword in text for keyword in [
            'offer', 'congratulations', 'pleased to offer', 'job offer',
            'extend an offer', 'offer letter'
        ]):
            return 'offer'
        
        # Follow-up patterns
        if any(keyword in text for keyword in [
            'next steps', 'following up', 'update on your application',
            'status update'
        ]):
            return 'follow_up'
        
        return 'unknown'
    
    def extract_company_name(self, sender: str, subject: str, body: str) -> str:
        """Enhanced company name extraction"""
        # Try sender email domain first
        if '@' in sender:
            domain = sender.split('@')[-1].lower()
            if domain not in ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']:
                domain_parts = domain.split('.')
                if len(domain_parts) >= 2:
                    company = domain_parts[0] if domain_parts[0] not in ['www', 'mail', 'careers', 'jobs'] else domain_parts[1]
                    return company.replace('-', ' ').title()
        
        # Try to extract from subject line
        subject_patterns = [
            r'(?:at|from|with)\s+([A-Z][a-zA-Z\s&]+?)(?:\s+(?:team|hiring|hr|recruiter)|\s*$)',
            r'([A-Z][a-zA-Z\s&]+?)\s+(?:opportunity|position|role|job)',
            r'([A-Z][a-zA-Z\s&]+?)\s+(?:interview|screening)'
        ]
        
        for pattern in subject_patterns:
            match = re.search(pattern, subject, re.IGNORECASE)
            if match:
                company = match.group(1).strip()
                if len(company.split()) <= 3 and company not in ['Team', 'Hiring', 'HR']:
                    return company
        
        # Try sender name
        if '<' in sender:
            name_part = sender.split('<')[0].strip()
            company_indicators = ['HR', 'Recruiting', 'Talent', 'Careers']
            for indicator in company_indicators:
                if indicator in name_part:
                    parts = name_part.split()
                    for i, part in enumerate(parts):
                        if indicator in part and i > 0:
                            return parts[i-1]
        
        return "Unknown Company"
    
    def extract_position_from_email(self, subject: str, body: str) -> str:
        """Extract job position from email content"""
        text = f"{subject} {body}"
        
        # Position patterns
        patterns = [
            r'(?:for|as)\s+(?:a\s+|the\s+)?([a-zA-Z\s]+(?:engineer|developer|manager|analyst|designer|lead|director|coordinator|specialist|intern))',
            r'(?:position|role):\s*([a-zA-Z\s]+)',
            r'([a-zA-Z\s]+(?:engineer|developer|manager|analyst|designer|lead|director|intern))\s+(?:position|role|opportunity)',
            r'software\s+(engineer|developer)',
            r'(full\s+stack|frontend|backend|mobile|ios|android|web)\s+(developer|engineer)',
            r'(data\s+(?:scientist|analyst|engineer))',
            r'(product\s+manager)',
            r'(ui/ux\s+designer)',
            r'(devops\s+engineer)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip().title()
        
        return "Unknown Position"
    
    def determine_application_status(self, email_type: str, subject: str, body: str) -> str:
        """Determine application status based on email content"""
        status_mapping = {
            'interview_invitation': 'interview_scheduled',
            'application_confirmation': 'applied',
            'rejection': 'rejected',
            'offer': 'offer',
            'follow_up': 'under_review'
        }
        
        return status_mapping.get(email_type, 'applied')
    
    def find_existing_application(self, app_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find existing application in database"""
        try:
            conn = sqlite3.connect(self.app_tracker.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM applications 
                WHERE company = ? AND position = ?
                ORDER BY application_date DESC
                LIMIT 1
            ''', (app_data['company'], app_data['position']))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))
            return None
            
        except Exception as e:
            print(f"Error finding existing application: {e}")
            return None
    
    def create_application_from_email(self, app_data: Dict[str, Any]) -> Optional[int]:
        """Create new application from email data"""
        try:
            application_data = {
                'company': app_data['company'],
                'position': app_data['position'],
                'application_date': datetime.now().date().isoformat(),
                'status': app_data['status'],
                'platform': app_data['platform'],
                'notes': app_data['notes']
            }
            
            return self.app_tracker.log_application(application_data)
            
        except Exception as e:
            print(f"Error creating application: {e}")
            return None
    
    def update_application_from_email(self, app_id: int, email: Dict[str, Any], app_data: Dict[str, Any]):
        """Update existing application with email information"""
        try:
            # Update application status if it's more advanced
            status_hierarchy = {
                'applied': 1,
                'under_review': 2,
                'interview_scheduled': 3,
                'rejected': 4,
                'offer': 5
            }
            
            current_status = self.get_application_status(app_id)
            new_status = app_data['status']
            
            if status_hierarchy.get(new_status, 0) > status_hierarchy.get(current_status, 0):
                self.app_tracker.update_application_status(app_id, new_status)
                
                # Log response if it's an interview invitation or rejection
                if app_data['email_type'] in ['interview_invitation', 'rejection', 'offer']:
                    response_data = {
                        'application_id': app_id,
                        'response_type': app_data['email_type'],
                        'response_date': datetime.now().date().isoformat(),
                        'message': email.get('subject', '')
                    }
                    self.app_tracker.log_response(response_data)
            
        except Exception as e:
            print(f"Error updating application: {e}")
    
    def get_application_status(self, app_id: int) -> str:
        """Get current status of application"""
        try:
            conn = sqlite3.connect(self.app_tracker.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT status FROM applications WHERE id = ?', (app_id,))
            row = cursor.fetchone()
            conn.close()
            
            return row[0] if row else 'applied'
            
        except Exception:
            return 'applied'
    
    def get_sync_summary(self) -> Dict[str, Any]:
        """Get summary of synced data"""
        try:
            stats = self.app_tracker.get_application_stats()
            return {
                'total_applications': stats.get('total_applications', 0),
                'total_companies': len(stats.get('top_companies', [])),
                'interview_invitations': stats.get('interviews_scheduled', 0),
                'response_rate': stats.get('response_rate', 0),
                'last_sync': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e)}