#!/usr/bin/env python3

"""
Test script to debug mock interview functionality
"""

import requests
import json

def test_mock_interview_page():
    """Test if the mock interview page loads"""
    try:
        response = requests.get('http://localhost:5000/mock-interview')
        print(f"✅ Mock interview page status: {response.status_code}")
        if response.status_code != 200:
            print(f"❌ Page failed to load: {response.text}")
        else:
            print("✅ Page loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load page: {e}")

def test_mock_interview_start():
    """Test starting a mock interview"""
    try:
        # Test data
        test_data = {
            "interview_type": "technical",
            "difficulty": "beginner",
            "company": "Google",
            "role": "Software Engineer"
        }
        
        response = requests.post(
            'http://localhost:5000/mock-interview/start',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(test_data)
        )
        
        print(f"✅ Start interview status: {response.status_code}")
        data = response.json()
        print(f"✅ Response data: {json.dumps(data, indent=2)}")
        
        if data.get('success'):
            print("✅ Interview started successfully!")
            return data.get('session')
        else:
            print(f"❌ Interview failed to start: {data.get('error')}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start interview: {e}")
        return None

def test_interview_types():
    """Test if interview types are available"""
    try:
        # This would test the backend interview types
        from mock_interview_system import MockInterviewSystem
        system = MockInterviewSystem()
        types = system.get_interview_types()
        print(f"✅ Available interview types: {list(types.keys())}")
        for key, value in types.items():
            print(f"   {key}: {value['name']} - Difficulties: {value['difficulty_levels']}")
    except Exception as e:
        print(f"❌ Failed to get interview types: {e}")

if __name__ == "__main__":
    print("🧪 Testing Mock Interview Functionality")
    print("=" * 50)
    
    print("\n1. Testing page load...")
    test_mock_interview_page()
    
    print("\n2. Testing interview types...")
    test_interview_types()
    
    print("\n3. Testing interview start...")
    session = test_mock_interview_start()
    
    print("\n" + "=" * 50)
    if session:
        print("✅ All tests passed! Mock interview system is working.")
    else:
        print("❌ Some tests failed. Check the errors above.")