import openai
import os
from datetime import datetime, timedelta
import json

class FollowUpManager:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Follow-up timeline templates
        self.follow_up_schedules = {
            'standard': {
                'thank_you': {'days': 0, 'hours': 2},  # 2 hours after interview
                'follow_up_1': {'days': 3, 'hours': 0},  # 3 days after
                'follow_up_2': {'days': 7, 'hours': 0},  # 1 week after
                'follow_up_3': {'days': 14, 'hours': 0}  # 2 weeks after
            },
            'aggressive': {
                'thank_you': {'days': 0, 'hours': 1},
                'follow_up_1': {'days': 2, 'hours': 0},
                'follow_up_2': {'days': 5, 'hours': 0},
                'follow_up_3': {'days': 10, 'hours': 0}
            },
            'conservative': {
                'thank_you': {'days': 0, 'hours': 4},
                'follow_up_1': {'days': 5, 'hours': 0},
                'follow_up_2': {'days': 10, 'hours': 0},
                'follow_up_3': {'days': 21, 'hours': 0}
            }
        }
        
        # Email templates
        self.email_templates = {
            'thank_you': {
                'subject': 'Thank you for the {position} interview',
                'template': """Dear {interviewer_name},

Thank you for taking the time to meet with me today to discuss the {position} role at {company}. I thoroughly enjoyed our conversation about {specific_topic} and learning more about {team_project}.

Our discussion reinforced my enthusiasm for the role, particularly {specific_interest}. I'm excited about the opportunity to contribute to {company_goal} and bring my experience in {relevant_skill} to the team.

{additional_point}

Please don't hesitate to reach out if you need any additional information. I look forward to hearing about the next steps in the process.

Best regards,
{your_name}"""
            },
            'follow_up_1': {
                'subject': 'Following up on our {position} interview',
                'template': """Dear {interviewer_name},

I hope this email finds you well. I wanted to follow up on our interview last {day_of_week} for the {position} position.

Since our conversation, I've been reflecting on {discussion_point} and wanted to share {additional_thought}. This has further strengthened my interest in the role and my confidence that I would be a great fit for your team.

I understand that hiring decisions take time, and I don't want to be pushy. However, I remain very interested in the position and would appreciate any updates you might be able to share about the timeline or next steps.

{optional_addition}

Thank you again for your consideration, and I look forward to hearing from you.

Best regards,
{your_name}"""
            },
            'follow_up_2': {
                'subject': 'Checking in regarding the {position} opportunity',
                'template': """Dear {interviewer_name},

I hope you're doing well. I'm writing to check in regarding the {position} role we discussed {time_ago}.

I remain very interested in the opportunity to join {company} and contribute to {specific_team_goal}. In the meantime, I've {recent_accomplishment} which I believe further demonstrates my qualifications for this role.

I understand that these processes can take time, and I appreciate your patience with my follow-up. If you need any additional information or references, please let me know.

I'd be grateful for any update you can provide on the status or timeline for the position.

Thank you for your time and consideration.

Best regards,
{your_name}"""
            },
            'final_follow_up': {
                'subject': 'Final follow-up on {position} opportunity',
                'template': """Dear {interviewer_name},

I hope this message finds you well. I'm reaching out one final time regarding the {position} position we discussed {time_ago}.

While I understand that hiring decisions involve many factors and timing considerations, I wanted to reiterate my strong interest in the role and {company}. The opportunity to {specific_contribution} continues to excite me.

I recognize that you may have moved forward with other candidates, and I completely understand if that's the case. However, if the position is still being considered or if similar opportunities arise in the future, I would welcome the chance to be considered.

Thank you for your time throughout this process. I have great respect for {company} and wish you and the team continued success.

Best regards,
{your_name}"""
            },
            'networking': {
                'subject': 'Great meeting you - let\'s stay connected',
                'template': """Dear {contact_name},

It was a pleasure meeting you {where_met}. I really enjoyed our conversation about {topic_discussed} and learning about your experience at {company}.

I'd love to stay connected and continue our discussion about {shared_interest}. Would you be open to connecting on LinkedIn?

{optional_question}

Thank you for sharing your insights, and I hope our paths cross again soon.

Best regards,
{your_name}"""
            }
        }
        
        # Status tracking
        self.interview_statuses = [
            'scheduled', 'completed', 'waiting_response', 'rejected', 
            'offer_received', 'accepted', 'declined'
        ]
        
        # Follow-up types
        self.follow_up_types = [
            'thank_you', 'status_inquiry', 'additional_info', 
            'networking', 'final_follow_up'
        ]
    
    def create_follow_up_plan(self, interview_data, strategy='standard'):
        """Create a comprehensive follow-up plan for an interview"""
        try:
            interview_date = datetime.fromisoformat(interview_data['interview_date'])
            schedule = self.follow_up_schedules.get(strategy, self.follow_up_schedules['standard'])
            
            follow_up_plan = {
                'interview_id': interview_data.get('id'),
                'company': interview_data.get('company'),
                'position': interview_data.get('position'),
                'interviewer': interview_data.get('interviewer'),
                'interview_date': interview_date.isoformat(),
                'strategy': strategy,
                'follow_ups': [],
                'created_at': datetime.now().isoformat()
            }
            
            # Generate follow-up schedule
            for follow_up_type, timing in schedule.items():
                follow_up_date = interview_date + timedelta(
                    days=timing['days'], 
                    hours=timing['hours']
                )
                
                follow_up_plan['follow_ups'].append({
                    'type': follow_up_type,
                    'scheduled_date': follow_up_date.isoformat(),
                    'status': 'pending',
                    'email_template': self._generate_email_content(
                        follow_up_type, interview_data
                    )
                })
            
            return follow_up_plan
            
        except Exception as e:
            print(f"Follow-up plan creation error: {e}")
            return {'error': str(e)}
    
    def _generate_email_content(self, follow_up_type, interview_data):
        """Generate personalized email content"""
        if follow_up_type not in self.email_templates:
            follow_up_type = 'follow_up_1'
        
        template = self.email_templates[follow_up_type]
        
        # Basic placeholders
        placeholders = {
            'position': interview_data.get('position', 'the position'),
            'company': interview_data.get('company', 'your company'),
            'interviewer_name': interview_data.get('interviewer', 'Hiring Manager'),
            'your_name': '[Your Name]',
            'specific_topic': '[Specific topic discussed]',
            'team_project': '[Team project mentioned]',
            'specific_interest': '[Specific aspect that interested you]',
            'company_goal': '[Company goal discussed]',
            'relevant_skill': '[Your relevant skill]',
            'additional_point': '[Additional point if needed]',
            'discussion_point': '[Specific point from discussion]',
            'additional_thought': '[Your additional thought]',
            'optional_addition': '[Optional additional content]',
            'time_ago': '[Time since interview]',
            'specific_team_goal': '[Specific team goal]',
            'recent_accomplishment': '[Recent accomplishment]',
            'specific_contribution': '[Specific contribution you could make]'
        }
        
        # Fill template
        subject = template['subject'].format(**placeholders)
        body = template['template'].format(**placeholders)
        
        return {
            'subject': subject,
            'body': body,
            'placeholders': placeholders
        }
    
    def personalize_email(self, template_content, personal_details):
        """Personalize email template with specific details"""
        try:
            # Use AI to enhance personalization
            prompt = f"""
            Personalize this follow-up email template with the following details:
            
            Template: {template_content['body']}
            
            Personal Details:
            - Specific topics discussed: {personal_details.get('topics_discussed', 'N/A')}
            - Interviewer insights: {personal_details.get('interviewer_insights', 'N/A')}
            - Company interests: {personal_details.get('company_interests', 'N/A')}
            - Your relevant experience: {personal_details.get('relevant_experience', 'N/A')}
            - Additional points to mention: {personal_details.get('additional_points', 'N/A')}
            
            Replace the placeholder text with specific, personalized content that sounds natural and professional.
            Keep the same tone and structure but make it more specific and engaging.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            personalized_body = response.choices[0].message.content
            
            return {
                'subject': template_content['subject'].replace('[', '').replace(']', ''),
                'body': personalized_body,
                'personalized': True
            }
            
        except Exception as e:
            print(f"Email personalization error: {e}")
            return {
                'subject': template_content['subject'],
                'body': template_content['body'],
                'personalized': False,
                'error': str(e)
            }
    
    def track_follow_up(self, follow_up_id, action_taken, response_received=None):
        """Track follow-up actions and responses"""
        try:
            follow_up_record = {
                'follow_up_id': follow_up_id,
                'action_taken': action_taken,
                'date_sent': datetime.now().isoformat(),
                'response_received': response_received,
                'status': 'sent',
                'notes': ''
            }
            
            if response_received:
                follow_up_record['status'] = 'responded'
                follow_up_record['response_date'] = datetime.now().isoformat()
                follow_up_record['next_action'] = self._determine_next_action(response_received)
            
            return follow_up_record
            
        except Exception as e:
            return {'error': str(e)}
    
    def _determine_next_action(self, response_content):
        """Determine next action based on response received"""
        response_lower = response_content.lower()
        
        if any(phrase in response_lower for phrase in ['thank you', 'received', 'reviewing']):
            return 'wait_for_decision'
        elif any(phrase in response_lower for phrase in ['schedule', 'next interview', 'meet']):
            return 'prepare_for_next_interview'
        elif any(phrase in response_lower for phrase in ['unfortunately', 'decided', 'other candidate']):
            return 'send_final_thank_you'
        elif any(phrase in response_lower for phrase in ['questions', 'information', 'clarify']):
            return 'provide_additional_info'
        else:
            return 'analyze_response'
    
    def generate_follow_up_reminders(self, follow_up_plans):
        """Generate reminders for upcoming follow-ups"""
        try:
            now = datetime.now()
            reminders = []
            
            for plan in follow_up_plans:
                for follow_up in plan['follow_ups']:
                    if follow_up['status'] == 'pending':
                        scheduled_date = datetime.fromisoformat(follow_up['scheduled_date'])
                        
                        # Check if it's time for follow-up
                        if scheduled_date <= now:
                            reminders.append({
                                'type': 'overdue',
                                'company': plan['company'],
                                'position': plan['position'],
                                'follow_up_type': follow_up['type'],
                                'scheduled_date': follow_up['scheduled_date'],
                                'email_template': follow_up['email_template']
                            })
                        elif scheduled_date <= now + timedelta(hours=24):
                            reminders.append({
                                'type': 'upcoming',
                                'company': plan['company'],
                                'position': plan['position'],
                                'follow_up_type': follow_up['type'],
                                'scheduled_date': follow_up['scheduled_date'],
                                'email_template': follow_up['email_template']
                            })
            
            return reminders
            
        except Exception as e:
            print(f"Reminder generation error: {e}")
            return []
    
    def analyze_response_sentiment(self, response_text):
        """Analyze the sentiment and intent of interview responses"""
        try:
            prompt = f"""
            Analyze this interview follow-up response and determine:
            1. Overall sentiment (positive, neutral, negative)
            2. Likelihood of getting the job (high, medium, low)
            3. Recommended next action
            4. Key insights from the response
            
            Response: "{response_text}"
            
            Provide analysis in JSON format with keys: sentiment, likelihood, next_action, insights.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.3
            )
            
            try:
                analysis = json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                # Fallback to simple analysis
                analysis = {
                    'sentiment': 'neutral',
                    'likelihood': 'medium',
                    'next_action': 'wait_for_update',
                    'insights': ['Unable to perform detailed analysis']
                }
            
            return analysis
            
        except Exception as e:
            return {
                'sentiment': 'unknown',
                'likelihood': 'unknown',
                'next_action': 'manual_review',
                'insights': [f'Analysis error: {str(e)}'],
                'error': str(e)
            }
    
    def get_follow_up_statistics(self, follow_up_history):
        """Generate statistics from follow-up history"""
        try:
            stats = {
                'total_follow_ups': len(follow_up_history),
                'response_rate': 0,
                'average_response_time': 0,
                'most_effective_timing': {},
                'success_rate_by_type': {}
            }
            
            responses = [f for f in follow_up_history if f.get('response_received')]
            stats['response_rate'] = len(responses) / len(follow_up_history) * 100 if follow_up_history else 0
            
            # Calculate average response time
            response_times = []
            for follow_up in responses:
                if follow_up.get('date_sent') and follow_up.get('response_date'):
                    sent_date = datetime.fromisoformat(follow_up['date_sent'])
                    response_date = datetime.fromisoformat(follow_up['response_date'])
                    response_times.append((response_date - sent_date).total_seconds() / 3600)  # Hours
            
            if response_times:
                stats['average_response_time'] = sum(response_times) / len(response_times)
            
            return stats
            
        except Exception as e:
            return {'error': str(e)}
    
    def create_networking_follow_up(self, contact_info, meeting_context):
        """Create follow-up for networking contacts"""
        try:
            template = self.email_templates['networking']
            
            placeholders = {
                'contact_name': contact_info.get('name', 'there'),
                'where_met': meeting_context.get('location', 'recently'),
                'topic_discussed': meeting_context.get('topic', 'your work'),
                'company': contact_info.get('company', 'your company'),
                'shared_interest': meeting_context.get('shared_interest', 'industry trends'),
                'optional_question': meeting_context.get('follow_up_question', ''),
                'your_name': '[Your Name]'
            }
            
            networking_follow_up = {
                'type': 'networking',
                'contact': contact_info,
                'email_content': {
                    'subject': template['subject'].format(**placeholders),
                    'body': template['template'].format(**placeholders)
                },
                'suggested_timeline': {
                    'immediate': 'Send within 24 hours',
                    'follow_up': 'Check in after 2-3 weeks',
                    'long_term': 'Maintain contact quarterly'
                },
                'created_at': datetime.now().isoformat()
            }
            
            return networking_follow_up
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_best_practices(self):
        """Get follow-up best practices and tips"""
        return {
            'timing': [
                'Send thank you email within 24 hours',
                'Wait 3-5 business days for first follow-up',
                'Space subsequent follow-ups 1-2 weeks apart',
                'Send final follow-up after 3-4 weeks total'
            ],
            'content': [
                'Reference specific conversation points',
                'Reiterate your interest and qualifications',
                'Provide additional relevant information',
                'Keep emails concise and professional',
                'Always proofread before sending'
            ],
            'strategy': [
                'Adapt timing based on company culture',
                'Use different channels if email gets no response',
                'Connect on LinkedIn after interview',
                'Follow up with multiple interviewers if applicable',
                'Know when to stop following up'
            ],
            'red_flags': [
                'Following up too frequently',
                'Being overly aggressive or pushy',
                'Sending generic, impersonal messages',
                'Continuing after clear rejection',
                'Following up on wrong contact information'
            ]
        }
    
    def export_follow_up_plan(self, follow_up_plan, format='calendar'):
        """Export follow-up plan to calendar or task list format"""
        try:
            if format == 'calendar':
                calendar_events = []
                for follow_up in follow_up_plan['follow_ups']:
                    event = {
                        'title': f"Follow up: {follow_up_plan['company']} - {follow_up['type']}",
                        'date': follow_up['scheduled_date'],
                        'description': f"Send {follow_up['type']} email for {follow_up_plan['position']} position",
                        'type': 'reminder'
                    }
                    calendar_events.append(event)
                return calendar_events
            
            elif format == 'checklist':
                checklist = []
                for follow_up in follow_up_plan['follow_ups']:
                    task = {
                        'task': f"Send {follow_up['type']} email to {follow_up_plan['company']}",
                        'due_date': follow_up['scheduled_date'],
                        'status': follow_up['status'],
                        'priority': 'high' if follow_up['type'] == 'thank_you' else 'medium'
                    }
                    checklist.append(task)
                return checklist
            
            return {'error': 'Unsupported export format'}
            
        except Exception as e:
            return {'error': str(e)}