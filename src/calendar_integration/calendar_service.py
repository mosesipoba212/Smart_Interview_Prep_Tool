"""
Google Calendar Integration Service
Automatically schedules interview prep blocks and manages calendar events
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_CALENDAR_AVAILABLE = True
except ImportError:
    GOOGLE_CALENDAR_AVAILABLE = False
    print("⚠️  Google Calendar API not available. Using mock calendar service.")

class CalendarService:
    """Google Calendar integration for interview prep scheduling"""
    
    SCOPES = [
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/calendar.events'
    ]
    
    def __init__(self):
        self.service = None
        self.mock_mode = not GOOGLE_CALENDAR_AVAILABLE
        
        if not self.mock_mode:
            self.authenticate()
        else:
            print("📅 Calendar service initialized in mock mode")
    
    def authenticate(self):
        """Authenticate with Google Calendar API"""
        creds = None
        
        # Check for existing token
        if os.path.exists('calendar_token.json'):
            creds = Credentials.from_authorized_user_file('calendar_token.json', self.SCOPES)
        
        # If no valid credentials, request authorization
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Use the same credentials.json file as Gmail
                if os.path.exists('credentials.json'):
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', self.SCOPES)
                    creds = flow.run_local_server(port=0)
                else:
                    print("⚠️  Calendar credentials.json not found. Using mock calendar service.")
                    self.mock_mode = True
                    return
            
            # Save credentials for next run
            with open('calendar_token.json', 'w') as token:
                token.write(creds.to_json())
        
        try:
            self.service = build('calendar', 'v3', credentials=creds)
            print("✅ Google Calendar API authenticated successfully")
        except HttpError as error:
            print(f"❌ Calendar API authentication failed: {error}")
            self.mock_mode = True
    
    def schedule_prep_blocks(self, interview_date: str, interview_type: str, duration_hours: int = 2) -> List[Dict[str, Any]]:
        """Schedule interview preparation blocks leading up to the interview"""
        try:
            # Parse interview date
            target_date = self.parse_interview_date(interview_date)
            if not target_date:
                target_date = datetime.now() + timedelta(days=7)  # Default to next week
            
            # Generate prep schedule
            prep_blocks = self.generate_prep_schedule(target_date, interview_type, duration_hours)
            
            # Schedule each prep block
            scheduled_events = []
            for block in prep_blocks:
                if self.mock_mode:
                    event = self.create_mock_event(block)
                else:
                    event = self.create_calendar_event(block)
                
                if event:
                    scheduled_events.append(event)
            
            print(f"📅 Scheduled {len(scheduled_events)} prep blocks for {interview_type} interview")
            return scheduled_events
            
        except Exception as e:
            print(f"❌ Error scheduling prep blocks: {e}")
            return []
    
    def parse_interview_date(self, date_string: str) -> Optional[datetime]:
        """Parse interview date string into datetime object"""
        if not date_string or date_string == "Date TBD":
            return None
        
        # Common date formats
        date_formats = [
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%B %d, %Y',
            '%b %d, %Y',
            '%d %B %Y',
            '%d %b %Y'
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue
        
        # Try to extract date from natural language
        try:
            # Simple extraction for "Monday, January 15" format
            if ',' in date_string:
                parts = date_string.split(',')
                if len(parts) >= 2:
                    date_part = parts[1].strip()
                    current_year = datetime.now().year
                    return datetime.strptime(f"{date_part} {current_year}", '%B %d %Y')
        except:
            pass
        
        return None
    
    def generate_prep_schedule(self, interview_date: datetime, interview_type: str, total_hours: int) -> List[Dict[str, Any]]:
        """Generate a series of prep blocks leading up to the interview"""
        prep_blocks = []
        
        # Prep schedule templates based on interview type
        prep_templates = {
            'technical': [
                {'days_before': 7, 'duration': 2, 'focus': 'Algorithm Practice', 'description': 'Practice coding problems and data structures'},
                {'days_before': 5, 'duration': 2, 'focus': 'System Design Review', 'description': 'Review system design patterns and architecture'},
                {'days_before': 3, 'duration': 1.5, 'focus': 'Company Research', 'description': 'Research company technology stack and recent developments'},
                {'days_before': 1, 'duration': 1, 'focus': 'Mock Interview', 'description': 'Practice with mock technical questions'},
            ],
            'behavioral': [
                {'days_before': 5, 'duration': 1.5, 'focus': 'STAR Stories Prep', 'description': 'Prepare STAR method examples from your experience'},
                {'days_before': 3, 'duration': 1, 'focus': 'Company Values Research', 'description': 'Research company culture and values'},
                {'days_before': 1, 'duration': 1, 'focus': 'Question Practice', 'description': 'Practice common behavioral questions out loud'},
            ],
            'system_design': [
                {'days_before': 7, 'duration': 2, 'focus': 'Architecture Patterns', 'description': 'Review common system design patterns'},
                {'days_before': 5, 'duration': 2, 'focus': 'Scalability Concepts', 'description': 'Study load balancing, caching, and database scaling'},
                {'days_before': 3, 'duration': 1.5, 'focus': 'Trade-offs Analysis', 'description': 'Practice discussing system trade-offs'},
                {'days_before': 1, 'duration': 1, 'focus': 'Mock Design Session', 'description': 'Practice designing a system end-to-end'},
            ],
            'product': [
                {'days_before': 5, 'duration': 1.5, 'focus': 'Product Analysis', 'description': 'Analyze competitor products and market trends'},
                {'days_before': 3, 'duration': 1, 'focus': 'Metrics & KPIs', 'description': 'Review important product metrics and frameworks'},
                {'days_before': 1, 'duration': 1, 'focus': 'Case Study Practice', 'description': 'Practice product case study questions'},
            ]
        }
        
        template = prep_templates.get(interview_type, prep_templates['behavioral'])
        
        for block_template in template:
            prep_date = interview_date - timedelta(days=block_template['days_before'])
            
            # Schedule for evening (7 PM) on weekdays, afternoon (2 PM) on weekends
            if prep_date.weekday() < 5:  # Weekday
                start_time = prep_date.replace(hour=19, minute=0, second=0, microsecond=0)
            else:  # Weekend
                start_time = prep_date.replace(hour=14, minute=0, second=0, microsecond=0)
            
            end_time = start_time + timedelta(hours=block_template['duration'])
            
            prep_blocks.append({
                'title': f"Interview Prep: {block_template['focus']}",
                'description': block_template['description'],
                'start_time': start_time,
                'end_time': end_time,
                'type': interview_type,
                'focus_area': block_template['focus']
            })
        
        return prep_blocks
    
    def create_calendar_event(self, block: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create an actual Google Calendar event"""
        if self.mock_mode or not self.service:
            return self.create_mock_event(block)
        
        try:
            event = {
                'summary': block['title'],
                'description': block['description'],
                'start': {
                    'dateTime': block['start_time'].isoformat(),
                    'timeZone': 'America/New_York',  # You can make this configurable
                },
                'end': {
                    'dateTime': block['end_time'].isoformat(),
                    'timeZone': 'America/New_York',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 30},       # 30 minutes before
                    ],
                },
                'colorId': '9',  # Blue color for interview prep
            }
            
            created_event = self.service.events().insert(calendarId='primary', body=event).execute()
            
            return {
                'id': created_event['id'],
                'title': block['title'],
                'start_time': block['start_time'],
                'end_time': block['end_time'],
                'description': block['description'],
                'calendar_link': created_event.get('htmlLink', ''),
                'status': 'scheduled'
            }
            
        except HttpError as error:
            print(f"❌ Error creating calendar event: {error}")
            return self.create_mock_event(block)
    
    def create_mock_event(self, block: Dict[str, Any]) -> Dict[str, Any]:
        """Create a mock event for testing/demo purposes"""
        import uuid
        
        return {
            'id': str(uuid.uuid4()),
            'title': block['title'],
            'start_time': block['start_time'],
            'end_time': block['end_time'],
            'description': block['description'],
            'calendar_link': f"https://calendar.google.com/calendar/event?eid={uuid.uuid4()}",
            'status': 'mock_scheduled'
        }
    
    def get_upcoming_interviews(self, days_ahead: int = 14) -> List[Dict[str, Any]]:
        """Get upcoming interview-related events"""
        try:
            if self.mock_mode:
                return self.get_mock_upcoming_interviews()
            
            # Calculate time range
            now = datetime.utcnow()
            time_max = now + timedelta(days=days_ahead)
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now.isoformat() + 'Z',
                timeMax=time_max.isoformat() + 'Z',
                maxResults=50,
                singleEvents=True,
                orderBy='startTime',
                q='interview'  # Search for events containing "interview"
            ).execute()
            
            events = events_result.get('items', [])
            
            upcoming_interviews = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                
                upcoming_interviews.append({
                    'id': event['id'],
                    'title': event['summary'],
                    'start_time': start,
                    'description': event.get('description', ''),
                    'location': event.get('location', ''),
                    'calendar_link': event.get('htmlLink', '')
                })
            
            return upcoming_interviews
            
        except HttpError as error:
            print(f"❌ Error fetching upcoming interviews: {error}")
            return self.get_mock_upcoming_interviews()
    
    def get_mock_upcoming_interviews(self) -> List[Dict[str, Any]]:
        """Get mock upcoming interviews for demo"""
        now = datetime.now()
        
        return [
            {
                'id': 'mock_1',
                'title': 'Technical Interview - Software Engineer',
                'start_time': (now + timedelta(days=3)).isoformat(),
                'description': 'Technical interview focusing on algorithms and system design',
                'location': 'Zoom Meeting',
                'calendar_link': 'https://calendar.google.com/mock'
            },
            {
                'id': 'mock_2',
                'title': 'Interview Prep: Algorithm Practice',
                'start_time': (now + timedelta(days=1)).isoformat(),
                'description': 'Practice coding problems and data structures',
                'location': 'Home',
                'calendar_link': 'https://calendar.google.com/mock'
            }
        ]
    
    def update_prep_schedule(self, interview_id: str, new_date: datetime) -> bool:
        """Update prep schedule when interview date changes"""
        try:
            # This would involve finding related prep events and rescheduling them
            # For now, return success for mock mode
            if self.mock_mode:
                print(f"📅 Mock: Updated prep schedule for interview {interview_id}")
                return True
            
            # In real implementation, you would:
            # 1. Find all prep events related to this interview
            # 2. Delete existing prep events
            # 3. Create new prep schedule based on new date
            
            return True
            
        except Exception as e:
            print(f"❌ Error updating prep schedule: {e}")
            return False
    
    def get_calendar_conflicts(self, start_time: datetime, end_time: datetime) -> List[Dict[str, Any]]:
        """Check for calendar conflicts in the given time range"""
        try:
            if self.mock_mode:
                return []  # No conflicts in mock mode
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=start_time.isoformat() + 'Z',
                timeMax=end_time.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            conflicts = []
            
            for event in events:
                if event.get('status') != 'cancelled':
                    conflicts.append({
                        'title': event['summary'],
                        'start': event['start'].get('dateTime', event['start'].get('date')),
                        'end': event['end'].get('dateTime', event['end'].get('date'))
                    })
            
            return conflicts
            
        except HttpError as error:
            print(f"❌ Error checking calendar conflicts: {error}")
            return []
    
    def suggest_alternative_times(self, preferred_time: datetime, duration_hours: int = 2) -> List[datetime]:
        """Suggest alternative times if there are conflicts"""
        alternatives = []
        
        # Suggest times within the same day
        base_date = preferred_time.date()
        
        # Morning options (9 AM - 11 AM)
        morning_time = datetime.combine(base_date, datetime.min.time().replace(hour=9))
        if not self.get_calendar_conflicts(morning_time, morning_time + timedelta(hours=duration_hours)):
            alternatives.append(morning_time)
        
        # Afternoon options (2 PM - 4 PM)
        afternoon_time = datetime.combine(base_date, datetime.min.time().replace(hour=14))
        if not self.get_calendar_conflicts(afternoon_time, afternoon_time + timedelta(hours=duration_hours)):
            alternatives.append(afternoon_time)
        
        # Evening options (7 PM - 9 PM)
        evening_time = datetime.combine(base_date, datetime.min.time().replace(hour=19))
        if not self.get_calendar_conflicts(evening_time, evening_time + timedelta(hours=duration_hours)):
            alternatives.append(evening_time)
        
        return alternatives[:3]  # Return top 3 alternatives
