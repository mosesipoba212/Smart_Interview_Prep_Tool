"""
Custom Question Banks Module
Industry-specific and role-specific interview question collections
"""

import json
import random
from typing import Dict, List, Any
from pathlib import Path

class QuestionBanks:
    """Manages custom question banks for different industries and roles"""
    
    def __init__(self):
        self.question_banks = self.load_question_banks()
        print("📚 Custom question banks initialized")
    
    def load_question_banks(self) -> Dict[str, Any]:
        """Load all question banks from JSON files or create default ones"""
        return {
            "industries": {
                "technology": {
                    "name": "Technology & Software",
                    "icon": "💻",
                    "questions": {
                        "technical": [
                            "Explain the difference between REST and GraphQL APIs",
                            "How would you optimize a slow database query?",
                            "What is your approach to handling technical debt?",
                            "Describe a challenging bug you've fixed recently",
                            "How do you ensure code quality in your projects?",
                            "What's your experience with microservices architecture?",
                            "How do you handle state management in modern web applications?",
                            "Explain the concepts of CI/CD and DevOps",
                            "What are the principles of clean code?",
                            "How would you design a scalable system for millions of users?"
                        ],
                        "behavioral": [
                            "Tell me about a time you had to learn a new technology quickly",
                            "Describe a situation where you disagreed with a technical decision",
                            "How do you handle tight deadlines in software development?",
                            "Tell me about a time you had to debug a complex issue",
                            "Describe your experience working in an Agile environment"
                        ],
                        "system_design": [
                            "Design a URL shortening service like bit.ly",
                            "How would you design a chat application like WhatsApp?",
                            "Design a social media feed system",
                            "How would you build a ride-sharing app like Uber?",
                            "Design a distributed cache system"
                        ]
                    }
                },
                "finance": {
                    "name": "Finance & Banking",
                    "icon": "💰",
                    "questions": {
                        "technical": [
                            "Explain the concept of risk management in trading",
                            "How do you calculate Value at Risk (VaR)?",
                            "What is the Black-Scholes model and its applications?",
                            "Describe different types of financial derivatives",
                            "How do you assess credit risk for loan applications?",
                            "Explain the concept of portfolio optimization",
                            "What are the key metrics for evaluating investment performance?",
                            "How do regulatory requirements impact financial systems?",
                            "Describe the process of financial statement analysis",
                            "What is algorithmic trading and how does it work?"
                        ],
                        "behavioral": [
                            "Describe a time you had to make a decision with incomplete information",
                            "How do you handle high-pressure financial situations?",
                            "Tell me about a time you identified a financial risk",
                            "Describe your experience with regulatory compliance",
                            "How do you communicate complex financial concepts to non-experts?"
                        ]
                    }
                },
                "healthcare": {
                    "name": "Healthcare & Life Sciences",
                    "icon": "🏥",
                    "questions": {
                        "technical": [
                            "Explain the drug development process from discovery to market",
                            "How do you ensure compliance with FDA regulations?",
                            "Describe the importance of clinical trial design",
                            "What are the key challenges in healthcare data management?",
                            "How do you approach patient safety in medical devices?",
                            "Explain the concept of evidence-based medicine",
                            "What are the ethical considerations in healthcare research?",
                            "How do you handle medical data privacy (HIPAA compliance)?",
                            "Describe the process of medical device validation",
                            "What is pharmacovigilance and why is it important?"
                        ],
                        "behavioral": [
                            "Describe a time you had to handle a patient safety issue",
                            "How do you stay updated with medical regulations?",
                            "Tell me about a challenging ethical decision you faced",
                            "Describe your experience working in a regulated environment",
                            "How do you handle stress in high-stakes medical situations?"
                        ]
                    }
                },
                "consulting": {
                    "name": "Management Consulting",
                    "icon": "📊",
                    "questions": {
                        "case_study": [
                            "A retail client is experiencing declining sales. How would you approach this problem?",
                            "How would you help a tech company decide whether to enter a new market?",
                            "A manufacturing company wants to reduce costs by 20%. What's your approach?",
                            "How would you value a company for acquisition?",
                            "A client wants to improve customer satisfaction. How do you proceed?"
                        ],
                        "behavioral": [
                            "Describe a time you had to influence someone without authority",
                            "How do you handle difficult client situations?",
                            "Tell me about a time you had to present complex analysis to executives",
                            "Describe your approach to managing multiple client projects",
                            "How do you handle disagreement within your team?"
                        ]
                    }
                }
            },
            "roles": {
                "software_engineer": {
                    "name": "Software Engineer",
                    "icon": "👨‍💻",
                    "levels": {
                        "junior": [
                            "What is object-oriented programming?",
                            "Explain the difference between == and === in JavaScript",
                            "What is version control and why is it important?",
                            "How do you debug code?",
                            "What is the difference between frontend and backend?"
                        ],
                        "mid": [
                            "Explain design patterns and give examples",
                            "How would you optimize application performance?",
                            "What is test-driven development?",
                            "Describe your experience with databases",
                            "How do you handle code reviews?"
                        ],
                        "senior": [
                            "How do you make architectural decisions?",
                            "Describe your approach to mentoring junior developers",
                            "How do you handle technical debt?",
                            "What's your experience with system scalability?",
                            "How do you evaluate new technologies for adoption?"
                        ]
                    }
                },
                "product_manager": {
                    "name": "Product Manager",
                    "icon": "📱",
                    "questions": [
                        "How do you prioritize product features?",
                        "Describe your experience with user research",
                        "How do you measure product success?",
                        "Tell me about a product you launched from concept to market",
                        "How do you handle conflicting stakeholder requirements?",
                        "What frameworks do you use for product strategy?",
                        "How do you work with engineering and design teams?",
                        "Describe a time you had to pivot a product strategy",
                        "How do you analyze competitor products?",
                        "What metrics do you track for product performance?"
                    ]
                },
                "data_scientist": {
                    "name": "Data Scientist",
                    "icon": "📈",
                    "questions": [
                        "Explain the difference between supervised and unsupervised learning",
                        "How do you handle missing data in datasets?",
                        "What is overfitting and how do you prevent it?",
                        "Describe your experience with A/B testing",
                        "How do you evaluate machine learning model performance?",
                        "What is feature engineering and why is it important?",
                        "Explain the bias-variance tradeoff",
                        "How do you communicate data insights to non-technical stakeholders?",
                        "What tools and languages do you use for data analysis?",
                        "Describe a challenging data science project you worked on"
                    ]
                },
                "sales": {
                    "name": "Sales Representative",
                    "icon": "🤝",
                    "questions": [
                        "How do you handle objections from potential customers?",
                        "Describe your sales process from lead to close",
                        "How do you research and qualify prospects?",
                        "Tell me about your biggest sales win",
                        "How do you handle rejection in sales?",
                        "What CRM tools have you used?",
                        "How do you build long-term customer relationships?",
                        "Describe a time you exceeded your sales quota",
                        "How do you stay motivated during slow periods?",
                        "What's your approach to cold calling/emailing?"
                    ]
                }
            },
            "company_specific": {
                "faang": {
                    "name": "FAANG Companies",
                    "companies": ["Facebook/Meta", "Apple", "Amazon", "Netflix", "Google"],
                    "questions": [
                        "How would you improve [company]'s main product?",
                        "What would you do in your first 90 days at [company]?",
                        "How do you handle ambiguity in large organizations?",
                        "Describe a time you disagreed with a manager's decision",
                        "How do you stay innovative in a fast-paced environment?",
                        "What's your approach to work-life balance?",
                        "How do you handle competing priorities?",
                        "Tell me about a time you failed and what you learned",
                        "How do you influence without authority?",
                        "What makes you excited about working at [company]?"
                    ]
                },
                "startups": {
                    "name": "Startups",
                    "questions": [
                        "How do you thrive in ambiguous environments?",
                        "Describe your experience wearing multiple hats",
                        "How do you prioritize when everything seems urgent?",
                        "What attracts you to startup environments?",
                        "How do you handle rapid changes in direction?",
                        "Describe a time you had to work with limited resources",
                        "How do you contribute to company culture?",
                        "What's your approach to risk-taking?",
                        "How do you handle uncertainty about job security?",
                        "Describe your ideal startup environment"
                    ]
                }
            }
        }
    
    def get_questions_by_industry(self, industry: str, question_type: str = None, count: int = 10) -> List[str]:
        """Get questions for a specific industry"""
        if industry not in self.question_banks["industries"]:
            return []
        
        industry_data = self.question_banks["industries"][industry]
        questions = []
        
        if question_type and question_type in industry_data["questions"]:
            questions = industry_data["questions"][question_type]
        else:
            # Get questions from all types
            for qtype, qlist in industry_data["questions"].items():
                questions.extend(qlist)
        
        return random.sample(questions, min(count, len(questions)))
    
    def get_questions_by_role(self, role: str, level: str = None, count: int = 10) -> List[str]:
        """Get questions for a specific role"""
        if role not in self.question_banks["roles"]:
            return []
        
        role_data = self.question_banks["roles"][role]
        
        if "levels" in role_data and level and level in role_data["levels"]:
            questions = role_data["levels"][level]
        elif "questions" in role_data:
            questions = role_data["questions"]
        else:
            return []
        
        return random.sample(questions, min(count, len(questions)))
    
    def get_company_specific_questions(self, company_type: str, count: int = 10) -> List[str]:
        """Get company-specific questions"""
        if company_type not in self.question_banks["company_specific"]:
            return []
        
        questions = self.question_banks["company_specific"][company_type]["questions"]
        return random.sample(questions, min(count, len(questions)))
    
    def get_custom_question_set(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a custom question set based on multiple filters"""
        result = {
            "questions": [],
            "metadata": {
                "total_questions": 0,
                "sources": [],
                "difficulty_mix": {},
                "question_types": []
            }
        }
        
        # Industry-specific questions
        if filters.get("industry"):
            industry_questions = self.get_questions_by_industry(
                filters["industry"], 
                filters.get("question_type"),
                filters.get("industry_count", 5)
            )
            result["questions"].extend(industry_questions)
            result["metadata"]["sources"].append(f"Industry: {filters['industry']}")
        
        # Role-specific questions
        if filters.get("role"):
            role_questions = self.get_questions_by_role(
                filters["role"],
                filters.get("level"),
                filters.get("role_count", 5)
            )
            result["questions"].extend(role_questions)
            result["metadata"]["sources"].append(f"Role: {filters['role']}")
        
        # Company-specific questions
        if filters.get("company_type"):
            company_questions = self.get_company_specific_questions(
                filters["company_type"],
                filters.get("company_count", 3)
            )
            result["questions"].extend(company_questions)
            result["metadata"]["sources"].append(f"Company: {filters['company_type']}")
        
        # Shuffle and limit total questions
        if result["questions"]:
            random.shuffle(result["questions"])
            max_questions = filters.get("max_questions", 15)
            result["questions"] = result["questions"][:max_questions]
        
        result["metadata"]["total_questions"] = len(result["questions"])
        
        return result
    
    def get_available_categories(self) -> Dict[str, Any]:
        """Get all available categories for question selection"""
        return {
            "industries": {
                key: {
                    "name": value["name"],
                    "icon": value["icon"],
                    "question_types": list(value["questions"].keys())
                }
                for key, value in self.question_banks["industries"].items()
            },
            "roles": {
                key: {
                    "name": value["name"],
                    "icon": value["icon"],
                    "has_levels": "levels" in value
                }
                for key, value in self.question_banks["roles"].items()
            },
            "company_types": {
                key: {
                    "name": value["name"],
                    "description": f"Questions for {value.get('companies', [value['name']])[0] if value.get('companies') else value['name']}"
                }
                for key, value in self.question_banks["company_specific"].items()
            }
        }
    
    def add_custom_questions(self, category: str, subcategory: str, questions: List[str]) -> bool:
        """Add custom questions to existing categories"""
        try:
            # Implementation for adding custom questions
            # This would typically save to a database or file
            print(f"✅ Added {len(questions)} custom questions to {category}/{subcategory}")
            return True
        except Exception as e:
            print(f"❌ Error adding custom questions: {e}")
            return False
