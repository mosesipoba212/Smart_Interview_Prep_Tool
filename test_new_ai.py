"""
Test the new AI service integration
"""

from src.ai_engine.ai_service import ai_service
from src.ai_engine.question_generator import QuestionGenerator

def test_ai_service():
    """Test the universal AI service"""
    print("🧪 Testing Universal AI Service")
    print("=" * 50)
    
    # Check provider info
    provider_info = ai_service.get_provider_info()
    print(f"Current Provider: {provider_info['name']}")
    print(f"Type: {provider_info['type']}")
    print(f"Cost: {provider_info['cost']}")
    
    # List all available providers
    providers = ai_service.list_providers()
    print(f"\nAvailable Providers: {len(providers)}")
    for p in providers:
        print(f"  - {p['name']} ({p['cost']})")
    
    # Test question generation
    print("\n🤖 Testing Question Generation")
    generator = QuestionGenerator()
    
    questions = generator.generate_questions(
        interview_type="technical",
        company="Google",
        position="Software Engineer",
        count=3
    )
    
    print(f"\nGenerated {len(questions)} questions:")
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q.get('question', 'No question')}")
        print(f"   Difficulty: {q.get('difficulty', 'Unknown')}")
        print(f"   Category: {q.get('category', 'Unknown')}")
        print()

if __name__ == "__main__":
    test_ai_service()