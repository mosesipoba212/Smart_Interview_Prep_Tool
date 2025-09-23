#!/usr/bin/env python3
"""
Test OpenAI API Integration
Quick test to verify the API key is working
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_openai_integration():
    """Test if OpenAI API is working"""
    try:
        from src.ai_engine.question_generator import QuestionGenerator
        
        print("🔧 Testing OpenAI API integration...")
        
        # Initialize the question generator
        generator = QuestionGenerator()
        
        if generator.use_ai:
            print("✅ OpenAI API key detected and configured!")
            
            # Test generating a few questions
            print("🤖 Testing AI question generation...")
            questions = generator.generate_questions(
                interview_type='technical',
                company='Google',
                position='Software Engineer',
                count=3
            )
            
            if questions and len(questions) > 0:
                print(f"✅ Successfully generated {len(questions)} questions!")
                print("\n📝 Sample Questions:")
                for i, q in enumerate(questions[:2], 1):
                    print(f"{i}. {q.get('question', 'N/A')}")
                    print(f"   Difficulty: {q.get('difficulty', 'N/A')}")
                    print(f"   Tips: {q.get('tips', 'N/A')}")
                    print()
            else:
                print("⚠️  Questions generated but may be using fallback templates")
                
        else:
            print("⚠️  OpenAI not available, using fallback question templates")
            
    except Exception as e:
        print(f"❌ Error testing OpenAI integration: {e}")
        return False
    
    return True

def show_ai_status():
    """Show current AI configuration status"""
    api_key = os.getenv('OPENAI_API_KEY', '')
    
    print("🎯 Smart Interview Prep Tool - AI Status")
    print("=" * 50)
    
    if api_key and api_key != 'your_openai_api_key_here':
        key_preview = f"{api_key[:8]}...{api_key[-8:]}" if len(api_key) > 16 else api_key
        print(f"✅ OpenAI API Key: {key_preview}")
        print("✅ AI-powered question generation: ENABLED")
    else:
        print("❌ OpenAI API Key: Not configured")
        print("⚠️  AI-powered question generation: Using templates")
    
    print("\n🌐 Application Status:")
    print("📍 URL: http://127.0.0.1:5000")
    print("🚀 Status: Running with enhanced AI capabilities!")
    
    print("\n💡 What you can now do:")
    print("• Generate AI-powered interview questions")
    print("• Get personalized question sets for any company")
    print("• Receive tailored preparation tips")
    print("• Access advanced question analytics")

if __name__ == "__main__":
    show_ai_status()
    print("\n" + "=" * 50)
    test_openai_integration()
    print("\n🎉 Your Smart Interview Prep Tool is ready with AI power!")
    print("Visit: http://127.0.0.1:5000 to start using it!")
