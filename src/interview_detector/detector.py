"""
Interview Type Detector
Automatically detects interview types and identifies interview-related emails
"""

import re
from typing import Dict, Any, List, Optional

class InterviewDetector:
    """Detects interview types and identifies interview-related emails"""
    
    def __init__(self):
        self.interview_keywords = self.load_interview_keywords()
        self.interview_type_patterns = self.load_type_patterns()
        print("🔍 Interview detector initialized")
    
    def load_interview_keywords(self) -> List[str]:
        """Load comprehensive keywords that indicate an email is interview-related"""
        return [
            # Direct interview mentions
            'interview', 'interviews', 'interviewing', 'interviewee',
            'phone interview', 'video interview', 'zoom interview',
            'skype interview', 'teams interview', 'google meet',
            
            # Screening and calls
            'phone call', 'video call', 'phone screen', 'screening',
            'initial call', 'quick call', 'brief call', 'intro call',
            'schedule a call', 'available for a call', 'time to chat',
            
            # Meeting terminology
            'meeting', 'chat', 'discussion', 'conversation',
            'connect', 'touch base', 'catch up', 'sync',
            
            # Process terminology
            'next steps', 'follow up', 'follow-up', 'next stage',
            'move forward', 'proceed', 'continue', 'advance',
            
            # Assessment types
            'technical assessment', 'coding challenge', 'take-home test',
            'skill assessment', 'technical test', 'coding test',
            'assignment', 'project', 'case study',
            
            # Interview rounds
            'first round', 'second round', 'third round', 'final round',
            'onsite', 'on-site', 'in-person', 'office visit',
            'panel interview', 'group interview', 'team interview',
            
            # People involved
            'hiring manager', 'team lead', 'recruiter', 'hr',
            'talent acquisition', 'recruitment', 'headhunter',
            'engineering manager', 'technical lead', 'cto', 'vp',
            
            # Application process
            'application', 'position', 'role', 'opportunity',
            'job opening', 'vacancy', 'candidate', 'applicant',
            'resume', 'cv', 'background', 'experience',
            
            # Company-specific patterns
            'join our team', 'career opportunity', 'talent',
            'potential fit', 'interested in you', 'your profile',
            
            # Scheduling keywords
            'calendar', 'calendly', 'schedule', 'book a time',
            'available', 'availability', 'free time', 'slot',
            'appointment', 'time slots', 'meeting request',
            
            # Urgency indicators
            'asap', 'urgent', 'soon', 'this week', 'next week',
            'immediate', 'priority', 'expedite'
        ]
    
    def load_type_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load patterns for different interview types"""
        return {
            'technical': {
                'keywords': [
                    'technical interview', 'coding interview', 'technical assessment',
                    'algorithm', 'data structure', 'coding challenge', 'programming',
                    'system design', 'architecture', 'technical discussion',
                    'code review', 'pair programming', 'whiteboard',
                    'leetcode', 'hackerrank', 'codility',
                    'technical skills', 'engineering', 'development'
                ],
                'context_clues': [
                    'solve problems', 'coding skills', 'technical expertise',
                    'programming languages', 'frameworks', 'databases',
                    'apis', 'scalability', 'performance'
                ]
            },
            'behavioral': {
                'keywords': [
                    'behavioral interview', 'cultural fit', 'team fit',
                    'leadership', 'teamwork', 'communication',
                    'personality', 'values', 'motivation',
                    'conflict resolution', 'problem solving',
                    'star method', 'tell me about', 'describe a time'
                ],
                'context_clues': [
                    'work style', 'team dynamics', 'company culture',
                    'past experience', 'challenges faced', 'achievements',
                    'strengths and weaknesses', 'career goals'
                ]
            },
            'system_design': {
                'keywords': [
                    'system design', 'architecture interview', 'design interview',
                    'scalability', 'distributed systems', 'microservices',
                    'load balancing', 'database design', 'api design',
                    'high level design', 'low level design'
                ],
                'context_clues': [
                    'design a system', 'architect a solution', 'scale to millions',
                    'handle traffic', 'database schema', 'caching strategy',
                    'monitoring', 'fault tolerance'
                ]
            },
            'phone_screen': {
                'keywords': [
                    'phone screen', 'phone screening', 'initial call',
                    'recruiter call', 'hr call', 'preliminary interview',
                    'screening call', 'brief call', 'quick chat'
                ],
                'context_clues': [
                    'get to know', 'background', 'experience overview',
                    'interest in role', 'availability', 'next steps'
                ]
            },
            'final_round': {
                'keywords': [
                    'final round', 'final interview', 'onsite interview',
                    'panel interview', 'meet the team', 'leadership interview',
                    'ceo interview', 'vp interview', 'director interview'
                ],
                'context_clues': [
                    'final step', 'last stage', 'decision making',
                    'senior leadership', 'executive team', 'final assessment'
                ]
            },
            'product': {
                'keywords': [
                    'product interview', 'product manager', 'product sense',
                    'product design', 'product strategy', 'product thinking',
                    'user experience', 'market analysis', 'feature prioritization'
                ],
                'context_clues': [
                    'product roadmap', 'user needs', 'market research',
                    'feature development', 'metrics', 'kpis',
                    'customer feedback', 'competitive analysis'
                ]
            },
            'case_study': {
                'keywords': [
                    'case study', 'business case', 'case interview',
                    'consulting case', 'problem solving exercise',
                    'analytical exercise', 'case analysis'
                ],
                'context_clues': [
                    'business problem', 'analytical thinking', 'framework',
                    'market sizing', 'profitability', 'strategy',
                    'recommendations', 'data analysis'
                ]
            },
            'presentation': {
                'keywords': [
                    'presentation', 'present to', 'demo', 'showcase',
                    'walk through', 'explain your work', 'show us',
                    'technical presentation', 'project presentation'
                ],
                'context_clues': [
                    'prepare slides', 'present your', 'demo your work',
                    'explain your approach', 'showcase your skills',
                    'walk us through'
                ]
            }
        }
    
    def is_interview_email(self, email: Dict[str, Any]) -> bool:
        """Determine if an email is interview-related"""
        subject = email.get('subject', '').lower()
        body = email.get('body', '').lower()
        sender = email.get('sender', '').lower()
        
        # Combine all text for analysis
        full_text = f"{subject} {body} {sender}"
        
        # Check for interview keywords
        for keyword in self.interview_keywords:
            if keyword in full_text:
                return True
        
        return False
    
    def detect_interview_type(self, email: Dict[str, Any]) -> str:
        """Detect the type of interview based on email content"""
        subject = email.get('subject', '').lower()
        body = email.get('body', '').lower()
        
        # Combine subject and body for analysis
        full_text = f"{subject} {body}"
        
        # Score each interview type based on keyword matches
        type_scores = {}
        
        for interview_type, patterns in self.interview_type_patterns.items():
            score = 0
            
            # Check keywords (higher weight)
            for keyword in patterns.get('keywords', []):
                if keyword in full_text:
                    score += 3
            
            # Check context clues (lower weight)
            for clue in patterns.get('context_clues', []):
                if clue in full_text:
                    score += 1
            
            type_scores[interview_type] = score
        
        # Return the type with highest score, or 'general' if no strong matches
        if not type_scores or max(type_scores.values()) == 0:
            return 'general'
        
        return max(type_scores, key=type_scores.get)
    
    def extract_company_name(self, email: Dict[str, Any]) -> str:
        """Extract company name from email sender"""
        sender = email.get('sender', '')
        
        if '@' in sender:
            domain = sender.split('@')[1]
            # Remove common email domains
            if domain in ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']:
                return 'Unknown'
            # Extract company name from domain
            company = domain.split('.')[0]
            return company.title()
        
        return 'Unknown'
    
    def extract_location(self, text: str) -> Optional[str]:
        """Extract location information from text"""
        # Common location patterns
        location_patterns = [
            r'\b([A-Z][a-z]+,\s*[A-Z]{2})\b',  # City, State
            r'\b([A-Z][a-z]+,\s*[A-Z][a-z]+)\b',  # City, Country
            r'\b(remote)\b',
            r'\b(onsite)\b',
            r'\b(hybrid)\b'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def assess_interview_priority(self, email: Dict[str, Any]) -> str:
        """Assess the priority/urgency of an interview"""
        subject = email.get('subject', '').lower()
        body = email.get('body', '').lower()
        full_text = f"{subject} {body}"
        
        # High priority indicators
        high_priority = [
            'urgent', 'asap', 'immediate', 'today', 'tomorrow',
            'final round', 'offer', 'decision', 'ceo', 'vp'
        ]
        
        # Medium priority indicators
        medium_priority = [
            'this week', 'next week', 'soon', 'priority',
            'technical interview', 'onsite', 'panel'
        ]
        
        for indicator in high_priority:
            if indicator in full_text:
                return 'high'
        
        for indicator in medium_priority:
            if indicator in full_text:
                return 'medium'
        
        return 'low'