import json
import openai
import os
from datetime import datetime

class SalaryNegotiationTools:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Salary ranges by role, level, and location (rough estimates in USD)
        self.salary_data = {
            'software_engineer': {
                'junior': {
                    'san_francisco': {'min': 130000, 'max': 160000},
                    'new_york': {'min': 120000, 'max': 150000},
                    'seattle': {'min': 125000, 'max': 155000},
                    'austin': {'min': 95000, 'max': 125000},
                    'chicago': {'min': 85000, 'max': 115000},
                    'boston': {'min': 100000, 'max': 130000},
                    'remote': {'min': 90000, 'max': 130000},
                    'london': {'min': 65000, 'max': 85000},  # GBP
                    'toronto': {'min': 75000, 'max': 95000},  # CAD
                    'default': {'min': 80000, 'max': 110000}
                },
                'mid': {
                    'san_francisco': {'min': 160000, 'max': 220000},
                    'new_york': {'min': 150000, 'max': 200000},
                    'seattle': {'min': 155000, 'max': 210000},
                    'austin': {'min': 125000, 'max': 165000},
                    'chicago': {'min': 115000, 'max': 155000},
                    'boston': {'min': 130000, 'max': 170000},
                    'remote': {'min': 130000, 'max': 180000},
                    'london': {'min': 85000, 'max': 120000},  # GBP
                    'toronto': {'min': 95000, 'max': 130000},  # CAD
                    'default': {'min': 110000, 'max': 150000}
                },
                'senior': {
                    'san_francisco': {'min': 220000, 'max': 350000},
                    'new_york': {'min': 200000, 'max': 300000},
                    'seattle': {'min': 210000, 'max': 320000},
                    'austin': {'min': 165000, 'max': 240000},
                    'chicago': {'min': 155000, 'max': 220000},
                    'boston': {'min': 170000, 'max': 250000},
                    'remote': {'min': 180000, 'max': 280000},
                    'london': {'min': 120000, 'max': 180000},  # GBP
                    'toronto': {'min': 130000, 'max': 190000},  # CAD
                    'default': {'min': 150000, 'max': 250000}
                },
                'staff': {
                    'san_francisco': {'min': 350000, 'max': 550000},
                    'new_york': {'min': 300000, 'max': 450000},
                    'seattle': {'min': 320000, 'max': 500000},
                    'austin': {'min': 240000, 'max': 380000},
                    'chicago': {'min': 220000, 'max': 350000},
                    'boston': {'min': 250000, 'max': 400000},
                    'remote': {'min': 280000, 'max': 450000},
                    'london': {'min': 180000, 'max': 280000},  # GBP
                    'toronto': {'min': 190000, 'max': 300000},  # CAD
                    'default': {'min': 250000, 'max': 400000}
                }
            },
            'product_manager': {
                'junior': {
                    'san_francisco': {'min': 140000, 'max': 170000},
                    'new_york': {'min': 130000, 'max': 160000},
                    'seattle': {'min': 135000, 'max': 165000},
                    'default': {'min': 100000, 'max': 140000}
                },
                'mid': {
                    'san_francisco': {'min': 170000, 'max': 240000},
                    'new_york': {'min': 160000, 'max': 220000},
                    'seattle': {'min': 165000, 'max': 230000},
                    'default': {'min': 130000, 'max': 180000}
                },
                'senior': {
                    'san_francisco': {'min': 240000, 'max': 380000},
                    'new_york': {'min': 220000, 'max': 340000},
                    'seattle': {'min': 230000, 'max': 360000},
                    'default': {'min': 180000, 'max': 280000}
                }
            },
            'data_scientist': {
                'junior': {
                    'san_francisco': {'min': 125000, 'max': 155000},
                    'new_york': {'min': 115000, 'max': 145000},
                    'seattle': {'min': 120000, 'max': 150000},
                    'default': {'min': 90000, 'max': 125000}
                },
                'mid': {
                    'san_francisco': {'min': 155000, 'max': 210000},
                    'new_york': {'min': 145000, 'max': 190000},
                    'seattle': {'min': 150000, 'max': 200000},
                    'default': {'min': 120000, 'max': 170000}
                },
                'senior': {
                    'san_francisco': {'min': 210000, 'max': 320000},
                    'new_york': {'min': 190000, 'max': 280000},
                    'seattle': {'min': 200000, 'max': 300000},
                    'default': {'min': 170000, 'max': 250000}
                }
            }
        }
        
        # Benefits and perks data
        self.benefits_data = {
            'health_insurance': {
                'value_percent': 8,  # 8% of base salary
                'negotiable': True,
                'priority': 'high'
            },
            'dental_vision': {
                'value_percent': 2,
                'negotiable': True,
                'priority': 'medium'
            },
            'retirement_401k': {
                'value_percent': 6,
                'negotiable': False,
                'priority': 'high'
            },
            'stock_options': {
                'value_percent': 15,  # Varies widely
                'negotiable': True,
                'priority': 'high'
            },
            'pto_vacation': {
                'value_percent': 4,
                'negotiable': True,
                'priority': 'high'
            },
            'remote_work': {
                'value_percent': 5,  # Cost savings
                'negotiable': True,
                'priority': 'medium'
            },
            'professional_development': {
                'value_percent': 2,
                'negotiable': True,
                'priority': 'medium'
            },
            'signing_bonus': {
                'value_percent': 10,  # One-time
                'negotiable': True,
                'priority': 'medium'
            }
        }
        
        # Negotiation strategies and tips
        self.negotiation_strategies = {
            'preparation': [
                "Research market rates for your role and location",
                "Know your own value and accomplishments",
                "Prepare multiple scenarios and alternatives",
                "Practice your negotiation conversation",
                "Understand the company's compensation philosophy"
            ],
            'timing': [
                "Wait for the offer before discussing salary",
                "Don't accept the first offer immediately",
                "Negotiate after receiving the written offer",
                "Give yourself time to think and respond",
                "Be prepared for multiple rounds of negotiation"
            ],
            'communication': [
                "Express enthusiasm for the role and company",
                "Frame requests in terms of market value",
                "Be specific about your expectations",
                "Listen actively to their constraints",
                "Maintain a collaborative tone throughout"
            ],
            'tactics': [
                "Anchor high but reasonably",
                "Bundle multiple requests together",
                "Focus on total compensation, not just base salary",
                "Be prepared to justify your requests",
                "Have backup options if they can't meet salary demands"
            ]
        }
    
    def calculate_salary_range(self, role, level, location, years_experience=None):
        """Calculate expected salary range based on role, level, and location"""
        try:
            # Normalize inputs
            role = role.lower().replace(' ', '_')
            level = level.lower()
            location = location.lower().replace(' ', '_').replace(',_', '_')
            
            # Get base salary data
            if role not in self.salary_data:
                role = 'software_engineer'  # Default fallback
            
            role_data = self.salary_data[role]
            
            if level not in role_data:
                level = 'mid'  # Default fallback
            
            level_data = role_data[level]
            
            # Get location-specific data or default
            salary_range = level_data.get(location, level_data.get('default', level_data['junior']))
            
            # Adjust for years of experience
            if years_experience:
                experience_multiplier = self._calculate_experience_multiplier(years_experience, level)
                salary_range = {
                    'min': int(salary_range['min'] * experience_multiplier),
                    'max': int(salary_range['max'] * experience_multiplier)
                }
            
            # Calculate percentiles
            base_min = salary_range['min']
            base_max = salary_range['max']
            median = int((base_min + base_max) / 2)
            
            return {
                'role': role.replace('_', ' ').title(),
                'level': level.title(),
                'location': location.replace('_', ' ').title(),
                'currency': self._get_currency(location),
                'salary_range': {
                    'min': base_min,
                    'median': median,
                    'max': base_max,
                    'p25': int(base_min + (median - base_min) * 0.5),
                    'p75': int(median + (base_max - median) * 0.5)
                },
                'market_insights': self._get_market_insights(role, level, location),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error calculating salary range: {e}")
            return {
                'error': 'Unable to calculate salary range',
                'message': str(e)
            }
    
    def _calculate_experience_multiplier(self, years_experience, level):
        """Calculate experience-based salary multiplier"""
        base_multipliers = {
            'junior': {'min_years': 0, 'max_years': 3, 'base': 1.0},
            'mid': {'min_years': 3, 'max_years': 7, 'base': 1.0},
            'senior': {'min_years': 7, 'max_years': 12, 'base': 1.0},
            'staff': {'min_years': 12, 'max_years': 20, 'base': 1.0}
        }
        
        level_info = base_multipliers.get(level, base_multipliers['mid'])
        
        if years_experience < level_info['min_years']:
            # Below expected level
            return max(0.85, 1.0 - (level_info['min_years'] - years_experience) * 0.05)
        elif years_experience > level_info['max_years']:
            # Above expected level
            return min(1.25, 1.0 + (years_experience - level_info['max_years']) * 0.03)
        else:
            # Within expected range
            return 1.0
    
    def _get_currency(self, location):
        """Get currency based on location"""
        if 'london' in location or 'uk' in location:
            return 'GBP'
        elif 'toronto' in location or 'canada' in location:
            return 'CAD'
        elif 'berlin' in location or 'germany' in location:
            return 'EUR'
        else:
            return 'USD'
    
    def _get_market_insights(self, role, level, location):
        """Get market insights for the role and location"""
        insights = []
        
        high_demand_locations = ['san_francisco', 'seattle', 'new_york']
        if location in high_demand_locations:
            insights.append("High-demand market with competitive salaries")
            insights.append("Strong negotiation position due to market competition")
        
        if role == 'software_engineer':
            insights.append("Tech industry continues to show strong salary growth")
            insights.append("Remote work options may affect compensation")
        elif role == 'data_scientist':
            insights.append("Growing demand for ML/AI expertise")
            insights.append("Consider specialization premiums")
        
        if level == 'senior' or level == 'staff':
            insights.append("Leadership and mentoring skills are highly valued")
            insights.append("Stock compensation becomes more significant")
        
        return insights
    
    def calculate_total_compensation(self, base_salary, equity_value=0, bonus=0, benefits_value=0):
        """Calculate total compensation package"""
        try:
            total_comp = base_salary + equity_value + bonus + benefits_value
            
            return {
                'base_salary': base_salary,
                'equity_value': equity_value,
                'bonus': bonus,
                'benefits_value': benefits_value,
                'total_compensation': total_comp,
                'breakdown': {
                    'base_salary_percent': round((base_salary / total_comp) * 100, 1),
                    'equity_percent': round((equity_value / total_comp) * 100, 1),
                    'bonus_percent': round((bonus / total_comp) * 100, 1),
                    'benefits_percent': round((benefits_value / total_comp) * 100, 1)
                },
                'recommendations': self._get_comp_recommendations(base_salary, equity_value, bonus)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _get_comp_recommendations(self, base_salary, equity_value, bonus):
        """Get compensation package recommendations"""
        recommendations = []
        
        total_cash = base_salary + bonus
        if equity_value > total_cash * 0.3:
            recommendations.append("High equity ratio - consider risk vs. stability")
        
        if bonus > base_salary * 0.2:
            recommendations.append("Significant bonus component - understand performance criteria")
        
        if equity_value == 0:
            recommendations.append("Consider negotiating for equity/stock options")
        
        recommendations.append("Don't forget to factor in benefits and perks value")
        
        return recommendations
    
    def get_negotiation_strategy(self, current_offer, target_salary, role, level):
        """Generate personalized negotiation strategy"""
        try:
            gap = target_salary - current_offer
            gap_percent = (gap / current_offer) * 100
            
            strategy = {
                'assessment': self._assess_negotiation_position(gap_percent),
                'talking_points': self._generate_talking_points(role, level, gap_percent),
                'tactics': self._recommend_tactics(gap_percent),
                'alternatives': self._suggest_alternatives(gap_percent),
                'timeline': self._create_negotiation_timeline(),
                'scripts': self._generate_negotiation_scripts(current_offer, target_salary)
            }
            
            return strategy
            
        except Exception as e:
            return {'error': str(e)}
    
    def _assess_negotiation_position(self, gap_percent):
        """Assess the strength of negotiation position"""
        if gap_percent <= 5:
            return {
                'strength': 'strong',
                'likelihood': 'high',
                'message': 'Small gap - very reasonable request'
            }
        elif gap_percent <= 15:
            return {
                'strength': 'moderate',
                'likelihood': 'moderate',
                'message': 'Moderate gap - requires good justification'
            }
        elif gap_percent <= 25:
            return {
                'strength': 'challenging',
                'likelihood': 'low-moderate',
                'message': 'Large gap - may need to compromise or focus on total comp'
            }
        else:
            return {
                'strength': 'difficult',
                'likelihood': 'low',
                'message': 'Very large gap - consider alternative benefits or timeline'
            }
    
    def _generate_talking_points(self, role, level, gap_percent):
        """Generate role-specific talking points"""
        points = []
        
        if role == 'software_engineer':
            points.extend([
                "Market research shows strong demand for my skillset",
                "I bring specific technical expertise in [mention technologies]",
                "My experience with [relevant projects] adds immediate value"
            ])
        elif role == 'product_manager':
            points.extend([
                "I have proven track record of successful product launches",
                "My cross-functional leadership experience is valuable",
                "I can drive user growth and engagement metrics"
            ])
        
        if level in ['senior', 'staff']:
            points.extend([
                "I bring mentoring and team leadership capabilities",
                "My strategic thinking will help drive company objectives",
                "I can contribute to technical/product architecture decisions"
            ])
        
        if gap_percent > 15:
            points.append("I'm excited about the role and want to find a mutually beneficial arrangement")
        
        return points
    
    def _recommend_tactics(self, gap_percent):
        """Recommend negotiation tactics based on gap"""
        if gap_percent <= 10:
            return [
                "Direct approach - simply state your salary expectation",
                "Emphasize your enthusiasm for the role",
                "Mention one or two key value propositions"
            ]
        elif gap_percent <= 20:
            return [
                "Present market research data",
                "Bundle with other benefits if salary is inflexible",
                "Suggest a performance review timeline for increases"
            ]
        else:
            return [
                "Focus on total compensation package",
                "Consider sign-on bonus to bridge gap",
                "Negotiate future salary review milestones",
                "Explore alternative benefits (equity, PTO, remote work)"
            ]
    
    def _suggest_alternatives(self, gap_percent):
        """Suggest alternative negotiation points"""
        alternatives = []
        
        if gap_percent > 10:
            alternatives.extend([
                "Sign-on bonus to bridge the gap",
                "Earlier salary review (6 months vs 12 months)",
                "Additional equity/stock options",
                "Flexible work arrangements",
                "Professional development budget",
                "Extra vacation days"
            ])
        
        alternatives.extend([
            "Better health/dental benefits",
            "Relocation assistance",
            "Home office setup allowance",
            "Conference/training budget"
        ])
        
        return alternatives[:6]  # Limit to top 6
    
    def _create_negotiation_timeline(self):
        """Create a negotiation timeline"""
        return {
            'day_1': "Receive and review offer thoroughly",
            'day_2-3': "Research market rates and prepare talking points",
            'day_4-5': "Schedule call with hiring manager/recruiter",
            'week_1_end': "Present your counteroffer professionally",
            'week_2': "Allow time for internal discussion",
            'week_2_end': "Follow up if no response received",
            'week_3': "Finalize negotiations and make decision"
        }
    
    def _generate_negotiation_scripts(self, current_offer, target_salary):
        """Generate sample negotiation scripts"""
        return {
            'opening': f"Thank you for the offer. I'm very excited about joining the team. Based on my research of market rates and the value I'll bring, I was hoping we could discuss the compensation.",
            'main_ask': f"Given my experience and the market rate for this role, I was hoping for a salary closer to ${target_salary:,}. Is there flexibility in the offer?",
            'alternative': f"If the base salary isn't flexible, I'd be interested in discussing other aspects of the compensation package, such as equity, signing bonus, or benefits.",
            'closing': "I'm really excited about the opportunity and hope we can find a package that works for both of us."
        }
    
    def get_benefits_calculator(self, base_salary):
        """Calculate the value of different benefits"""
        benefits_breakdown = {}
        
        for benefit, info in self.benefits_data.items():
            value = int(base_salary * (info['value_percent'] / 100))
            benefits_breakdown[benefit] = {
                'annual_value': value,
                'monthly_value': int(value / 12),
                'negotiable': info['negotiable'],
                'priority': info['priority'],
                'description': self._get_benefit_description(benefit)
            }
        
        total_benefits_value = sum(b['annual_value'] for b in benefits_breakdown.values())
        
        return {
            'base_salary': base_salary,
            'total_benefits_value': total_benefits_value,
            'total_compensation': base_salary + total_benefits_value,
            'benefits_breakdown': benefits_breakdown,
            'benefits_as_percent': round((total_benefits_value / base_salary) * 100, 1)
        }
    
    def _get_benefit_description(self, benefit):
        """Get description for each benefit type"""
        descriptions = {
            'health_insurance': 'Medical insurance coverage for you and family',
            'dental_vision': 'Dental and vision insurance coverage',
            'retirement_401k': '401(k) matching and retirement benefits',
            'stock_options': 'Equity compensation and stock options',
            'pto_vacation': 'Paid time off and vacation days',
            'remote_work': 'Flexible/remote work arrangements',
            'professional_development': 'Training, conferences, and skill development',
            'signing_bonus': 'One-time bonus upon joining'
        }
        return descriptions.get(benefit, 'Additional employment benefit')
    
    def generate_personalized_advice(self, profile):
        """Generate AI-powered personalized negotiation advice"""
        try:
            prompt = f"""
            Generate personalized salary negotiation advice for:
            - Role: {profile.get('role', 'Software Engineer')}
            - Level: {profile.get('level', 'Mid-level')}
            - Years Experience: {profile.get('experience', 5)}
            - Location: {profile.get('location', 'Tech Hub')}
            - Current Offer: ${profile.get('current_offer', 120000):,}
            - Target Salary: ${profile.get('target_salary', 140000):,}
            - Company Size: {profile.get('company_size', 'Medium')}
            - Industry: {profile.get('industry', 'Technology')}
            
            Provide specific, actionable advice including:
            1. Assessment of the request reasonableness
            2. Key talking points for this specific situation
            3. Potential objections and how to address them
            4. Alternative negotiation strategies
            5. Timeline recommendations
            
            Keep advice practical and professional.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.7
            )
            
            return {
                'advice': response.choices[0].message.content,
                'profile': profile,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"AI advice generation failed: {e}")
            return {
                'advice': "Unable to generate personalized advice at this time. Please use the general negotiation strategies and market data provided.",
                'error': str(e)
            }
    
    def get_negotiation_templates(self):
        """Get email templates for salary negotiation"""
        return {
            'initial_response': {
                'subject': 'Thank you for the offer - Questions about compensation',
                'body': """Dear [Hiring Manager/Recruiter],

Thank you for extending the offer for the [Position] role. I'm very excited about the opportunity to join [Company] and contribute to [specific project/team].

I've reviewed the offer details and would like to schedule a brief call to discuss the compensation package. Based on my research and experience, I believe there may be room for adjustment.

Would you be available for a 15-20 minute conversation this week to explore this further?

Best regards,
[Your name]"""
            },
            'counter_offer': {
                'subject': 'Following up on our compensation discussion',
                'body': """Dear [Hiring Manager/Recruiter],

Thank you for taking the time to discuss the offer with me yesterday. I remain very enthusiastic about joining [Company] and the [Position] role.

After our conversation and additional market research, I'd like to propose the following adjustments to the compensation package:

• Base Salary: $[amount] (current market rate for my experience level)
• [Additional requests like equity, bonus, benefits]

I believe this adjustment reflects the value I'll bring to the team, particularly my experience with [specific skills/achievements].

I'm confident we can find a mutually beneficial arrangement and look forward to hearing your thoughts.

Best regards,
[Your name]"""
            },
            'acceptance': {
                'subject': 'Accepting the offer - Next steps',
                'body': """Dear [Hiring Manager/Recruiter],

I'm delighted to formally accept the offer for the [Position] role with the terms we discussed:

• Base Salary: $[amount]
• Start Date: [date]
• [Other agreed terms]

Thank you for working with me on the compensation package. I'm excited to get started and contribute to [Company]'s success.

Please let me know the next steps for onboarding and documentation.

Best regards,
[Your name]"""
            }
        }
    
    def get_company_research_tips(self):
        """Get tips for researching company compensation"""
        return {
            'salary_research_sources': [
                'Glassdoor company reviews and salary data',
                'Levels.fyi for tech companies',
                'LinkedIn salary insights',
                'Blind app for anonymous employee discussions',
                'H1B visa database for tech salaries',
                'Company investor relations and earnings reports'
            ],
            'company_analysis': [
                'Recent funding rounds or financial performance',
                'Company growth stage and hiring volume',
                'Competitive landscape and market position',
                'Employee retention and satisfaction ratings',
                'Compensation philosophy and equity programs',
                'Geographic pay differences and remote work policies'
            ],
            'negotiation_timing': [
                'Best time is after receiving written offer',
                'Avoid negotiating during initial screening',
                'Friday afternoons can be good for initial discussions',
                'Allow 1-2 weeks for back-and-forth negotiation',
                'Be mindful of company budget cycles and fiscal years'
            ]
        }