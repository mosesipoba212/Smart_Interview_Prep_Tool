"""
Company-Specific Interview Guides
Provides detailed interview preparation guides for major tech companies
"""

from typing import Dict, List, Any

class CompanyGuides:
    """Manages company-specific interview preparation guides"""
    
    def __init__(self):
        self.company_data = self.load_company_data()
        print("🏢 Company guides initialized")
    
    def load_company_data(self) -> Dict[str, Dict[str, Any]]:
        """Load comprehensive company interview data"""
        return {
            'google': {
                'name': 'Google',
                'logo': '🟡',
                'focus_areas': [
                    'Algorithm & Data Structures',
                    'System Design',
                    'Googleyness & Leadership',
                    'General Cognitive Ability'
                ],
                'interview_process': {
                    'phone_screen': {
                        'duration': '45-60 minutes',
                        'focus': 'Coding problems, basic algorithms',
                        'tips': [
                            'Practice coding in Google Docs',
                            'Focus on optimal solutions',
                            'Explain your thought process clearly',
                            'Ask clarifying questions'
                        ]
                    },
                    'onsite': {
                        'duration': '4-5 rounds, 45 min each',
                        'rounds': [
                            'Coding & Algorithms (2-3 rounds)',
                            'System Design (1 round)',
                            'Googleyness & Leadership (1 round)'
                        ],
                        'tips': [
                            'Whiteboard coding practice',
                            'Think out loud',
                            'Consider edge cases',
                            'Discuss trade-offs'
                        ]
                    }
                },
                'common_questions': [
                    'Given a binary tree, find the lowest common ancestor',
                    'Design a URL shortener like bit.ly',
                    'Tell me about a time you had to work with a difficult teammate',
                    'How would you explain machine learning to a 5-year-old?'
                ],
                'preparation_tips': [
                    'Study "Cracking the Coding Interview"',
                    'Practice on LeetCode (Medium/Hard)',
                    'Read about Google\'s culture and values',
                    'Prepare STAR method examples',
                    'Study distributed systems concepts'
                ],
                'technical_focus': [
                    'Arrays and Strings',
                    'Trees and Graphs',
                    'Dynamic Programming',
                    'System Design',
                    'Scalability'
                ],
                'culture_values': [
                    'Focus on the user',
                    'Think big',
                    'Be data-driven',
                    'Collaboration',
                    'Innovation'
                ]
            },
            'microsoft': {
                'name': 'Microsoft',
                'logo': '🟦',
                'focus_areas': [
                    'Technical Skills',
                    'Problem Solving',
                    'Design & Architecture',
                    'Culture Fit'
                ],
                'interview_process': {
                    'phone_screen': {
                        'duration': '60 minutes',
                        'focus': 'Coding, basic system design',
                        'tips': [
                            'Use Visual Studio Online or similar',
                            'Focus on clean, readable code',
                            'Discuss optimization',
                            'Be collaborative'
                        ]
                    },
                    'onsite': {
                        'duration': '4-6 rounds, 60 min each',
                        'rounds': [
                            'Coding (2-3 rounds)',
                            'System Design (1 round)',
                            'Behavioral (1-2 rounds)'
                        ],
                        'tips': [
                            'Focus on collaboration',
                            'Discuss real-world applications',
                            'Show leadership examples',
                            'Demonstrate growth mindset'
                        ]
                    }
                },
                'common_questions': [
                    'Implement a LRU cache',
                    'Design a chat application',
                    'Describe a challenging project you led',
                    'How do you stay updated with technology?'
                ],
                'preparation_tips': [
                    'Study Microsoft technologies (.NET, Azure)',
                    'Practice system design for cloud',
                    'Prepare leadership examples',
                    'Study Microsoft\'s mission and values',
                    'Focus on collaboration skills'
                ],
                'technical_focus': [
                    'Object-Oriented Design',
                    'Cloud Architecture',
                    'Databases',
                    'API Design',
                    '.NET Ecosystem'
                ],
                'culture_values': [
                    'Respect',
                    'Integrity',
                    'Accountability',
                    'Growth mindset',
                    'Diversity & Inclusion'
                ]
            },
            'amazon': {
                'name': 'Amazon',
                'logo': '🟠',
                'focus_areas': [
                    'Leadership Principles',
                    'Technical Excellence',
                    'Customer Obsession',
                    'Ownership'
                ],
                'interview_process': {
                    'phone_screen': {
                        'duration': '45 minutes',
                        'focus': 'Coding + behavioral',
                        'tips': [
                            'Use Amazon Chime or similar',
                            'Have STAR examples ready',
                            'Focus on customer impact',
                            'Show ownership mentality'
                        ]
                    },
                    'onsite': {
                        'duration': '5-6 rounds, 60 min each',
                        'rounds': [
                            'Coding (2 rounds)',
                            'System Design (1 round)',
                            'Leadership Principles (2-3 rounds)'
                        ],
                        'tips': [
                            'Use STAR method consistently',
                            'Focus on leadership principles',
                            'Show bias for action',
                            'Demonstrate customer obsession'
                        ]
                    }
                },
                'common_questions': [
                    'Design Amazon\'s recommendation system',
                    'Tell me about a time you had to make a difficult decision',
                    'How would you handle a disagreement with your manager?',
                    'Describe a time you failed and what you learned'
                ],
                'preparation_tips': [
                    'Study all 16 Leadership Principles',
                    'Prepare 2-3 STAR examples per principle',
                    'Practice AWS architecture',
                    'Read "Working Backwards"',
                    'Focus on scale and efficiency'
                ],
                'technical_focus': [
                    'Distributed Systems',
                    'AWS Services',
                    'Scalability',
                    'Performance Optimization',
                    'Data Structures'
                ],
                'culture_values': [
                    'Customer Obsession',
                    'Ownership',
                    'Invent and Simplify',
                    'Bias for Action',
                    'Deliver Results'
                ]
            },
            'apple': {
                'name': 'Apple',
                'logo': '🍎',
                'focus_areas': [
                    'Technical Depth',
                    'Innovation',
                    'Design Thinking',
                    'Attention to Detail'
                ],
                'interview_process': {
                    'phone_screen': {
                        'duration': '30-45 minutes',
                        'focus': 'Technical skills, past experience',
                        'tips': [
                            'Show passion for Apple products',
                            'Demonstrate attention to detail',
                            'Focus on user experience',
                            'Discuss innovation examples'
                        ]
                    },
                    'onsite': {
                        'duration': '4-6 rounds, 45-60 min each',
                        'rounds': [
                            'Technical Deep Dive (2-3 rounds)',
                            'Design Review (1 round)',
                            'Behavioral (1-2 rounds)'
                        ],
                        'tips': [
                            'Show deep technical knowledge',
                            'Focus on quality over quantity',
                            'Demonstrate innovation',
                            'Show passion for products'
                        ]
                    }
                },
                'common_questions': [
                    'Design the iPhone camera app',
                    'How would you improve Siri?',
                    'Explain a complex technical concept simply',
                    'Describe your most innovative project'
                ],
                'preparation_tips': [
                    'Study Apple\'s design principles',
                    'Use Apple products extensively',
                    'Focus on iOS/macOS development',
                    'Prepare innovation examples',
                    'Study human interface guidelines'
                ],
                'technical_focus': [
                    'iOS/macOS Development',
                    'Swift/Objective-C',
                    'Hardware-Software Integration',
                    'Performance Optimization',
                    'User Experience'
                ],
                'culture_values': [
                    'Innovation',
                    'Quality',
                    'Simplicity',
                    'Privacy',
                    'Environmental Responsibility'
                ]
            },
            'meta': {
                'name': 'Meta (Facebook)',
                'logo': '🔵',
                'focus_areas': [
                    'Coding Excellence',
                    'System Design',
                    'Meta Values',
                    'Impact & Leadership'
                ],
                'interview_process': {
                    'phone_screen': {
                        'duration': '45 minutes',
                        'focus': 'Coding problems',
                        'tips': [
                            'Use CoderPad or similar',
                            'Think about scale from the start',
                            'Focus on clean code',
                            'Discuss social impact'
                        ]
                    },
                    'onsite': {
                        'duration': '4-5 rounds, 45 min each',
                        'rounds': [
                            'Coding (2 rounds)',
                            'System Design (1 round)',
                            'Behavioral (1-2 rounds)'
                        ],
                        'tips': [
                            'Show move fast mentality',
                            'Focus on connecting people',
                            'Demonstrate bold thinking',
                            'Show data-driven decisions'
                        ]
                    }
                },
                'common_questions': [
                    'Design Facebook\'s news feed',
                    'How would you detect fake accounts?',
                    'Tell me about a time you took a big risk',
                    'How do you prioritize features for billions of users?'
                ],
                'preparation_tips': [
                    'Study Meta\'s core values',
                    'Practice large-scale system design',
                    'Focus on social impact',
                    'Prepare examples of bold decisions',
                    'Study React and other Meta technologies'
                ],
                'technical_focus': [
                    'Large-Scale Systems',
                    'Machine Learning',
                    'Mobile Development',
                    'React/React Native',
                    'Data Infrastructure'
                ],
                'culture_values': [
                    'Move Fast',
                    'Be Bold',
                    'Focus on Impact',
                    'Be Open',
                    'Build Social Value'
                ]
            },
            'netflix': {
                'name': 'Netflix',
                'logo': '🔴',
                'focus_areas': [
                    'Technical Excellence',
                    'Innovation',
                    'Culture Fit',
                    'High Performance'
                ],
                'interview_process': {
                    'phone_screen': {
                        'duration': '60 minutes',
                        'focus': 'Technical skills + culture',
                        'tips': [
                            'Show high performance mindset',
                            'Demonstrate innovation',
                            'Focus on user experience',
                            'Show data-driven thinking'
                        ]
                    },
                    'onsite': {
                        'duration': '4-6 rounds, 60 min each',
                        'rounds': [
                            'Technical (2-3 rounds)',
                            'Architecture/Design (1 round)',
                            'Culture (1-2 rounds)'
                        ],
                        'tips': [
                            'Show freedom and responsibility',
                            'Demonstrate candor',
                            'Focus on context not control',
                            'Show high performance standards'
                        ]
                    }
                },
                'common_questions': [
                    'Design Netflix\'s recommendation algorithm',
                    'How would you scale video streaming globally?',
                    'Describe a time you gave difficult feedback',
                    'How do you ensure high performance in your team?'
                ],
                'preparation_tips': [
                    'Study Netflix culture deck',
                    'Focus on streaming technology',
                    'Prepare high performance examples',
                    'Study microservices architecture',
                    'Understand content delivery networks'
                ],
                'technical_focus': [
                    'Microservices',
                    'Cloud Computing (AWS)',
                    'Streaming Technology',
                    'Machine Learning',
                    'Data Analytics'
                ],
                'culture_values': [
                    'Freedom and Responsibility',
                    'High Performance',
                    'Candor',
                    'Context not Control',
                    'Innovation'
                ]
            }
        }
    
    def get_company_guide(self, company: str) -> Dict[str, Any]:
        """Get comprehensive guide for a specific company"""
        company_key = company.lower().replace(' ', '').replace('(', '').replace(')', '')
        return self.company_data.get(company_key, {})
    
    def get_all_companies(self) -> List[str]:
        """Get list of all available companies"""
        return [data['name'] for data in self.company_data.values()]
    
    def get_company_summary(self, company: str) -> Dict[str, Any]:
        """Get a summary of company interview info"""
        guide = self.get_company_guide(company)
        if not guide:
            return {}
        
        return {
            'name': guide.get('name'),
            'logo': guide.get('logo'),
            'focus_areas': guide.get('focus_areas', [])[:3],  # Top 3
            'key_tips': guide.get('preparation_tips', [])[:3],  # Top 3
            'process_duration': self._estimate_process_duration(guide)
        }
    
    def _estimate_process_duration(self, guide: Dict[str, Any]) -> str:
        """Estimate total interview process duration"""
        process = guide.get('interview_process', {})
        if 'onsite' in process:
            rounds = process['onsite'].get('rounds', [])
            return f"{len(rounds)} rounds + phone screen"
        return "Varies"
    
    def search_companies(self, query: str) -> List[Dict[str, Any]]:
        """Search companies by name or focus area"""
        results = []
        query_lower = query.lower()
        
        for company_data in self.company_data.values():
            # Check name match
            if query_lower in company_data['name'].lower():
                results.append(self.get_company_summary(company_data['name']))
                continue
            
            # Check focus areas
            for area in company_data.get('focus_areas', []):
                if query_lower in area.lower():
                    results.append(self.get_company_summary(company_data['name']))
                    break
        
        return results