"""
Test script to add sample application tracking data
"""
import requests
import json
from datetime import datetime, timedelta
import random

# Base URL for the app
BASE_URL = "http://127.0.0.1:5000"

# Sample companies and positions
companies = [
    ("Google", "Software Engineer"),
    ("Microsoft", "Senior Developer"),
    ("Apple", "iOS Developer"),
    ("Meta", "Frontend Engineer"),
    ("Amazon", "Full Stack Developer"),
    ("Netflix", "Backend Engineer"),
    ("Tesla", "Software Engineer"),
    ("Spotify", "Python Developer"),
    ("Uber", "Data Engineer"),
    ("Airbnb", "Product Engineer")
]

# Application statuses
statuses = ["applied", "rejected", "interview_scheduled", "offer", "pending"]
status_weights = [0.4, 0.3, 0.2, 0.05, 0.05]  # Most are applied/rejected

def add_sample_applications():
    """Add sample application data"""
    print("Adding sample application data...")
    
    for i, (company, position) in enumerate(companies):
        # Random application date in the last 60 days
        days_ago = random.randint(1, 60)
        app_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        # Random status based on weights
        status = random.choices(statuses, weights=status_weights)[0]
        
        application_data = {
            "company": company,
            "position": position,
            "application_date": app_date,
            "status": status,
            "platform": random.choice(["LinkedIn", "Indeed", "Company Website", "Glassdoor"]),
            "salary_range": f"${random.randint(80, 200)}k - ${random.randint(200, 300)}k",
            "location": random.choice(["Remote", "San Francisco, CA", "Seattle, WA", "New York, NY"]),
            "notes": f"Applied for {position} role at {company}"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/log-application", 
                                   json=application_data,
                                   headers={"Content-Type": "application/json"})
            
            if response.status_code == 200:
                print(f"✅ Added application: {company} - {position}")
            else:
                print(f"❌ Failed to add {company}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error adding {company}: {e}")

def add_sample_responses():
    """Add sample company responses"""
    print("Adding sample response data...")
    
    response_types = ["interview_invitation", "rejection", "phone_screen", "follow_up"]
    
    for i in range(5):  # Add 5 sample responses
        response_data = {
            "application_id": i + 1,  # Assume first 5 applications
            "response_type": random.choice(response_types),
            "response_date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
            "message": "Sample response message",
            "next_step": "Next step information"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/log-response", 
                                   json=response_data,
                                   headers={"Content-Type": "application/json"})
            
            if response.status_code == 200:
                print(f"✅ Added response for application {i+1}")
            else:
                print(f"❌ Failed to add response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error adding response: {e}")

if __name__ == "__main__":
    print("🚀 Adding sample data to Smart Interview Prep Tool...")
    add_sample_applications()
    add_sample_responses()
    print("✅ Sample data added! Check the analytics dashboard.")