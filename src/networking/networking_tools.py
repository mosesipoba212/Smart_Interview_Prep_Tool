import openai
import os
import requests
from datetime import datetime, timedelta
import json
import re

class NetworkingTools:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # LinkedIn connection message templates
        self.connection_templates = {
            'after_interview': {
                'subject': 'Great meeting you during the {position} interview',
                'message': """Hi {name},

It was a pleasure meeting you during the {position} interview at {company}. I really enjoyed our conversation about {topic_discussed} and learning more about {team_info}.

I'd love to stay connected and continue our discussion about {shared_interest}. 

Best regards,
{your_name}"""
            },
            'networking_event': {
                'subject': 'Great meeting you at {event_name}',
                'message': """Hi {name},

It was great meeting you at {event_name}. I enjoyed our conversation about {topic_discussed} and would love to stay connected.

{follow_up_question}

Looking forward to keeping in touch!

Best,
{your_name}"""
            },
            'referral_request': {
                'subject': 'Exploring opportunities at {company}',
                'message': """Hi {name},

I hope you're doing well! I'm currently exploring new opportunities and noticed that you work at {company}. I'm very interested in {specific_role} positions there.

Would you be open to having a brief conversation about your experience at {company} and the team culture? I'd love to learn more about {specific_aspect}.

{optional_attachment_mention}

Thank you for your time!

Best regards,
{your_name}"""
            },
            'informational_interview': {
                'subject': 'Seeking career insights in {industry}',
                'message': """Hi {name},

I hope this message finds you well. I'm currently {your_situation} and very interested in learning more about {industry/role}.

I've been following your career journey and would love to learn from your experience. Would you be open to a brief 15-20 minute conversation about your path and insights about {specific_topic}?

I'm particularly interested in learning about {specific_questions}.

Thank you for considering!

Best regards,
{your_name}"""
            },
            'cold_outreach': {
                'subject': 'Admiring your work in {field}',
                'message': """Hi {name},

I hope you're having a great week! I've been following your work in {field} and particularly admired {specific_work_example}.

I'm currently {your_situation} and would love to learn from your experience. Would you be open to connecting?

{specific_question_or_comment}

Best regards,
{your_name}"""
            }
        }
        
        # Industry networking strategies
        self.industry_strategies = {
            'technology': {
                'platforms': ['LinkedIn', 'GitHub', 'Twitter', 'Meetup', 'Discord'],
                'events': ['Tech meetups', 'Hackathons', 'Conferences', 'Virtual webinars'],
                'conversation_starters': [
                    'Recent tech trends and innovations',
                    'Programming languages and frameworks',
                    'Open source contributions',
                    'Technical challenges and solutions'
                ],
                'value_propositions': [
                    'Technical skills and experience',
                    'Problem-solving abilities',
                    'Learning agility',
                    'Collaboration skills'
                ]
            },
            'finance': {
                'platforms': ['LinkedIn', 'Bloomberg Terminal', 'FinTech communities'],
                'events': ['Industry conferences', 'CFA events', 'Webinars'],
                'conversation_starters': [
                    'Market trends and analysis',
                    'Regulatory changes',
                    'Financial technology innovations',
                    'Investment strategies'
                ],
                'value_propositions': [
                    'Analytical skills',
                    'Attention to detail',
                    'Risk management experience',
                    'Client relationship skills'
                ]
            },
            'marketing': {
                'platforms': ['LinkedIn', 'Twitter', 'Instagram', 'Marketing communities'],
                'events': ['Marketing conferences', 'Brand workshops', 'Digital events'],
                'conversation_starters': [
                    'Digital marketing trends',
                    'Brand strategy insights',
                    'Consumer behavior changes',
                    'Creative campaign ideas'
                ],
                'value_propositions': [
                    'Creative thinking',
                    'Data analysis skills',
                    'Campaign management',
                    'Brand development'
                ]
            }
        }
        
        # Networking goal types
        self.networking_goals = [
            'job_search', 'career_guidance', 'industry_insights',
            'skill_development', 'mentorship', 'partnerships',
            'knowledge_sharing', 'personal_branding'
        ]
        
        # Professional relationship stages
        self.relationship_stages = [
            'first_contact', 'initial_connection', 'building_rapport',
            'regular_contact', 'strong_relationship', 'mutual_benefit'
        ]
        
        # Follow-up timelines
        self.follow_up_schedules = {
            'immediate': {'days': 1, 'message': 'Thank you for connecting'},
            'short_term': {'days': 7, 'message': 'Follow up on discussion'},
            'medium_term': {'days': 30, 'message': 'Check in and update'},
            'long_term': {'days': 90, 'message': 'Quarterly connection'}
        }
    
    def create_networking_strategy(self, user_profile, goals):
        """Create personalized networking strategy"""
        try:
            strategy = {
                'user_profile': user_profile,
                'networking_goals': goals,
                'target_connections': self._identify_target_connections(user_profile, goals),
                'platform_strategy': self._create_platform_strategy(user_profile),
                'outreach_plan': self._create_outreach_plan(user_profile, goals),
                'content_strategy': self._create_content_strategy(user_profile),
                'event_recommendations': self._recommend_events(user_profile),
                'timeline': self._create_networking_timeline(goals),
                'success_metrics': self._define_success_metrics(goals),
                'created_at': datetime.now().isoformat()
            }
            
            return strategy
            
        except Exception as e:
            return {'error': str(e)}
    
    def _identify_target_connections(self, user_profile, goals):
        """Identify target connections based on profile and goals"""
        try:
            industry = user_profile.get('industry', 'technology')
            role_level = user_profile.get('level', 'mid')
            
            target_types = []
            
            if 'job_search' in goals:
                target_types.extend([
                    'Hiring managers in target companies',
                    'Recruiters in industry',
                    'Employees at target companies',
                    'Former colleagues in new roles'
                ])
            
            if 'career_guidance' in goals:
                target_types.extend([
                    'Senior professionals in industry',
                    'People in target roles',
                    'Career coaches and mentors',
                    'Industry thought leaders'
                ])
            
            if 'industry_insights' in goals:
                target_types.extend([
                    'Industry analysts and experts',
                    'Conference speakers and authors',
                    'Founders and executives',
                    'Journalists covering the industry'
                ])
            
            return {
                'primary_targets': target_types[:5],
                'secondary_targets': target_types[5:],
                'target_companies': user_profile.get('target_companies', []),
                'target_roles': user_profile.get('target_roles', []),
                'geographic_focus': user_profile.get('location_preferences', ['Local', 'Remote'])
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _create_platform_strategy(self, user_profile):
        """Create platform-specific networking strategy"""
        industry = user_profile.get('industry', 'technology')
        strategy_info = self.industry_strategies.get(industry, self.industry_strategies['technology'])
        
        platform_strategy = {
            'linkedin': {
                'priority': 'high',
                'activities': [
                    'Optimize profile for target role',
                    'Share industry insights regularly',
                    'Engage with target connections\' content',
                    'Send personalized connection requests',
                    'Participate in relevant groups'
                ],
                'posting_frequency': '2-3 times per week',
                'engagement_targets': '5-10 meaningful interactions daily'
            },
            'twitter': {
                'priority': 'medium' if industry == 'technology' else 'low',
                'activities': [
                    'Follow industry leaders',
                    'Share quick insights and articles',
                    'Participate in industry Twitter chats',
                    'Comment on trending topics'
                ],
                'posting_frequency': 'Daily',
                'engagement_targets': '3-5 interactions daily'
            },
            'industry_specific': {
                'platforms': strategy_info['platforms'],
                'events': strategy_info['events'],
                'conversation_starters': strategy_info['conversation_starters']
            }
        }
        
        return platform_strategy
    
    def _create_outreach_plan(self, user_profile, goals):
        """Create structured outreach plan"""
        outreach_plan = {
            'weekly_targets': {
                'new_connections': 5,
                'follow_up_messages': 10,
                'content_engagements': 15,
                'event_participations': 1
            },
            'message_cadence': {
                'connection_requests': '3-5 per day',
                'follow_ups': '2-3 per day',
                'cold_outreach': '1-2 per day'
            },
            'personalization_requirements': {
                'connection_requests': 'Always personalized',
                'follow_ups': 'Reference previous conversation',
                'content_sharing': 'Add personal insight'
            },
            'response_management': {
                'response_time_target': '24 hours',
                'follow_up_schedule': self.follow_up_schedules,
                'escalation_strategy': 'LinkedIn -> Email -> Phone'
            }
        }
        
        return outreach_plan
    
    def generate_connection_message(self, template_type, personalization_data):
        """Generate personalized connection message"""
        try:
            if template_type not in self.connection_templates:
                template_type = 'networking_event'
            
            template = self.connection_templates[template_type]
            
            # Fill in template with personalization data
            message = template['message'].format(**personalization_data)
            subject = template['subject'].format(**personalization_data)
            
            # Use AI to enhance personalization
            enhancement_prompt = f"""
            Enhance this networking message to make it more personal and engaging:
            
            Subject: {subject}
            Message: {message}
            
            Context: {personalization_data.get('context', '')}
            
            Make it sound natural, professional, and genuinely interested. Keep it concise but warm.
            Ensure it's not overly salesy or generic.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": enhancement_prompt}],
                max_tokens=300,
                temperature=0.7
            )
            
            enhanced_message = response.choices[0].message.content
            
            return {
                'original': {'subject': subject, 'message': message},
                'enhanced': enhanced_message,
                'template_type': template_type,
                'personalization_score': self._calculate_personalization_score(enhanced_message),
                'suggested_timing': self._suggest_optimal_timing(template_type)
            }
            
        except Exception as e:
            return {
                'original': template,
                'enhanced': template['message'],
                'error': str(e)
            }
    
    def optimize_linkedin_profile(self, profile_data, target_role):
        """Generate LinkedIn profile optimization recommendations"""
        try:
            optimization_prompt = f"""
            Analyze this LinkedIn profile and provide specific optimization recommendations for targeting {target_role} roles:
            
            Current Profile:
            - Headline: {profile_data.get('headline', 'Not provided')}
            - Summary: {profile_data.get('summary', 'Not provided')}
            - Experience: {profile_data.get('experience_count', 0)} positions
            - Skills: {', '.join(profile_data.get('skills', []))}
            - Industry: {profile_data.get('industry', 'Not specified')}
            
            Target Role: {target_role}
            
            Provide recommendations for:
            1. Headline optimization
            2. Summary improvement
            3. Skills to add/highlight
            4. Keywords to include
            5. Content strategy
            6. Profile completeness
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": optimization_prompt}],
                max_tokens=600,
                temperature=0.7
            )
            
            ai_recommendations = response.choices[0].message.content
            
            # Add structured recommendations
            optimization_tips = {
                'ai_recommendations': ai_recommendations,
                'headline_templates': self._generate_headline_templates(target_role),
                'summary_structure': self._suggest_summary_structure(target_role),
                'keyword_suggestions': self._suggest_keywords(target_role),
                'content_ideas': self._suggest_content_ideas(target_role),
                'profile_completeness_score': self._calculate_profile_completeness(profile_data),
                'next_actions': self._prioritize_profile_actions(profile_data, target_role)
            }
            
            return optimization_tips
            
        except Exception as e:
            return {'error': str(e)}
    
    def track_networking_activities(self, activities):
        """Track and analyze networking activities"""
        try:
            tracking_data = {
                'total_connections_made': 0,
                'response_rates': {},
                'most_effective_templates': {},
                'best_outreach_times': {},
                'platform_performance': {},
                'goal_progress': {},
                'relationship_progression': {},
                'roi_analysis': {}
            }
            
            for activity in activities:
                # Track connections
                if activity.get('type') == 'connection_request':
                    tracking_data['total_connections_made'] += 1
                
                # Track response rates
                template_type = activity.get('template_type', 'unknown')
                if template_type not in tracking_data['response_rates']:
                    tracking_data['response_rates'][template_type] = {'sent': 0, 'responses': 0}
                
                tracking_data['response_rates'][template_type]['sent'] += 1
                if activity.get('response_received'):
                    tracking_data['response_rates'][template_type]['responses'] += 1
                
                # Track timing effectiveness
                send_time = activity.get('sent_time', '')
                if send_time:
                    hour = datetime.fromisoformat(send_time).hour
                    time_bucket = f"{hour:02d}:00"
                    if time_bucket not in tracking_data['best_outreach_times']:
                        tracking_data['best_outreach_times'][time_bucket] = {'sent': 0, 'responses': 0}
                    
                    tracking_data['best_outreach_times'][time_bucket]['sent'] += 1
                    if activity.get('response_received'):
                        tracking_data['best_outreach_times'][time_bucket]['responses'] += 1
            
            # Calculate response rates
            for template_type in tracking_data['response_rates']:
                data = tracking_data['response_rates'][template_type]
                data['rate'] = data['responses'] / data['sent'] if data['sent'] > 0 else 0
            
            return tracking_data
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_networking_opportunities(self, location, industry, interests):
        """Find networking opportunities and events"""
        try:
            # This would typically integrate with event APIs
            # For now, providing structured recommendations
            
            opportunities = {
                'virtual_events': [
                    f"{industry} virtual meetups",
                    "Professional webinars",
                    "Online conferences",
                    "Virtual networking sessions"
                ],
                'local_events': [
                    f"Local {industry} meetups",
                    "Chamber of Commerce events",
                    "Professional association meetings",
                    "University alumni events"
                ],
                'online_communities': [
                    f"{industry} LinkedIn groups",
                    "Reddit professional communities",
                    "Discord servers",
                    "Slack workspaces"
                ],
                'conferences': [
                    f"Major {industry} conferences",
                    "Trade shows",
                    "Summit events",
                    "Workshop series"
                ],
                'recommended_timing': {
                    'best_days': ['Tuesday', 'Wednesday', 'Thursday'],
                    'best_times': ['Morning coffee events', 'Lunch networking', 'After-work mixers'],
                    'seasonal_considerations': 'Avoid major holidays and summer vacation periods'
                }
            }
            
            return opportunities
            
        except Exception as e:
            return {'error': str(e)}
    
    def create_relationship_map(self, connections):
        """Create visual relationship mapping"""
        try:
            relationship_map = {
                'direct_connections': [],
                'second_degree_opportunities': [],
                'key_influencers': [],
                'mutual_connections': [],
                'relationship_strength': {},
                'networking_paths': {},
                'gap_analysis': {}
            }
            
            for connection in connections:
                # Categorize connections
                relationship_strength = connection.get('interaction_frequency', 0)
                
                if relationship_strength >= 5:
                    relationship_map['key_influencers'].append(connection)
                elif relationship_strength >= 2:
                    relationship_map['direct_connections'].append(connection)
                else:
                    relationship_map['second_degree_opportunities'].append(connection)
                
                # Analyze relationship strength
                relationship_map['relationship_strength'][connection.get('name', 'Unknown')] = {
                    'strength_score': relationship_strength,
                    'last_interaction': connection.get('last_interaction', ''),
                    'interaction_type': connection.get('interaction_type', ''),
                    'mutual_interests': connection.get('mutual_interests', []),
                    'potential_value': connection.get('potential_value', 'medium')
                }
            
            # Identify networking gaps
            relationship_map['gap_analysis'] = self._identify_networking_gaps(connections)
            
            return relationship_map
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_personalization_score(self, message):
        """Calculate personalization score of message"""
        try:
            # Simple scoring based on personalization indicators
            score = 0
            
            # Check for personal details
            if any(indicator in message.lower() for indicator in ['your', 'you\'re', 'your work', 'your experience']):
                score += 20
            
            # Check for specific references
            if any(indicator in message for indicator in ['company', 'role', 'project', 'article']):
                score += 20
            
            # Check for genuine interest indicators
            if any(indicator in message.lower() for indicator in ['interested in', 'admire', 'impressed', 'learned']):
                score += 15
            
            # Check for specific questions
            if '?' in message:
                score += 10
            
            # Check for mutual connections or interests
            if any(indicator in message.lower() for indicator in ['mutual', 'both', 'shared']):
                score += 15
            
            # Avoid generic language
            if any(generic in message.lower() for generic in ['dear sir/madam', 'to whom it may concern', 'i hope this finds you well']):
                score -= 20
            
            return min(100, max(0, score))
            
        except Exception as e:
            return 50  # Default score
    
    def _suggest_optimal_timing(self, template_type):
        """Suggest optimal timing for different message types"""
        timing_suggestions = {
            'after_interview': 'Within 24 hours of interview',
            'networking_event': 'Within 48 hours of event',
            'referral_request': 'Tuesday-Thursday, 10 AM - 2 PM',
            'informational_interview': 'Tuesday-Thursday, morning hours',
            'cold_outreach': 'Tuesday-Wednesday, 9 AM - 11 AM'
        }
        
        return timing_suggestions.get(template_type, 'Tuesday-Thursday, business hours')
    
    def _identify_networking_gaps(self, connections):
        """Identify gaps in networking coverage"""
        gaps = {
            'industry_coverage': [],
            'role_level_gaps': [],
            'company_type_gaps': [],
            'geographic_gaps': [],
            'functional_area_gaps': []
        }
        
        # Analyze current network composition
        industries = [c.get('industry', 'Unknown') for c in connections]
        roles = [c.get('role_level', 'Unknown') for c in connections]
        
        # Identify missing industries
        target_industries = ['Technology', 'Finance', 'Healthcare', 'Education', 'Manufacturing']
        gaps['industry_coverage'] = [ind for ind in target_industries if ind not in industries]
        
        # Identify missing role levels
        target_levels = ['Entry', 'Mid', 'Senior', 'Executive', 'C-Suite']
        gaps['role_level_gaps'] = [level for level in target_levels if level not in roles]
        
        return gaps
    
    def generate_networking_report(self, networking_data):
        """Generate comprehensive networking performance report"""
        try:
            report = {
                'executive_summary': {
                    'total_connections': len(networking_data.get('connections', [])),
                    'monthly_growth': self._calculate_connection_growth(networking_data),
                    'response_rate': self._calculate_overall_response_rate(networking_data),
                    'top_performing_strategy': self._identify_top_strategy(networking_data)
                },
                'performance_metrics': {
                    'connection_quality_score': self._assess_connection_quality(networking_data),
                    'engagement_effectiveness': self._measure_engagement_effectiveness(networking_data),
                    'goal_achievement': self._assess_goal_achievement(networking_data),
                    'roi_analysis': self._calculate_networking_roi(networking_data)
                },
                'recommendations': {
                    'immediate_actions': self._suggest_immediate_actions(networking_data),
                    'strategy_adjustments': self._suggest_strategy_adjustments(networking_data),
                    'long_term_goals': self._suggest_long_term_goals(networking_data)
                },
                'next_month_plan': self._create_next_month_plan(networking_data),
                'generated_at': datetime.now().isoformat()
            }
            
            return report
            
        except Exception as e:
            return {'error': str(e)}