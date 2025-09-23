#!/usr/bin/env python3
"""
Setup Script for Smart Interview Prep Tool
Handles initial configuration and credential setup
"""

import os
import json
import shutil
from pathlib import Path

def create_directory_structure():
    """Create necessary directories"""
    directories = [
        'data',
        'logs',
        'exports',
        'credentials',
        'tests'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def setup_environment_file():
    """Setup environment configuration"""
    env_template = "config/.env.template"
    env_file = ".env"
    
    if os.path.exists(env_template) and not os.path.exists(env_file):
        shutil.copy(env_template, env_file)
        print(f"✅ Created {env_file} from template")
        print(f"📝 Please edit {env_file} and add your API keys")
    else:
        print(f"⚠️  {env_file} already exists or template not found")

def setup_credentials_info():
    """Create credential setup instructions"""
    instructions = """
# API Credentials Setup Instructions

## Gmail API Setup
1. Go to Google Cloud Console (https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create credentials (OAuth 2.0 Client ID)
5. Download credentials.json and place in project root

## Google Calendar API Setup  
1. In the same Google Cloud project
2. Enable Google Calendar API
3. Use the same OAuth credentials or create new ones
4. Download calendar_credentials.json and place in project root

## OpenAI API Setup
1. Sign up at https://platform.openai.com/
2. Generate an API key
3. Add the key to your .env file

## Required Files:
- credentials.json (Gmail API)
- calendar_credentials.json (Calendar API)  
- .env (API keys and configuration)

## File Structure:
```
Smart_Interview_Prep_Tool/
├── credentials.json          # Gmail API credentials
├── calendar_credentials.json # Calendar API credentials
├── .env                     # Environment variables
├── main.py                  # Main application
└── ...
```
"""
    
    with open("CREDENTIALS_SETUP.md", "w", encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ Created CREDENTIALS_SETUP.md with setup instructions")

def create_sample_config():
    """Create sample configuration files"""
    sample_configs = {
        "interview_types.json": {
            "technical": {
                "description": "Technical interviews focusing on coding and algorithms",
                "typical_duration": 60,
                "preparation_focus": ["algorithms", "data_structures", "system_design"]
            },
            "behavioral": {
                "description": "Behavioral interviews focusing on soft skills",
                "typical_duration": 45,
                "preparation_focus": ["STAR_method", "company_research", "career_stories"]
            },
            "system_design": {
                "description": "System design interviews for senior positions",
                "typical_duration": 90,
                "preparation_focus": ["architecture", "scalability", "trade_offs"]
            }
        },
        "company_profiles.json": {
            "google": {
                "interview_process": ["phone_screen", "technical", "system_design", "behavioral"],
                "focus_areas": ["algorithms", "system_design", "googleyness"],
                "preparation_tips": ["Practice LeetCode", "Study Google's products"]
            },
            "microsoft": {
                "interview_process": ["phone_screen", "technical", "behavioral"],
                "focus_areas": ["algorithms", "design_patterns", "collaboration"],
                "preparation_tips": ["Practice coding", "Understand Microsoft's culture"]
            }
        }
    }
    
    config_dir = "config"
    for filename, content in sample_configs.items():
        filepath = os.path.join(config_dir, filename)
        with open(filepath, "w", encoding='utf-8') as f:
            json.dump(content, f, indent=2)
        print(f"✅ Created sample config: {filepath}")

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask',
        'google-auth',
        'google-auth-oauthlib', 
        'google-auth-httplib2',
        'google-api-python-client',
        'openai',
        'beautifulsoup4',
        'python-dotenv',
        'pandas',
        'matplotlib',
        'sqlite3'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sqlite3':
                import sqlite3
            else:
                __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n📦 To install missing packages, run:")
        print(f"pip install {' '.join(missing_packages)}")
        print("Or install all requirements with:")
        print("pip install -r requirements.txt")
    else:
        print("\n✅ All required packages are installed!")

def create_test_files():
    """Create basic test files"""
    test_content = '''"""
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
'''
    
    os.makedirs('tests', exist_ok=True)
    with open('tests/test_basic.py', 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("✅ Created basic test file: tests/test_basic.py")

def main():
    """Run the complete setup"""
    print("🚀 Setting up Smart Interview Prep Tool...")
    print("=" * 50)
    
    # Create directory structure
    create_directory_structure()
    
    # Setup environment file
    setup_environment_file()
    
    # Create credential setup instructions
    setup_credentials_info()
    
    # Create sample configurations
    create_sample_config()
    
    # Create test files
    create_test_files()
    
    # Check dependencies
    print("\n📋 Checking Dependencies:")
    print("-" * 30)
    check_dependencies()
    
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("\n📝 Next steps:")
    print("1. Install missing packages: pip install -r requirements.txt")
    print("2. Read CREDENTIALS_SETUP.md for API setup")
    print("3. Edit .env file with your API keys")
    print("4. Run: python main.py")
    print("\n🎯 Happy interviewing!")

if __name__ == "__main__":
    main()
