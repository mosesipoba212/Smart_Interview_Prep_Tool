from datetime import datetime, timedelta
import json

class PreparationChecklist:
    def __init__(self):
        # Comprehensive checklist categories
        self.checklist_categories = {
            'research': {
                'name': 'Company & Role Research',
                'priority': 'high',
                'items': [
                    'Research company mission, values, and culture',
                    'Study recent company news and developments',
                    'Understand company products/services',
                    'Research company leadership team',
                    'Analyze company financial performance',
                    'Review job description thoroughly',
                    'Understand role requirements and responsibilities',
                    'Research team structure and dynamics',
                    'Identify growth opportunities in the role',
                    'Research company competitors and market position'
                ]
            },
            'interviewer_prep': {
                'name': 'Interviewer Research',
                'priority': 'high',
                'items': [
                    'Research interviewer background on LinkedIn',
                    'Understand interviewer\'s role and responsibilities',
                    'Find common connections or interests',
                    'Review interviewer\'s recent posts/articles',
                    'Prepare questions specific to interviewer\'s expertise',
                    'Understand interviewer\'s management style (if manager)',
                    'Research interviewer\'s career path',
                    'Find interviewer\'s published work or presentations'
                ]
            },
            'self_preparation': {
                'name': 'Personal Preparation',
                'priority': 'high',
                'items': [
                    'Prepare compelling elevator pitch',
                    'Practice STAR method responses',
                    'Prepare specific examples and stories',
                    'Review your resume thoroughly',
                    'Prepare answers to common questions',
                    'Practice behavioral interview scenarios',
                    'Prepare thoughtful questions to ask',
                    'Plan salary negotiation talking points',
                    'Prepare references list',
                    'Practice articulating career goals'
                ]
            },
            'technical_prep': {
                'name': 'Technical Preparation',
                'priority': 'high',
                'items': [
                    'Practice coding problems and algorithms',
                    'Review system design concepts',
                    'Study relevant programming languages',
                    'Practice whiteboarding skills',
                    'Review technical fundamentals',
                    'Prepare technical project explanations',
                    'Set up coding environment and tools',
                    'Practice explaining complex technical concepts',
                    'Review industry best practices',
                    'Prepare technical questions to ask'
                ]
            },
            'materials_logistics': {
                'name': 'Materials & Logistics',
                'priority': 'medium',
                'items': [
                    'Print multiple copies of resume',
                    'Prepare portfolio or work samples',
                    'Organize reference contact information',
                    'Prepare list of accomplishments',
                    'Create leave-behind materials',
                    'Plan interview outfit and backup',
                    'Test video call technology',
                    'Plan route and transportation',
                    'Confirm interview time and location',
                    'Prepare backup contact information'
                ]
            },
            'mental_preparation': {
                'name': 'Mental & Physical Preparation',
                'priority': 'medium',
                'items': [
                    'Get adequate sleep before interview',
                    'Plan nutritious meal before interview',
                    'Practice relaxation techniques',
                    'Visualize successful interview',
                    'Prepare confidence-building exercises',
                    'Plan arrival time (10-15 minutes early)',
                    'Prepare positive mindset affirmations',
                    'Practice good posture and body language',
                    'Prepare backup plans for unexpected issues',
                    'Set realistic expectations'
                ]
            },
            'follow_up_prep': {
                'name': 'Follow-up Preparation',
                'priority': 'low',
                'items': [
                    'Prepare thank you email template',
                    'Plan follow-up timeline',
                    'Prepare additional materials to send',
                    'Plan next steps conversation',
                    'Prepare answers for potential additional questions',
                    'Plan references notification strategy',
                    'Prepare salary negotiation strategy',
                    'Plan decision-making criteria',
                    'Prepare questions for final interviews',
                    'Plan onboarding preparation activities'
                ]
            }
        }
        
        # Interview type specific checklists
        self.interview_type_additions = {
            'phone_screening': [
                'Test phone connection and backup options',
                'Prepare quiet, professional environment',
                'Have resume and notes readily available',
                'Practice speaking clearly and concisely',
                'Prepare backup phone number'
            ],
            'video_interview': [
                'Test video platform and backup browsers',
                'Set up professional background/lighting',
                'Test audio and video quality',
                'Prepare backup internet connection',
                'Practice eye contact with camera',
                'Have technical support contact ready'
            ],
            'technical_interview': [
                'Practice coding on whiteboard/computer',
                'Review data structures and algorithms',
                'Prepare system design examples',
                'Practice explaining thought process aloud',
                'Set up development environment',
                'Prepare technical questions about company stack'
            ],
            'panel_interview': [
                'Research all panel members',
                'Practice maintaining eye contact with group',
                'Prepare questions for different expertise areas',
                'Practice addressing multiple people',
                'Understand panel dynamics and roles'
            ],
            'case_study': [
                'Practice case study frameworks',
                'Review industry-specific case studies',
                'Practice structured problem-solving',
                'Prepare presentation materials',
                'Practice thinking aloud process'
            ],
            'final_interview': [
                'Prepare detailed questions about role',
                'Research executive team thoroughly',
                'Prepare negotiation talking points',
                'Plan decision timeline discussion',
                'Prepare strategic questions about company direction'
            ]
        }
        
        # Countdown timers for different time periods
        self.countdown_schedules = {
            '2_weeks_before': {
                'phase': 'Initial Preparation',
                'focus_areas': ['research', 'self_preparation'],
                'time_commitment': '30-60 minutes daily',
                'key_activities': [
                    'Begin company research',
                    'Start preparing STAR stories',
                    'Review job description daily'
                ]
            },
            '1_week_before': {
                'phase': 'Deep Preparation',
                'focus_areas': ['interviewer_prep', 'technical_prep'],
                'time_commitment': '1-2 hours daily',
                'key_activities': [
                    'Research interviewers thoroughly',
                    'Intensify technical practice',
                    'Begin mock interviews'
                ]
            },
            '3_days_before': {
                'phase': 'Intensive Preparation',
                'focus_areas': ['materials_logistics', 'technical_prep'],
                'time_commitment': '2-3 hours daily',
                'key_activities': [
                    'Finalize all materials',
                    'Complete technical practice',
                    'Conduct final mock interviews'
                ]
            },
            '1_day_before': {
                'phase': 'Final Preparation',
                'focus_areas': ['mental_preparation', 'logistics'],
                'time_commitment': '1-2 hours total',
                'key_activities': [
                    'Finalize logistics',
                    'Mental preparation',
                    'Light review only'
                ]
            },
            'day_of': {
                'phase': 'Interview Day',
                'focus_areas': ['mental_preparation', 'logistics'],
                'time_commitment': '30 minutes prep',
                'key_activities': [
                    'Final logistics check',
                    'Mental warm-up',
                    'Arrive early and composed'
                ]
            }
        }
        
        # Priority levels and completion tracking
        self.priority_weights = {
            'critical': 10,
            'high': 7,
            'medium': 4,
            'low': 2
        }
    
    def create_personalized_checklist(self, interview_data, user_preferences):
        """Create personalized checklist based on interview type and user preferences"""
        try:
            interview_type = interview_data.get('type', 'behavioral')
            interview_date = datetime.fromisoformat(interview_data['interview_date'])
            days_until = (interview_date - datetime.now()).days
            
            # Base checklist
            checklist = {
                'interview_info': {
                    'company': interview_data.get('company'),
                    'position': interview_data.get('position'),
                    'date': interview_date.isoformat(),
                    'type': interview_type,
                    'days_until': days_until
                },
                'categories': {},
                'priority_items': [],
                'countdown_timeline': {},
                'completion_stats': {
                    'total_items': 0,
                    'completed_items': 0,
                    'completion_percentage': 0,
                    'priority_completion': {}
                },
                'recommendations': [],
                'created_at': datetime.now().isoformat()
            }
            
            # Add base categories
            for category_key, category_data in self.checklist_categories.items():
                checklist['categories'][category_key] = {
                    'name': category_data['name'],
                    'priority': category_data['priority'],
                    'items': []
                }
                
                # Add items with completion tracking
                for item in category_data['items']:
                    checklist_item = {
                        'text': item,
                        'completed': False,
                        'completion_date': None,
                        'notes': '',
                        'priority': category_data['priority'],
                        'estimated_time': self._estimate_item_time(item),
                        'category': category_key
                    }
                    checklist['categories'][category_key]['items'].append(checklist_item)
                    checklist['completion_stats']['total_items'] += 1
            
            # Add interview type specific items
            if interview_type in self.interview_type_additions:
                if 'interview_specific' not in checklist['categories']:
                    checklist['categories']['interview_specific'] = {
                        'name': f'{interview_type.title()} Specific',
                        'priority': 'high',
                        'items': []
                    }
                
                for item in self.interview_type_additions[interview_type]:
                    checklist_item = {
                        'text': item,
                        'completed': False,
                        'completion_date': None,
                        'notes': '',
                        'priority': 'high',
                        'estimated_time': self._estimate_item_time(item),
                        'category': 'interview_specific'
                    }
                    checklist['categories']['interview_specific']['items'].append(checklist_item)
                    checklist['completion_stats']['total_items'] += 1
            
            # Create countdown timeline
            checklist['countdown_timeline'] = self._create_countdown_timeline(
                interview_date, checklist['categories']
            )
            
            # Generate priority recommendations
            checklist['recommendations'] = self._generate_checklist_recommendations(
                days_until, interview_type, user_preferences
            )
            
            # Identify priority items
            checklist['priority_items'] = self._identify_priority_items(checklist['categories'])
            
            return checklist
            
        except Exception as e:
            return {'error': str(e)}
    
    def _create_countdown_timeline(self, interview_date, categories):
        """Create countdown timeline with specific activities"""
        timeline = {}
        now = datetime.now()
        
        for period, schedule_info in self.countdown_schedules.items():
            if period == 'day_of':
                target_date = interview_date.date()
            elif period == '1_day_before':
                target_date = (interview_date - timedelta(days=1)).date()
            elif period == '3_days_before':
                target_date = (interview_date - timedelta(days=3)).date()
            elif period == '1_week_before':
                target_date = (interview_date - timedelta(days=7)).date()
            elif period == '2_weeks_before':
                target_date = (interview_date - timedelta(days=14)).date()
            
            # Get relevant items for this period
            period_items = []
            focus_areas = schedule_info.get('focus_areas', [])
            
            for category_key in focus_areas:
                if category_key in categories:
                    # Select top priority items from category
                    category_items = categories[category_key]['items'][:3]  # Top 3 items
                    period_items.extend([item['text'] for item in category_items])
            
            timeline[period] = {
                'date': target_date.isoformat(),
                'phase': schedule_info['phase'],
                'time_commitment': schedule_info['time_commitment'],
                'focus_areas': focus_areas,
                'key_activities': schedule_info['key_activities'],
                'checklist_items': period_items,
                'status': 'upcoming' if target_date >= now.date() else 'completed'
            }
        
        return timeline
    
    def _estimate_item_time(self, item):
        """Estimate time needed for checklist item"""
        time_estimates = {
            'research': 30,  # minutes
            'practice': 45,
            'prepare': 20,
            'review': 15,
            'test': 10,
            'plan': 15,
            'organize': 20,
            'contact': 10
        }
        
        item_lower = item.lower()
        for keyword, time in time_estimates.items():
            if keyword in item_lower:
                return time
        
        return 20  # Default estimate
    
    def _generate_checklist_recommendations(self, days_until, interview_type, user_preferences):
        """Generate personalized recommendations"""
        recommendations = []
        
        # Time-based recommendations
        if days_until <= 1:
            recommendations.extend([
                'Focus on logistics and mental preparation',
                'Avoid learning new information - review only',
                'Ensure all materials are prepared',
                'Get good rest and nutrition'
            ])
        elif days_until <= 3:
            recommendations.extend([
                'Intensive preparation mode - 2-3 hours daily',
                'Complete all technical practice',
                'Finalize all research and materials',
                'Conduct final mock interviews'
            ])
        elif days_until <= 7:
            recommendations.extend([
                'Deep preparation phase - 1-2 hours daily',
                'Focus on interviewer research',
                'Intensify skill-specific practice',
                'Begin finalizing materials'
            ])
        else:
            recommendations.extend([
                'Begin with company and role research',
                'Start developing STAR stories',
                'Create study schedule',
                'Begin technical skill practice'
            ])
        
        # Interview type specific recommendations
        type_recommendations = {
            'technical': [
                'Practice coding daily',
                'Focus on system design concepts',
                'Prepare technical questions to ask'
            ],
            'behavioral': [
                'Develop comprehensive STAR stories',
                'Practice storytelling and communication',
                'Research company culture deeply'
            ],
            'case_study': [
                'Practice structured problem-solving',
                'Review relevant frameworks',
                'Practice presenting solutions clearly'
            ]
        }
        
        if interview_type in type_recommendations:
            recommendations.extend(type_recommendations[interview_type])
        
        # User preference based recommendations
        experience_level = user_preferences.get('experience_level', 'mid')
        if experience_level == 'entry':
            recommendations.extend([
                'Focus on learning potential and enthusiasm',
                'Prepare examples from projects and internships',
                'Research entry-level expectations'
            ])
        elif experience_level == 'senior':
            recommendations.extend([
                'Prepare leadership and strategic examples',
                'Focus on business impact and results',
                'Prepare questions about company strategy'
            ])
        
        return recommendations
    
    def _identify_priority_items(self, categories):
        """Identify highest priority items across all categories"""
        priority_items = []
        
        for category_key, category in categories.items():
            for item in category['items']:
                if item['priority'] in ['critical', 'high']:
                    priority_items.append({
                        'text': item['text'],
                        'category': category['name'],
                        'priority': item['priority'],
                        'estimated_time': item['estimated_time']
                    })
        
        # Sort by priority weight
        priority_items.sort(
            key=lambda x: self.priority_weights.get(x['priority'], 0), 
            reverse=True
        )
        
        return priority_items[:10]  # Top 10 priority items
    
    def update_checklist_progress(self, checklist_id, item_updates):
        """Update checklist item completion status"""
        try:
            updates = []
            
            for update in item_updates:
                item_update = {
                    'checklist_id': checklist_id,
                    'category': update.get('category'),
                    'item_text': update.get('item_text'),
                    'completed': update.get('completed', False),
                    'completion_date': datetime.now().isoformat() if update.get('completed') else None,
                    'notes': update.get('notes', ''),
                    'updated_at': datetime.now().isoformat()
                }
                updates.append(item_update)
            
            return {
                'updates_processed': len(updates),
                'updates': updates,
                'status': 'success'
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def calculate_readiness_score(self, checklist_data):
        """Calculate interview readiness score based on checklist completion"""
        try:
            total_weight = 0
            completed_weight = 0
            
            for category_key, category in checklist_data.get('categories', {}).items():
                category_priority = category.get('priority', 'medium')
                category_weight = self.priority_weights.get(category_priority, 4)
                
                for item in category.get('items', []):
                    item_priority = item.get('priority', 'medium')
                    item_weight = self.priority_weights.get(item_priority, 4)
                    total_item_weight = category_weight * item_weight
                    
                    total_weight += total_item_weight
                    if item.get('completed', False):
                        completed_weight += total_item_weight
            
            readiness_score = (completed_weight / total_weight * 100) if total_weight > 0 else 0
            
            # Determine readiness level
            if readiness_score >= 90:
                readiness_level = 'Excellent'
            elif readiness_score >= 75:
                readiness_level = 'Good'
            elif readiness_score >= 60:
                readiness_level = 'Adequate'
            elif readiness_score >= 40:
                readiness_level = 'Needs Improvement'
            else:
                readiness_level = 'Insufficient'
            
            return {
                'readiness_score': round(readiness_score, 1),
                'readiness_level': readiness_level,
                'completed_items': sum(1 for cat in checklist_data.get('categories', {}).values() 
                                     for item in cat.get('items', []) if item.get('completed', False)),
                'total_items': sum(len(cat.get('items', [])) for cat in checklist_data.get('categories', {}).values()),
                'recommendations': self._get_readiness_recommendations(readiness_score, checklist_data)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _get_readiness_recommendations(self, score, checklist_data):
        """Get recommendations based on readiness score"""
        if score >= 90:
            return [
                'You\'re well prepared! Focus on rest and mental preparation',
                'Do light review only - avoid cramming',
                'Ensure all logistics are finalized'
            ]
        elif score >= 75:
            return [
                'Good preparation level - focus on remaining priorities',
                'Complete any high-priority items',
                'Practice key talking points once more'
            ]
        elif score >= 60:
            return [
                'Adequate preparation - prioritize remaining critical items',
                'Focus on company research and key examples',
                'Complete technical preparation if applicable'
            ]
        elif score >= 40:
            return [
                'Significant preparation needed - focus on essentials',
                'Prioritize research and basic preparation',
                'Consider requesting interview postponement if possible'
            ]
        else:
            return [
                'Insufficient preparation - immediate action required',
                'Focus only on absolute essentials',
                'Strongly consider rescheduling if possible'
            ]
    
    def generate_daily_prep_schedule(self, checklist_data, days_remaining):
        """Generate daily preparation schedule based on remaining time"""
        try:
            if days_remaining <= 0:
                return {'message': 'Interview is today or has passed'}
            
            # Get incomplete items
            incomplete_items = []
            for category in checklist_data.get('categories', {}).values():
                for item in category.get('items', []):
                    if not item.get('completed', False):
                        incomplete_items.append(item)
            
            if not incomplete_items:
                return {'message': 'All items completed!'}
            
            # Sort by priority
            incomplete_items.sort(
                key=lambda x: self.priority_weights.get(x.get('priority', 'medium'), 4),
                reverse=True
            )
            
            # Distribute items across remaining days
            items_per_day = len(incomplete_items) // days_remaining + 1
            daily_schedule = {}
            
            for day in range(days_remaining):
                day_date = (datetime.now() + timedelta(days=day)).date()
                start_idx = day * items_per_day
                end_idx = min((day + 1) * items_per_day, len(incomplete_items))
                day_items = incomplete_items[start_idx:end_idx]
                
                total_time = sum(item.get('estimated_time', 20) for item in day_items)
                
                daily_schedule[f'day_{day + 1}'] = {
                    'date': day_date.isoformat(),
                    'items': [item['text'] for item in day_items],
                    'estimated_time': f'{total_time} minutes',
                    'priority_distribution': self._analyze_priority_distribution(day_items),
                    'recommendations': self._get_daily_recommendations(day, days_remaining)
                }
            
            return daily_schedule
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_priority_distribution(self, items):
        """Analyze priority distribution of items"""
        priority_count = {}
        for item in items:
            priority = item.get('priority', 'medium')
            priority_count[priority] = priority_count.get(priority, 0) + 1
        return priority_count
    
    def _get_daily_recommendations(self, day_number, total_days):
        """Get recommendations for specific day in preparation timeline"""
        recommendations = []
        
        if day_number == 0:  # First day
            recommendations.extend([
                'Start with highest priority items',
                'Focus on research and foundational preparation',
                'Set up organized study environment'
            ])
        elif day_number == total_days - 1:  # Last day
            recommendations.extend([
                'Focus on final review and logistics',
                'Avoid learning new information',
                'Prioritize mental and physical preparation'
            ])
        else:  # Middle days
            recommendations.extend([
                'Balance preparation with practice',
                'Focus on skill development and examples',
                'Regular review of previous day\'s work'
            ])
        
        return recommendations
    
    def export_checklist(self, checklist_data, format='pdf'):
        """Export checklist in various formats"""
        try:
            if format == 'pdf':
                return {
                    'title': f"Interview Preparation Checklist - {checklist_data.get('interview_info', {}).get('company', 'Interview')}",
                    'sections': [
                        {'name': cat['name'], 'items': [item['text'] for item in cat['items']]}
                        for cat in checklist_data.get('categories', {}).values()
                    ],
                    'metadata': checklist_data.get('interview_info', {})
                }
            elif format == 'calendar':
                calendar_events = []
                for period, timeline in checklist_data.get('countdown_timeline', {}).items():
                    event = {
                        'title': f"Interview Prep: {timeline['phase']}",
                        'date': timeline['date'],
                        'description': f"Activities: {', '.join(timeline['key_activities'][:3])}",
                        'duration': timeline['time_commitment']
                    }
                    calendar_events.append(event)
                return calendar_events
            
            return checklist_data
            
        except Exception as e:
            return {'error': str(e)}