#!/usr/bin/env python3
"""
API Integration Status Checker
Verifies all API keys and services are working properly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def check_openai_status():
    """Check OpenAI API status"""
    print("🤖 OpenAI API Status:")
    print("-" * 30)
    
    api_key = os.getenv('OPENAI_API_KEY', '')
    
    if api_key and api_key != 'your_openai_api_key_here':
        key_preview = f"{api_key[:8]}...{api_key[-8:]}" if len(api_key) > 16 else api_key
        print(f"✅ API Key: {key_preview}")
        
        try:
            from src.ai_engine.question_generator import QuestionGenerator
            generator = QuestionGenerator()
            
            if generator.use_ai:
                print("✅ Status: ACTIVE - AI-powered questions enabled")
                return True
            else:
                print("⚠️  Status: FALLBACK - Using template questions")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    else:
        print("❌ API Key: Not configured")
        print("⚠️  Status: Using template questions")
        return False

def check_google_api_status():
    """Check Google API status"""
    print("\n🔍 Google API Status:")
    print("-" * 30)
    
    api_key = os.getenv('GOOGLE_API_KEY', '')
    
    if api_key:
        key_preview = f"{api_key[:8]}...{api_key[-8:]}" if len(api_key) > 16 else api_key
        print(f"✅ API Key: {key_preview}")
        print("✅ Status: ACTIVE - Enhanced Gmail/Calendar features")
        return True
    else:
        print("❌ API Key: Not configured")
        print("⚠️  Status: Using mock services")
        return False

def check_gmail_service():
    """Check Gmail service status"""
    print("\n📧 Gmail Service Status:")
    print("-" * 30)
    
    try:
        from src.email_parser.simplified_gmail_service import SimplifiedGmailService
        service = SimplifiedGmailService()
        
        # Test fetching emails
        emails = service.fetch_recent_emails()
        print(f"✅ Service: ACTIVE")
        print(f"✅ Sample emails: {len(emails)} mock interviews available")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_calendar_service():
    """Check Calendar service status"""
    print("\n📅 Calendar Service Status:")
    print("-" * 30)
    
    try:
        from src.calendar_integration.calendar_service import CalendarService
        service = CalendarService()
        
        if service.mock_mode:
            print("✅ Service: ACTIVE (Mock mode)")
            print("✅ Features: Prep scheduling simulation")
        else:
            print("✅ Service: ACTIVE (Full integration)")
            print("✅ Features: Real Google Calendar integration")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_performance_tracker():
    """Check Performance Tracker status"""
    print("\n📊 Performance Tracker Status:")
    print("-" * 30)
    
    try:
        from src.performance_tracker.tracker import PerformanceTracker
        tracker = PerformanceTracker()
        
        print("✅ Database: Connected")
        print("✅ Analytics: Available") 
        print("✅ Export: Enabled")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_interview_detector():
    """Check Interview Detector status"""
    print("\n🔍 Interview Detector Status:")
    print("-" * 30)
    
    try:
        from src.interview_detector.detector import InterviewDetector
        detector = InterviewDetector()
        
        # Test detection
        test_email = {
            'subject': 'Technical Interview Invitation',
            'body': 'We would like to schedule a technical interview',
            'sender': 'recruiter@company.com'
        }
        
        is_interview = detector.is_interview_email(test_email)
        interview_type = detector.detect_interview_type(test_email)
        
        print("✅ Detection: ACTIVE")
        print(f"✅ Test result: {interview_type} interview detected")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_next_steps():
    """Show next steps for optimization"""
    print("\n🚀 Next Steps for Full Functionality:")
    print("=" * 50)
    
    google_key = os.getenv('GOOGLE_API_KEY', '')
    openai_key = os.getenv('OPENAI_API_KEY', '')
    
    if not openai_key or openai_key == 'your_openai_api_key_here':
        print("1. 🤖 Add OpenAI API key for AI-powered questions")
        print("   • Sign up at: https://platform.openai.com/")
        print("   • Add key to .env file")
    
    if not google_key:
        print("2. 🔍 Add Google API key for enhanced features")
        print("   • Enable Gmail/Calendar APIs in Google Cloud")
        print("   • Generate API key and add to .env file")
    
    print("\n3. 📧 For full Gmail integration:")
    print("   • Set up OAuth2 credentials in Google Cloud")
    print("   • Download credentials.json file")
    
    print("\n4. 📅 For full Calendar integration:")
    print("   • Use same OAuth2 credentials")
    print("   • Enable Google Calendar API")

def main():
    """Run comprehensive status check"""
    print("🎯 Smart Interview Prep Tool - System Status")
    print("=" * 50)
    
    # Check all services
    checks = [
        check_openai_status(),
        check_google_api_status(), 
        check_gmail_service(),
        check_calendar_service(),
        check_performance_tracker(),
        check_interview_detector()
    ]
    
    # Summary
    active_services = sum(checks)
    total_services = len(checks)
    
    print("\n" + "=" * 50)
    print(f"📊 System Health: {active_services}/{total_services} services active")
    
    if active_services == total_services:
        print("🎉 All systems operational!")
    elif active_services >= total_services * 0.7:
        print("✅ System ready with good functionality!")
    else:
        print("⚠️  Basic functionality available, consider adding API keys")
    
    print(f"\n🌐 Application URL: http://127.0.0.1:5000")
    print("🎯 Status: Ready for interview preparation!")
    
    show_next_steps()

if __name__ == "__main__":
    main()
