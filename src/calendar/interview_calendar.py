from datetime import datetime, timedelta
import json

class InterviewCalendar:
    def __init__(self):
        # Interview types and their typical durations
        self.interview_types = {
            'phone_screening': {'duration': 30, 'prep_time': 60},
            'technical_interview': {'duration': 90, 'prep_time': 180},
            'behavioral_interview': {'duration': 60, 'prep_time': 120},
            'panel_interview': {'duration': 75, 'prep_time': 150},
            'final_interview': {'duration': 45, 'prep_time': 120},
            'culture_fit': {'duration': 45, 'prep_time': 90},
            'case_study': {'duration': 120, 'prep_time': 240},
            'presentation': {'duration': 60, 'prep_time': 300}
        }
        
        # Preparation activities by interview type
        self.prep_activities = {
            'phone_screening': [
                'Research company basics',
                'Prepare elevator pitch',
                'Review resume thoroughly',
                'Prepare basic questions about role'
            ],
            'technical_interview': [
                'Practice coding problems',
                'Review system design concepts',
                'Study relevant technologies',
                'Prepare technical questions',
                'Set up coding environment'
            ],
            'behavioral_interview': [
                'Prepare STAR stories',
                'Research company culture',
                'Practice common behavioral questions',
                'Prepare specific examples',
                'Review job description thoroughly'
            ],
            'panel_interview': [
                'Research all panel members',
                'Prepare for multiple perspectives',
                'Practice maintaining eye contact with group',
                'Prepare questions for different roles',
                'Review company org structure'
            ],
            'final_interview': [
                'Prepare negotiation talking points',
                'Research market salary data',
                'Prepare thoughtful questions about role',
                'Review all previous interview feedback',
                'Prepare references list'
            ],
            'culture_fit': [
                'Research company values deeply',
                'Prepare examples showing culture alignment',
                'Research recent company news',
                'Prepare questions about team dynamics',
                'Practice showing personality authentically'
            ],
            'case_study': [
                'Practice case study frameworks',
                'Review industry-specific cases',
                'Prepare presentation structure',
                'Practice thinking aloud',
                'Review business fundamentals'
            ],
            'presentation': [
                'Prepare presentation content',
                'Practice presentation delivery',
                'Test technical setup',
                'Prepare for Q&A session',
                'Create backup materials'
            ]
        }
        
        # Reminder timeline (days before interview)
        self.reminder_schedule = {
            'initial_prep': 7,  # 1 week before
            'deep_prep': 3,     # 3 days before  
            'final_prep': 1,    # 1 day before
            'day_of': 0         # Day of interview
        }
        
        # Time blocks for preparation
        self.prep_time_blocks = [
            {'name': 'Company Research', 'duration': 30, 'priority': 'high'},
            {'name': 'Role Analysis', 'duration': 20, 'priority': 'high'},
            {'name': 'Resume Review', 'duration': 15, 'priority': 'medium'},
            {'name': 'Question Preparation', 'duration': 45, 'priority': 'high'},
            {'name': 'Mock Interview', 'duration': 60, 'priority': 'medium'},
            {'name': 'Technical Prep', 'duration': 90, 'priority': 'high'},
            {'name': 'Outfit/Materials Prep', 'duration': 15, 'priority': 'low'},
            {'name': 'Route/Tech Check', 'duration': 20, 'priority': 'medium'}
        ]
    
    def create_interview_schedule(self, interview_data):
        """Create comprehensive interview schedule with prep timeline"""
        try:
            interview_date = datetime.fromisoformat(interview_data['interview_date'])
            interview_type = interview_data.get('type', 'behavioral_interview')
            
            # Get interview type details
            type_info = self.interview_types.get(interview_type, self.interview_types['behavioral_interview'])
            
            schedule = {
                'interview_id': interview_data.get('id'),
                'company': interview_data.get('company'),
                'position': interview_data.get('position'),
                'interviewer': interview_data.get('interviewer'),
                'interview_date': interview_date.isoformat(),
                'interview_type': interview_type,
                'duration_minutes': type_info['duration'],
                'prep_time_needed': type_info['prep_time'],
                'preparation_timeline': [],
                'reminders': [],
                'checklist': [],
                'calendar_events': [],
                'created_at': datetime.now().isoformat()
            }
            
            # Create preparation timeline
            schedule['preparation_timeline'] = self._create_prep_timeline(
                interview_date, interview_type, type_info
            )
            
            # Create reminder schedule
            schedule['reminders'] = self._create_reminder_schedule(
                interview_date, interview_data
            )
            
            # Create checklist
            schedule['checklist'] = self._create_interview_checklist(
                interview_type, interview_data
            )
            
            # Create calendar events
            schedule['calendar_events'] = self._create_calendar_events(
                interview_date, interview_data, schedule['preparation_timeline']
            )
            
            return schedule
            
        except Exception as e:
            return {'error': str(e)}
    
    def _create_prep_timeline(self, interview_date, interview_type, type_info):
        """Create detailed preparation timeline"""
        timeline = []
        prep_activities = self.prep_activities.get(interview_type, [])
        
        # Distribute activities across preparation period
        prep_start = interview_date - timedelta(days=7)  # Start 1 week before
        
        # Week before (7 days out)
        timeline.append({
            'phase': 'Initial Preparation',
            'date': prep_start.isoformat(),
            'days_before': 7,
            'activities': prep_activities[:2] if len(prep_activities) >= 2 else prep_activities,
            'time_needed': 60,
            'priority': 'medium',
            'status': 'pending'
        })
        
        # 3 days before
        if len(prep_activities) > 2:
            timeline.append({
                'phase': 'Deep Preparation',
                'date': (interview_date - timedelta(days=3)).isoformat(),
                'days_before': 3,
                'activities': prep_activities[2:4] if len(prep_activities) >= 4 else prep_activities[2:],
                'time_needed': 90,
                'priority': 'high',
                'status': 'pending'
            })
        
        # Day before
        timeline.append({
            'phase': 'Final Preparation',
            'date': (interview_date - timedelta(days=1)).isoformat(),
            'days_before': 1,
            'activities': [
                'Review all materials',
                'Practice key answers',
                'Prepare questions to ask',
                'Plan route/test technology',
                'Prepare outfit and materials'
            ],
            'time_needed': 120,
            'priority': 'high',
            'status': 'pending'
        })
        
        # Day of interview
        timeline.append({
            'phase': 'Interview Day',
            'date': interview_date.isoformat(),
            'days_before': 0,
            'activities': [
                'Review key points (30 min before)',
                'Arrive 10-15 minutes early',
                'Final tech/materials check',
                'Mental preparation/relaxation'
            ],
            'time_needed': 45,
            'priority': 'critical',
            'status': 'pending'
        })
        
        return timeline
    
    def _create_reminder_schedule(self, interview_date, interview_data):
        """Create reminder schedule"""
        reminders = []
        
        for reminder_type, days_before in self.reminder_schedule.items():
            reminder_date = interview_date - timedelta(days=days_before)
            
            reminder_content = {
                'initial_prep': f"Start preparing for your {interview_data.get('company')} interview in 1 week",
                'deep_prep': f"Deep preparation time for {interview_data.get('company')} interview in 3 days",
                'final_prep': f"Final preparation for tomorrow's {interview_data.get('company')} interview",
                'day_of': f"Today is your {interview_data.get('company')} interview at {interview_date.strftime('%I:%M %p')}"
            }
            
            reminders.append({
                'type': reminder_type,
                'date': reminder_date.isoformat(),
                'title': reminder_content[reminder_type],
                'priority': 'high' if reminder_type in ['final_prep', 'day_of'] else 'medium',
                'sent': False
            })
        
        return reminders
    
    def _create_interview_checklist(self, interview_type, interview_data):
        """Create comprehensive interview checklist"""
        checklist = []
        
        # Universal checklist items
        universal_items = [
            {'item': 'Research company thoroughly', 'category': 'research', 'priority': 'high'},
            {'item': 'Review job description', 'category': 'research', 'priority': 'high'},
            {'item': 'Prepare elevator pitch', 'category': 'preparation', 'priority': 'high'},
            {'item': 'Prepare STAR method examples', 'category': 'preparation', 'priority': 'high'},
            {'item': 'Prepare questions to ask interviewer', 'category': 'preparation', 'priority': 'high'},
            {'item': 'Print extra copies of resume', 'category': 'materials', 'priority': 'medium'},
            {'item': 'Choose appropriate outfit', 'category': 'logistics', 'priority': 'medium'},
            {'item': 'Plan route and parking', 'category': 'logistics', 'priority': 'medium'},
            {'item': 'Test video call technology', 'category': 'technology', 'priority': 'high'},
            {'item': 'Prepare notebook and pen', 'category': 'materials', 'priority': 'low'}
        ]
        
        # Type-specific items
        type_specific = {
            'technical_interview': [
                {'item': 'Practice coding problems', 'category': 'technical', 'priority': 'high'},
                {'item': 'Set up coding environment', 'category': 'technical', 'priority': 'high'},
                {'item': 'Review system design concepts', 'category': 'technical', 'priority': 'medium'},
                {'item': 'Prepare technical questions', 'category': 'technical', 'priority': 'medium'}
            ],
            'presentation': [
                {'item': 'Create presentation slides', 'category': 'presentation', 'priority': 'high'},
                {'item': 'Practice presentation timing', 'category': 'presentation', 'priority': 'high'},
                {'item': 'Prepare backup materials', 'category': 'presentation', 'priority': 'medium'},
                {'item': 'Test presentation technology', 'category': 'technology', 'priority': 'high'}
            ],
            'case_study': [
                {'item': 'Review case study frameworks', 'category': 'analytical', 'priority': 'high'},
                {'item': 'Practice case study examples', 'category': 'analytical', 'priority': 'high'},
                {'item': 'Prepare structured thinking approach', 'category': 'analytical', 'priority': 'medium'}
            ]
        }
        
        # Combine universal and type-specific items
        checklist.extend(universal_items)
        if interview_type in type_specific:
            checklist.extend(type_specific[interview_type])
        
        # Add completion tracking
        for item in checklist:
            item.update({
                'completed': False,
                'completion_date': None,
                'notes': ''
            })
        
        return checklist
    
    def _create_calendar_events(self, interview_date, interview_data, prep_timeline):
        """Create calendar events for preparation and interview"""
        events = []
        
        # Interview event
        events.append({
            'title': f"Interview: {interview_data.get('company')} - {interview_data.get('position')}",
            'start_time': interview_date.isoformat(),
            'end_time': (interview_date + timedelta(hours=1.5)).isoformat(),
            'type': 'interview',
            'location': interview_data.get('location', 'TBD'),
            'description': f"Interview with {interview_data.get('interviewer', 'TBD')}",
            'reminders': [15, 60]  # 15 min and 1 hour before
        })
        
        # Preparation events
        for phase in prep_timeline:
            if phase['days_before'] > 0:
                prep_date = datetime.fromisoformat(phase['date'])
                events.append({
                    'title': f"Interview Prep: {phase['phase']} - {interview_data.get('company')}",
                    'start_time': prep_date.isoformat(),
                    'end_time': (prep_date + timedelta(minutes=phase['time_needed'])).isoformat(),
                    'type': 'preparation',
                    'description': f"Preparation activities: {', '.join(phase['activities'][:3])}",
                    'reminders': [30]  # 30 min before
                })
        
        # Day-before final prep
        final_prep_date = interview_date - timedelta(days=1)
        final_prep_date = final_prep_date.replace(hour=18, minute=0)  # 6 PM day before
        
        events.append({
            'title': f"Final Interview Prep - {interview_data.get('company')}",
            'start_time': final_prep_date.isoformat(),
            'end_time': (final_prep_date + timedelta(hours=2)).isoformat(),
            'type': 'final_preparation',
            'description': 'Final review, practice, and mental preparation',
            'reminders': [30]
        })
        
        return events
    
    def track_preparation_progress(self, schedule_id, activity_completed, notes=''):
        """Track completion of preparation activities"""
        try:
            completion_record = {
                'schedule_id': schedule_id,
                'activity': activity_completed,
                'completed_at': datetime.now().isoformat(),
                'notes': notes,
                'status': 'completed'
            }
            
            return completion_record
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_daily_prep_plan(self, interview_date, interview_type):
        """Get specific daily preparation plan"""
        try:
            days_until = (datetime.fromisoformat(interview_date) - datetime.now()).days
            
            if days_until < 0:
                return {'message': 'Interview has passed'}
            
            prep_activities = self.prep_activities.get(interview_type, [])
            
            if days_until >= 7:
                return {
                    'phase': 'Early Preparation',
                    'focus': 'Research and Foundation',
                    'activities': prep_activities[:2] if len(prep_activities) >= 2 else prep_activities,
                    'time_allocation': '30-60 minutes',
                    'priority': 'Start when convenient'
                }
            elif days_until >= 3:
                return {
                    'phase': 'Active Preparation',
                    'focus': 'Skill Building and Practice',
                    'activities': prep_activities[2:4] if len(prep_activities) >= 4 else prep_activities,
                    'time_allocation': '60-90 minutes',
                    'priority': 'High - schedule time blocks'
                }
            elif days_until >= 1:
                return {
                    'phase': 'Intensive Preparation',
                    'focus': 'Practice and Refinement',
                    'activities': [
                        'Complete mock interview',
                        'Finalize key talking points',
                        'Prepare specific examples',
                        'Research interviewer background'
                    ],
                    'time_allocation': '2-3 hours',
                    'priority': 'Critical - dedicated time needed'
                }
            else:  # Day of interview
                return {
                    'phase': 'Day of Interview',
                    'focus': 'Final Review and Logistics',
                    'activities': [
                        'Light review of key points (30 min)',
                        'Check route/technology',
                        'Prepare materials',
                        'Mental preparation'
                    ],
                    'time_allocation': '45 minutes total',
                    'priority': 'Execute plan'
                }
                
        except Exception as e:
            return {'error': str(e)}
    
    def generate_deadline_alerts(self, schedules):
        """Generate alerts for upcoming deadlines"""
        try:
            now = datetime.now()
            alerts = []
            
            for schedule in schedules:
                interview_date = datetime.fromisoformat(schedule['interview_date'])
                days_until = (interview_date - now).days
                hours_until = (interview_date - now).total_seconds() / 3600
                
                # Critical alerts
                if hours_until <= 24 and hours_until > 0:
                    alerts.append({
                        'type': 'critical',
                        'company': schedule['company'],
                        'position': schedule['position'],
                        'message': f"Interview in {int(hours_until)} hours",
                        'action_needed': 'Final preparation',
                        'priority': 'high'
                    })
                elif days_until <= 3 and days_until > 0:
                    alerts.append({
                        'type': 'urgent',
                        'company': schedule['company'],
                        'position': schedule['position'],
                        'message': f"Interview in {days_until} days",
                        'action_needed': 'Begin intensive preparation',
                        'priority': 'medium'
                    })
                elif days_until <= 7 and days_until > 3:
                    alerts.append({
                        'type': 'reminder',
                        'company': schedule['company'],
                        'position': schedule['position'],
                        'message': f"Interview in {days_until} days",
                        'action_needed': 'Start preparation activities',
                        'priority': 'low'
                    })
            
            return alerts
            
        except Exception as e:
            return {'error': str(e)}
    
    def export_calendar_data(self, schedules, format='ical'):
        """Export calendar data in various formats"""
        try:
            if format == 'ical':
                # Basic iCal format structure
                ical_events = []
                for schedule in schedules:
                    for event in schedule.get('calendar_events', []):
                        ical_event = {
                            'summary': event['title'],
                            'dtstart': event['start_time'],
                            'dtend': event['end_time'],
                            'description': event.get('description', ''),
                            'location': event.get('location', ''),
                            'reminder': event.get('reminders', [])
                        }
                        ical_events.append(ical_event)
                return ical_events
            
            elif format == 'google':
                # Google Calendar format
                google_events = []
                for schedule in schedules:
                    for event in schedule.get('calendar_events', []):
                        google_event = {
                            'summary': event['title'],
                            'start': {'dateTime': event['start_time']},
                            'end': {'dateTime': event['end_time']},
                            'description': event.get('description', ''),
                            'location': event.get('location', ''),
                            'reminders': {
                                'useDefault': False,
                                'overrides': [
                                    {'method': 'popup', 'minutes': min_before}
                                    for min_before in event.get('reminders', [])
                                ]
                            }
                        }
                        google_events.append(google_event)
                return google_events
            
            return {'error': 'Unsupported export format'}
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_preparation_insights(self, completed_schedules):
        """Analyze preparation patterns and provide insights"""
        try:
            insights = {
                'average_prep_time': 0,
                'most_effective_activities': [],
                'preparation_patterns': {},
                'success_correlation': {},
                'recommendations': []
            }
            
            if not completed_schedules:
                return insights
            
            # Calculate average preparation time
            total_prep_time = sum(
                schedule.get('prep_time_needed', 0) 
                for schedule in completed_schedules
            )
            insights['average_prep_time'] = total_prep_time / len(completed_schedules)
            
            # Analyze preparation patterns
            for schedule in completed_schedules:
                interview_type = schedule.get('interview_type', 'unknown')
                if interview_type not in insights['preparation_patterns']:
                    insights['preparation_patterns'][interview_type] = {
                        'count': 0,
                        'success_rate': 0,
                        'avg_prep_time': 0
                    }
                insights['preparation_patterns'][interview_type]['count'] += 1
            
            # Generate recommendations
            insights['recommendations'] = [
                'Schedule preparation time in advance',
                'Focus on company-specific research',
                'Practice behavioral questions with STAR method',
                'Do mock interviews for technical roles',
                'Prepare thoughtful questions to ask'
            ]
            
            return insights
            
        except Exception as e:
            return {'error': str(e)}