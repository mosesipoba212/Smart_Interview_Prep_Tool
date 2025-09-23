"""
Basic tests for Smart Interview Prep Tool
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestInterviewDetector(unittest.TestCase):
    def setUp(self):
        from src.interview_detector.detector import InterviewDetector
        self.detector = InterviewDetector()
    
    def test_is_interview_email(self):
        # Test email that should be detected as interview
        email = {
            'subject': 'Technical Interview Invitation',
            'body': 'We would like to schedule a technical interview',
            'sender': 'recruiter@company.com'
        }
        self.assertTrue(self.detector.is_interview_email(email))
    
    def test_detect_interview_type(self):
        email = {
            'subject': 'Technical Interview',
            'body': 'coding challenge and algorithms'
        }
        interview_type = self.detector.detect_interview_type(email)
        self.assertEqual(interview_type, 'technical')

class TestQuestionGenerator(unittest.TestCase):
    def setUp(self):
        from src.ai_engine.question_generator import QuestionGenerator
        self.generator = QuestionGenerator()
    
    def test_generate_questions(self):
        questions = self.generator.generate_questions('technical', 'Google', 'Software Engineer', 5)
        self.assertEqual(len(questions), 5)
        self.assertTrue(all('question' in q for q in questions))

if __name__ == '__main__':
    unittest.main()
