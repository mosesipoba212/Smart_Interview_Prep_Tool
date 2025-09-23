import random
import json
from datetime import datetime
import os
from ..ai_engine.ai_service import ai_service

class MockInterviewSimulator:
    def __init__(self):
        # Use the universal AI service
        self.ai_service = ai_service
        print(f"🎤 Mock interview using: {self.ai_service.get_provider_info()['name']}")
        
        # Interview types and their characteristics
        self.interview_types = {
            'technical': {
                'name': 'Technical Interview',
                'description': 'Algorithm, data structure, and coding problems',
                'duration': 45,
                'difficulty_levels': ['Easy', 'Medium', 'Hard'],
                'topics': ['Arrays', 'Strings', 'Linked Lists', 'Trees', 'Graphs', 'Dynamic Programming', 'Sorting', 'Searching', 'Hash Tables', 'Recursion']
            },
            'behavioral': {
                'name': 'Behavioral Interview',
                'description': 'Situational and experience-based questions',
                'duration': 30,
                'difficulty_levels': ['Basic', 'Intermediate', 'Advanced'],
                'topics': ['Leadership', 'Teamwork', 'Problem Solving', 'Communication', 'Conflict Resolution', 'Decision Making', 'Adaptability', 'Time Management']
            },
            'system_design': {
                'name': 'System Design Interview',
                'description': 'Architecture and scalability discussions',
                'duration': 60,
                'difficulty_levels': ['Junior', 'Mid-level', 'Senior'],
                'topics': ['Scalability', 'Load Balancing', 'Databases', 'Caching', 'Microservices', 'APIs', 'Data Storage', 'Performance']
            },
            'product': {
                'name': 'Product Interview',
                'description': 'Product strategy and user experience',
                'duration': 45,
                'difficulty_levels': ['Associate', 'Manager', 'Senior'],
                'topics': ['Product Strategy', 'User Research', 'Market Analysis', 'Feature Prioritization', 'Metrics', 'A/B Testing', 'User Experience', 'Roadmapping']
            }
        }
        
        # Sample questions by type and difficulty
        self.question_bank = {
            'technical': {
                'Easy': [
                    "Implement a function to reverse a string",
                    "Find the maximum element in an array",
                    "Check if a string is a palindrome",
                    "Implement binary search",
                    "Find the first duplicate in an array"
                ],
                'Medium': [
                    "Design a data structure for LRU cache",
                    "Find the longest palindromic substring",
                    "Implement a binary tree traversal",
                    "Merge two sorted linked lists",
                    "Find all anagrams in a string array"
                ],
                'Hard': [
                    "Design a distributed cache system",
                    "Implement a thread-safe singleton pattern",
                    "Find the median of two sorted arrays",
                    "Design a rate limiter",
                    "Implement a graph algorithm for shortest path"
                ]
            },
            'behavioral': {
                'Basic': [
                    "Tell me about yourself",
                    "Why are you interested in this role?",
                    "What are your strengths and weaknesses?",
                    "Describe a challenging project you worked on",
                    "How do you handle stress and pressure?"
                ],
                'Intermediate': [
                    "Describe a time when you had to work with a difficult team member",
                    "Tell me about a project that didn't go as planned",
                    "How do you prioritize tasks when everything is urgent?",
                    "Describe a time when you had to learn something new quickly",
                    "Tell me about a time you disagreed with your manager"
                ],
                'Advanced': [
                    "Describe a time when you led a team through a major change",
                    "Tell me about a strategic decision you made that had significant impact",
                    "How would you handle competing priorities from different stakeholders?",
                    "Describe a time when you had to influence someone without authority",
                    "Tell me about a time you had to make a decision with incomplete information"
                ]
            },
            'system_design': {
                'Junior': [
                    "Design a simple URL shortener like bit.ly",
                    "How would you design a basic chat application?",
                    "Design a simple file storage system",
                    "How would you build a notification system?",
                    "Design a basic social media feed"
                ],
                'Mid-level': [
                    "Design a distributed cache system like Redis",
                    "How would you scale a web application to handle millions of users?",
                    "Design a ride-sharing service like Uber",
                    "How would you build a real-time messaging system?",
                    "Design a content delivery network (CDN)"
                ],
                'Senior': [
                    "Design a global search engine like Google",
                    "How would you architect a system like Netflix?",
                    "Design a distributed database system",
                    "How would you build a payment processing system?",
                    "Design a system for real-time analytics at scale"
                ]
            },
            'product': {
                'Associate': [
                    "How would you improve our mobile app?",
                    "What features would you prioritize for a new user onboarding?",
                    "How do you decide what metrics to track?",
                    "Walk me through how you would research a new market",
                    "How would you approach a feature that's underperforming?"
                ],
                'Manager': [
                    "How would you set the product roadmap for the next quarter?",
                    "Describe how you would launch a feature in a competitive market",
                    "How do you balance user needs with business requirements?",
                    "Walk me through your process for conducting user research",
                    "How would you handle conflicting feedback from stakeholders?"
                ],
                'Senior': [
                    "How would you enter a new market with an existing product?",
                    "Describe your approach to product-market fit validation",
                    "How do you build and manage cross-functional teams?",
                    "Walk me through a strategic product decision you've made",
                    "How would you handle a major pivot in product strategy?"
                ]
            }
        }
    
    def get_interview_types(self):
        """Get all available interview types"""
        return self.interview_types
    
    def start_interview(self, interview_type, difficulty, company=None, role=None):
        """Start a new mock interview session"""
        if interview_type not in self.interview_types:
            return {"error": "Invalid interview type"}
        
        interview_config = self.interview_types[interview_type]
        
        # Generate questions based on type and difficulty
        questions = self._generate_questions(interview_type, difficulty, company, role)
        
        session = {
            'id': f"interview_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'type': interview_type,
            'difficulty': difficulty,
            'company': company,
            'role': role,
            'questions': questions,
            'current_question': 0,
            'responses': [],
            'start_time': datetime.now().isoformat(),
            'duration': interview_config['duration'],
            'status': 'active'
        }
        
        return session
    
    def _generate_questions(self, interview_type, difficulty, company=None, role=None):
        """Generate questions for the interview session"""
        questions = []
        
        # Get base questions from question bank
        if interview_type in self.question_bank and difficulty in self.question_bank[interview_type]:
            base_questions = self.question_bank[interview_type][difficulty]
            # Take more questions from template bank if AI fails
            questions.extend(random.sample(base_questions, min(5, len(base_questions))))
        
        # Generate additional AI-powered questions
        try:
            ai_questions = self._generate_ai_questions(interview_type, difficulty, company, role)
            if ai_questions:
                # Replace some template questions with AI questions if available
                questions = questions[:3] + ai_questions[:2]
        except Exception as e:
            print(f"⚠️ AI question generation failed: {e}")
            print(f"💡 Using template questions from question bank")
        
        # Ensure we always have at least 3 questions
        if len(questions) < 3:
            print(f"❌ Not enough questions generated, adding default fallbacks")
            fallback_questions = [
                "Tell me about your experience and background",
                "What interests you most about this role?",
                "Describe a challenging problem you've solved recently"
            ]
            questions.extend(fallback_questions[:3-len(questions)])
        
        return questions[:5]  # Limit to 5 questions per session
    
    def _generate_ai_questions(self, interview_type, difficulty, company=None, role=None):
        """Generate AI-powered interview questions"""
        company_context = f" for {company}" if company else ""
        role_context = f" for a {role} position" if role else ""
        
        prompt = f"""
        Generate 2 high-quality {interview_type} interview questions at {difficulty} level{company_context}{role_context}.
        
        Requirements:
        - Questions should be realistic and commonly asked
        - Appropriate for the specified difficulty level
        - If company is specified, tailor to their interview style
        - Return only the questions, one per line
        """
        
        try:
            response_text = self.ai_service.generate_text(prompt, max_tokens=300)
            
            if not response_text:
                print("⚠️ AI service returned empty response")
                return []
            
            questions = response_text.strip().split('\n')
            return [q.strip() for q in questions if q.strip()]
        except Exception as e:
            print(f"⚠️ AI API error: {e}")
            print(f"💡 Consider upgrading your AI plan or checking billing details")
            print(f"🔄 Using template-based question generation instead...")
            return []
    
    def submit_answer(self, session_id, question_index, answer, response_time=None):
        """Submit an answer for evaluation"""
        # In a real implementation, you'd store session data in a database
        # For now, we'll return immediate feedback
        
        feedback = self._evaluate_answer(answer, question_index, session_id)
        
        response_data = {
            'question_index': question_index,
            'answer': answer,
            'response_time': response_time,
            'feedback': feedback,
            'timestamp': datetime.now().isoformat()
        }
        
        return response_data
    
    def _evaluate_answer(self, answer, question_index, session_id):
        """Evaluate an interview answer using AI"""
        try:
            prompt = f"""
            Evaluate this interview answer and provide constructive feedback:
            
            Answer: "{answer}"
            
            Please provide:
            1. Overall score (1-10)
            2. Strengths in the answer
            3. Areas for improvement
            4. Suggestions for better responses
            
            Format as JSON with keys: score, strengths, improvements, suggestions
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.3
            )
            
            # Try to parse as JSON, fallback to text
            try:
                feedback = json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                feedback = {
                    "score": 7,
                    "strengths": ["Answer provided"],
                    "improvements": ["Could be more detailed"],
                    "suggestions": ["Use specific examples and metrics"]
                }
            
            return feedback
            
        except Exception as e:
            print(f"Answer evaluation failed: {e}")
            return {
                "score": 5,
                "strengths": ["Response submitted"],
                "improvements": ["Technical evaluation unavailable"],
                "suggestions": ["Practice more detailed responses"]
            }
    
    def get_final_report(self, session_data):
        """Generate a comprehensive interview report"""
        if not session_data.get('responses'):
            return {"error": "No responses to evaluate"}
        
        # Calculate overall metrics
        scores = [r.get('feedback', {}).get('score', 5) for r in session_data['responses']]
        average_score = sum(scores) / len(scores) if scores else 0
        
        # Calculate performance by category
        strengths = []
        improvements = []
        
        for response in session_data['responses']:
            feedback = response.get('feedback', {})
            if feedback.get('strengths'):
                strengths.extend(feedback['strengths'])
            if feedback.get('improvements'):
                improvements.extend(feedback['improvements'])
        
        # Generate overall recommendations
        recommendations = self._generate_recommendations(session_data, average_score)
        
        report = {
            'session_id': session_data.get('id'),
            'interview_type': session_data.get('type'),
            'difficulty': session_data.get('difficulty'),
            'total_questions': len(session_data.get('questions', [])),
            'questions_answered': len(session_data.get('responses', [])),
            'average_score': round(average_score, 1),
            'score_breakdown': scores,
            'strengths': list(set(strengths))[:5],  # Top 5 unique strengths
            'improvements': list(set(improvements))[:5],  # Top 5 unique improvements
            'recommendations': recommendations,
            'completion_rate': len(session_data.get('responses', [])) / len(session_data.get('questions', [])) * 100,
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def _generate_recommendations(self, session_data, average_score):
        """Generate personalized recommendations based on performance"""
        recommendations = []
        
        if average_score >= 8:
            recommendations.append("Excellent performance! Focus on advanced topics to further excel.")
        elif average_score >= 6:
            recommendations.append("Good foundation. Practice more complex scenarios.")
        else:
            recommendations.append("Focus on fundamentals and practice basic concepts.")
        
        interview_type = session_data.get('type', 'technical')
        
        if interview_type == 'technical':
            recommendations.extend([
                "Practice coding problems daily on platforms like LeetCode",
                "Review common data structures and algorithms",
                "Practice explaining your thought process clearly"
            ])
        elif interview_type == 'behavioral':
            recommendations.extend([
                "Prepare STAR method responses for common scenarios",
                "Practice storytelling and specific examples",
                "Research the company culture and values"
            ])
        elif interview_type == 'system_design':
            recommendations.extend([
                "Study scalable system architectures",
                "Practice drawing system diagrams",
                "Learn about trade-offs in system design"
            ])
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def get_practice_suggestions(self, interview_type, performance_history=None):
        """Get personalized practice suggestions"""
        suggestions = {
            'daily_practice': [],
            'study_materials': [],
            'mock_sessions': [],
            'improvement_areas': []
        }
        
        if interview_type == 'technical':
            suggestions['daily_practice'] = [
                "Solve 2-3 coding problems daily",
                "Practice whiteboard coding",
                "Review algorithm time complexities"
            ]
            suggestions['study_materials'] = [
                "Cracking the Coding Interview book",
                "LeetCode premium subscription",
                "System Design Interview book"
            ]
        elif interview_type == 'behavioral':
            suggestions['daily_practice'] = [
                "Practice STAR method responses",
                "Record yourself answering questions",
                "Research company values and culture"
            ]
            suggestions['study_materials'] = [
                "Company Glassdoor reviews",
                "LinkedIn company page insights",
                "Industry-specific behavioral guides"
            ]
        
        return suggestions