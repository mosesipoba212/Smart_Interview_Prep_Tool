"""
AI-Powered Question Generator
Generates tailored interview questions based on interview type, company, and position
"""

import os
import json
import random
from typing import List, Dict, Any
from datetime import datetime
from .ai_service import ai_service

class QuestionGenerator:
    """AI-powered interview question generator"""
    
    def __init__(self):
        # Use the universal AI service
        self.ai_service = ai_service
        print(f"🤖 Question generator using: {self.ai_service.get_provider_info()['name']}")
        
        # Load question templates
        self.question_templates = self.load_question_templates()
    
    def load_question_templates(self) -> Dict[str, List[str]]:
        """Load predefined question templates for different interview types"""
        return {
            'technical': [
                "What's your experience with {technology}?",
                "How would you optimize {specific_scenario}?",
                "Explain the difference between {concept_a} and {concept_b}.",
                "Walk me through how you would design {system_type}.",
                "What are the time and space complexities of {algorithm}?",
                "How do you handle {technical_challenge} in production?",
                "Describe your debugging process for {bug_type}.",
                "What design patterns have you used in {context}?",
                "How would you implement {feature} scalably?",
                "What testing strategies do you use for {code_type}?"
            ],
            'behavioral': [
                "Tell me about a time when you faced a significant challenge at work.",
                "Describe a situation where you had to work with a difficult team member.",
                "How do you handle tight deadlines and pressure?",
                "Give me an example of when you had to learn something new quickly.",
                "Tell me about a project you're particularly proud of.",
                "Describe a time when you had to give difficult feedback.",
                "How do you prioritize tasks when everything seems urgent?",
                "Tell me about a mistake you made and how you handled it.",
                "Describe your leadership style with examples.",
                "How do you stay motivated during challenging projects?"
            ],
            'system_design': [
                "Design a {system_type} that can handle {scale} users.",
                "How would you architect {specific_system}?",
                "What are the trade-offs between {option_a} and {option_b}?",
                "How would you ensure {system_quality} in your design?",
                "Design the database schema for {application_type}.",
                "How would you handle {scalability_challenge}?",
                "What caching strategy would you use for {use_case}?",
                "Design an API for {service_type}.",
                "How would you monitor and debug {distributed_system}?",
                "What security considerations are important for {system}?"
            ],
            'product': [
                "How would you improve {product_name}?",
                "What metrics would you track for {feature}?",
                "How do you prioritize features in a roadmap?",
                "Describe your process for gathering user feedback.",
                "How would you launch {new_feature}?",
                "What's your approach to A/B testing?",
                "How do you work with engineering teams?",
                "Describe a product failure and what you learned.",
                "How do you define product success?",
                "What frameworks do you use for product decisions?"
            ],
            'leadership': [
                "How do you build and motivate high-performing teams?",
                "Describe your approach to setting team goals.",
                "How do you handle underperforming team members?",
                "What's your strategy for cross-functional collaboration?",
                "How do you manage up and influence stakeholders?",
                "Describe a time you had to make a difficult decision.",
                "How do you handle conflicts within your team?",
                "What's your approach to hiring and onboarding?",
                "How do you foster innovation in your organization?",
                "Describe your long-term vision and strategy."
            ],
            'data_science': [
                "How would you approach {data_problem}?",
                "What ML models would you use for {prediction_task}?",
                "How do you handle missing or dirty data?",
                "Explain your model validation process.",
                "How would you deploy {ml_model} to production?",
                "What metrics would you use to evaluate {model_type}?",
                "How do you prevent overfitting in {model}?",
                "Describe your feature engineering process.",
                "How would you explain {complex_model} to stakeholders?",
                "What's your approach to model monitoring?"
            ]
        }
    
    def generate_questions(self, interview_type: str, company: str = "", position: str = "", count: int = 10) -> List[Dict[str, Any]]:
        """Generate tailored interview questions"""
        # Try AI generation first, fall back to templates
        ai_questions = self.generate_ai_questions(interview_type, company, position, count)
        if ai_questions:
            return ai_questions
        else:
            print("🔄 Falling back to template questions")
            return self.generate_template_questions(interview_type, company, position, count)
    
    def generate_ai_questions(self, interview_type: str, company: str, position: str, count: int) -> List[Dict[str, Any]]:
        """Generate questions using AI with enhanced error handling"""
        try:
            prompt = self.create_ai_prompt(interview_type, company, position, count)
            
            # Use the universal AI service
            response_text = self.ai_service.generate_text(prompt, max_tokens=1500)
            
            if not response_text:
                print("⚠️ AI generation returned empty response")
                return []
            
            return self.parse_ai_response(response_text, interview_type)
            
        except Exception as e:
            error_message = str(e)
            
            # Handle specific AI service errors
            if "429" in error_message or "quota" in error_message.lower():
                print(f"⚠️ AI API quota exceeded - falling back to template questions")
                print("💡 Consider upgrading your AI plan or checking billing details")
            elif "401" in error_message or "authentication" in error_message.lower():
                print(f"⚠️ AI API authentication failed - check your API key")
            elif "network" in error_message.lower() or "connection" in error_message.lower():
                print(f"⚠️ Network error connecting to AI service - falling back to templates")
            else:
                print(f"❌ AI question generation failed: {e}")
            
            # Return empty list to trigger fallback in main generate_questions method
            return []
    
    def create_ai_prompt(self, interview_type: str, company: str, position: str, count: int) -> str:
        """Create AI prompt for question generation"""
        return f"""
        Generate {count} tailored interview questions for:
        - Interview Type: {interview_type}
        - Company: {company}
        - Position: {position}
        
        Please provide questions that are:
        1. Specific to the role and industry
        2. Progressive in difficulty
        3. Include both conceptual and practical aspects
        4. Relevant to current industry trends
        
        Format each question as:
        Question: [question text]
        Difficulty: [Easy/Medium/Hard]
        Category: [specific subcategory]
        Tips: [brief preparation tips]
        ---
        """
    
    def parse_ai_response(self, response_text: str, interview_type: str) -> List[Dict[str, Any]]:
        """Parse AI response into structured questions"""
        questions = []
        question_blocks = response_text.split('---')
        
        for block in question_blocks:
            if 'Question:' in block:
                lines = block.strip().split('\n')
                question_data = {
                    'type': interview_type,
                    'difficulty': 'Medium',
                    'category': interview_type.title(),
                    'tips': ''
                }
                
                for line in lines:
                    if line.startswith('Question:'):
                        question_data['question'] = line.replace('Question:', '').strip()
                    elif line.startswith('Difficulty:'):
                        question_data['difficulty'] = line.replace('Difficulty:', '').strip()
                    elif line.startswith('Category:'):
                        question_data['category'] = line.replace('Category:', '').strip()
                    elif line.startswith('Tips:'):
                        question_data['tips'] = line.replace('Tips:', '').strip()
                
                if 'question' in question_data:
                    questions.append(question_data)
        
        return questions
    
    def generate_template_questions(self, interview_type: str, company: str, position: str, count: int) -> List[Dict[str, Any]]:
        """Enhanced template question generation with comprehensive question bank"""
        
        # Comprehensive question database with multiple categories and difficulties
        enhanced_question_bank = {
            'technical': {
                'easy': [
                    "What is the difference between a list and a tuple in Python?",
                    "Explain what a variable is in programming.",
                    "What is the purpose of loops in programming?",
                    "What is the difference between == and === in JavaScript?",
                    "What is a function and why do we use functions?",
                    "Explain the basic concept of algorithms.",
                    "What is the difference between front-end and back-end development?",
                    "What is debugging and how do you approach it?"
                ],
                'medium': [
                    "Explain the concept of object-oriented programming and its principles.",
                    "What are the benefits of using version control systems like Git?",
                    "Describe the difference between SQL and NoSQL databases.",
                    "What is the time complexity of common sorting algorithms?",
                    "Explain the concept of REST APIs and HTTP methods.",
                    "What is the difference between authentication and authorization?",
                    "Describe the MVC (Model-View-Controller) architecture pattern.",
                    "Explain the concepts of inheritance and polymorphism.",
                    "What are design patterns and give examples of commonly used ones?",
                    "How do you ensure code quality and maintainability?"
                ],
                'hard': [
                    "Design a system to handle millions of concurrent users.",
                    "Explain different caching strategies and their trade-offs.",
                    "How would you optimize a slow database query?",
                    "Describe microservices architecture and its challenges.",
                    "What are the principles of distributed system design?",
                    "How would you implement a load balancer from scratch?",
                    "Explain the CAP theorem and its implications for distributed systems.",
                    "Design a real-time chat application architecture.",
                    "How would you design a URL shortening service like bit.ly?",
                    "Explain eventual consistency in distributed systems."
                ]
            },
            'behavioral': {
                'easy': [
                    "Tell me about yourself and your background.",
                    "Why are you interested in this position?",
                    "What are your greatest strengths?",
                    "Describe a typical day in your current role.",
                    "What motivates you at work?",
                    "What do you know about our company?",
                    "Where do you see yourself in 5 years?",
                    "Why are you looking to leave your current position?"
                ],
                'medium': [
                    "Describe a challenging project you worked on.",
                    "Tell me about a time you had to learn something quickly.",
                    "How do you handle working under pressure?",
                    "Describe a time you had to work with a difficult team member.",
                    "What is your approach to problem-solving?",
                    "Tell me about a time you exceeded expectations.",
                    "Describe a situation where you had to adapt to change.",
                    "How do you handle feedback and criticism?",
                    "Tell me about a time you mentored someone.",
                    "Describe your ideal work environment."
                ],
                'hard': [
                    "Tell me about a time you failed and what you learned from it.",
                    "Describe a situation where you had to make a difficult decision.",
                    "How do you handle conflict in the workplace?",
                    "Tell me about a time you had to lead without authority.",
                    "Describe a situation where you disagreed with your manager.",
                    "How have you handled a major setback in your career?",
                    "Tell me about a time you had to influence someone without direct authority.",
                    "Describe the most difficult ethical decision you've faced at work.",
                    "How do you handle ambiguous requirements or unclear expectations?",
                    "Tell me about a time you had to deliver disappointing news to stakeholders."
                ]
            },
            'situational': {
                'easy': [
                    "How would you prioritize multiple deadlines?",
                    "What would you do if you noticed a mistake in your work?",
                    "How would you handle a customer complaint?",
                    "What steps would you take to learn a new technology?",
                    "How would you approach a project with unclear requirements?",
                    "What would you do if you were running late for an important meeting?",
                    "How would you handle working with someone who has a different communication style?",
                    "What would you do if you were assigned a task you've never done before?"
                ],
                'medium': [
                    "You discover your team is behind schedule. What do you do?",
                    "How would you handle a situation where a colleague takes credit for your work?",
                    "What would you do if you disagreed with a company policy?",
                    "How would you manage a project with limited resources?",
                    "What would you do if you were asked to work on something outside your expertise?",
                    "How would you handle a situation where stakeholders have conflicting requirements?",
                    "What would you do if you had to deliver bad news to a client?",
                    "How would you approach mentoring a new team member?",
                    "What would you do if you discovered a security vulnerability in production?",
                    "How would you handle a situation where your team resists adopting new processes?"
                ],
                'hard': [
                    "Your project is failing and the deadline is tomorrow. What do you do?",
                    "How would you handle laying off team members due to budget cuts?",
                    "What would you do if you discovered unethical behavior in your organization?",
                    "How would you manage a crisis that could damage the company's reputation?",
                    "What would you do if a key stakeholder constantly changes requirements?",
                    "How would you handle a situation where you need to fire a close friend?",
                    "What would you do if you were asked to compromise your values for company profit?",
                    "How would you manage a team revolt against a new company policy?",
                    "What would you do if you had to choose between technical debt and meeting deadlines?",
                    "How would you handle a data breach that affects customer privacy?"
                ]
            }
        }
        
        # Try to get questions from enhanced bank first, then fallback to original templates
        if interview_type in enhanced_question_bank:
            all_questions = []
            for difficulty, questions in enhanced_question_bank[interview_type].items():
                for q in questions:
                    all_questions.append({
                        'question': q,
                        'type': interview_type,
                        'difficulty': difficulty,
                        'category': interview_type.title(),
                        'tips': self.generate_tips(q, interview_type),
                        'estimated_time': self.estimate_time(interview_type)
                    })
            
            # Random selection from all difficulties
            selected_questions = random.sample(all_questions, min(count, len(all_questions)))
            return selected_questions
        
        # Fallback to original template system
        templates = self.question_templates.get(interview_type, self.question_templates['behavioral'])
        selected_templates = random.sample(templates, min(count, len(templates)))
        
        questions = []
        for i, template in enumerate(selected_templates):
            question = self.customize_template(template, company, position, interview_type)
            
            questions.append({
                'question': question,
                'type': interview_type,
                'difficulty': self.assign_difficulty(i, count),
                'category': interview_type.title(),
                'tips': self.generate_tips(question, interview_type),
                'estimated_time': self.estimate_time(interview_type)
            })
        
        return questions
    
    def customize_template(self, template: str, company: str, position: str, interview_type: str) -> str:
        """Customize question template with context"""
        # Technology mapping based on position
        tech_mapping = {
            'software engineer': ['Python', 'JavaScript', 'REST APIs'],
            'data scientist': ['machine learning', 'Python', 'SQL'],
            'frontend developer': ['React', 'JavaScript', 'CSS'],
            'backend developer': ['databases', 'APIs', 'microservices'],
            'devops engineer': ['containers', 'CI/CD', 'cloud services'],
            'product manager': ['user research', 'roadmaps', 'metrics']
        }
        
        # Get relevant technologies
        position_lower = position.lower()
        technologies = []
        for key, techs in tech_mapping.items():
            if key in position_lower:
                technologies = techs
                break
        
        if not technologies:
            technologies = ['your domain', 'relevant technologies', 'your expertise']
        
        # Replace placeholders
        replacements = {
            '{technology}': random.choice(technologies),
            '{specific_scenario}': f"a {position_lower} workflow",
            '{concept_a}': 'async',
            '{concept_b}': 'sync',
            '{system_type}': 'web application',
            '{algorithm}': 'sorting algorithm',
            '{technical_challenge}': 'performance issues',
            '{bug_type}': 'production bugs',
            '{context}': f'{position_lower} projects',
            '{feature}': 'new feature',
            '{code_type}': 'backend services',
            '{system}': f'{company} systems',
            '{scale}': '1 million',
            '{specific_system}': f'{company} platform',
            '{option_a}': 'SQL',
            '{option_b}': 'NoSQL',
            '{system_quality}': 'high availability',
            '{application_type}': f'{position_lower} application',
            '{scalability_challenge}': 'high traffic loads',
            '{use_case}': f'{company} use case',
            '{service_type}': f'{company} service',
            '{distributed_system}': 'microservices',
            '{product_name}': f'{company} product',
            '{feature}': 'core feature',
            '{new_feature}': 'product enhancement',
            '{data_problem}': 'customer segmentation',
            '{prediction_task}': 'churn prediction',
            '{ml_model}': 'recommendation system',
            '{model_type}': 'classification model',
            '{model}': 'neural network',
            '{complex_model}': 'ensemble model'
        }
        
        customized = template
        for placeholder, replacement in replacements.items():
            customized = customized.replace(placeholder, replacement)
        
        return customized
    
    def assign_difficulty(self, index: int, total: int) -> str:
        """Assign difficulty based on question position"""
        if index < total * 0.3:
            return 'Easy'
        elif index < total * 0.7:
            return 'Medium'
        else:
            return 'Hard'
    
    def generate_tips(self, question: str, interview_type: str) -> str:
        """Generate preparation tips for a question"""
        tip_templates = {
            'technical': [
                "Review the fundamentals and be ready to explain your thinking process.",
                "Practice coding this on a whiteboard or in your preferred language.",
                "Think about edge cases and time/space complexity.",
                "Be prepared to discuss trade-offs and alternative approaches."
            ],
            'behavioral': [
                "Use the STAR method (Situation, Task, Action, Result).",
                "Prepare specific examples from your experience.",
                "Focus on your contributions and what you learned.",
                "Be honest and show self-awareness."
            ],
            'system_design': [
                "Start with requirements gathering and constraints.",
                "Think about scalability from the beginning.",
                "Consider both high-level architecture and detailed components.",
                "Discuss monitoring, security, and failure scenarios."
            ]
        }
        
        tips = tip_templates.get(interview_type, tip_templates['behavioral'])
        return random.choice(tips)
    
    def estimate_time(self, interview_type: str) -> int:
        """Estimate time needed to answer question (in minutes)"""
        time_mapping = {
            'technical': 15,
            'behavioral': 5,
            'system_design': 20,
            'product': 10,
            'leadership': 8,
            'data_science': 12
        }
        return time_mapping.get(interview_type, 10)
    
    def generate_follow_up_questions(self, original_question: str, interview_type: str) -> List[str]:
        """Generate follow-up questions based on the original question"""
        follow_ups = {
            'technical': [
                "How would you test this solution?",
                "What if the requirements changed to handle 10x more data?",
                "What are potential bottlenecks in this approach?",
                "How would you monitor this in production?"
            ],
            'behavioral': [
                "What would you do differently next time?",
                "How did this experience change your approach?",
                "What was the most challenging part?",
                "How did you measure success?"
            ],
            'system_design': [
                "How would you handle failures in this system?",
                "What metrics would you monitor?",
                "How would you scale this globally?",
                "What security considerations are important?"
            ]
        }
        
        return follow_ups.get(interview_type, follow_ups['behavioral'])
    
    def get_question_analytics(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate analytics for the question set"""
        if not questions:
            return {}
        
        total_time = sum(q.get('estimated_time', 10) for q in questions)
        difficulty_counts = {}
        category_counts = {}
        
        for question in questions:
            difficulty = question.get('difficulty', 'Medium')
            category = question.get('category', 'General')
            
            difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
            category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            'total_questions': len(questions),
            'estimated_total_time': total_time,
            'difficulty_distribution': difficulty_counts,
            'category_distribution': category_counts,
            'average_time_per_question': total_time / len(questions)
        }
