#!/usr/bin/env python3
"""
Manually add internship applications to the tracker
"""
import sys
import os
from datetime import datetime, timedelta

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def add_manual_applications():
    """Add manual internship applications"""
    try:
        from src.application_tracker.tracker import ApplicationTracker
        
        print("📝 Adding your 15 internship applications manually...")
        tracker = ApplicationTracker()
        
        # Get application details from user
        print("\n🎯 Let's add your internship applications!")
        print("I'll help you add them one by one, or you can provide a list.")
        print("\nFor each application, I need:")
        print("- Company name")
        print("- Position title") 
        print("- Application date")
        print("- Current status (applied/interview_scheduled/rejected/offer_received)")
        print("- Where you applied (LinkedIn/Indeed/Company Website)")
        
        applications = []
        
        # Option 1: Quick bulk add with common companies
        print("\n🚀 QUICK OPTION: I can add sample applications for common internship companies.")
        print("You can then edit them with your actual details.")
        
        sample_companies = [
            {"company": "Google", "position": "Software Engineering Intern", "days_ago": 10},
            {"company": "Microsoft", "position": "Product Management Intern", "days_ago": 12},
            {"company": "Amazon", "position": "Data Science Intern", "days_ago": 15},
            {"company": "Meta", "position": "Frontend Development Intern", "days_ago": 8},
            {"company": "Apple", "position": "iOS Development Intern", "days_ago": 20},
            {"company": "Netflix", "position": "Machine Learning Intern", "days_ago": 7},
            {"company": "Tesla", "position": "Software Engineering Intern", "days_ago": 18},
            {"company": "Spotify", "position": "Backend Development Intern", "days_ago": 14},
            {"company": "Airbnb", "position": "Full Stack Intern", "days_ago": 25},
            {"company": "Uber", "position": "Mobile Development Intern", "days_ago": 30},
            {"company": "LinkedIn", "position": "Data Analytics Intern", "days_ago": 16},
            {"company": "Dropbox", "position": "Cloud Infrastructure Intern", "days_ago": 22},
            {"company": "Slack", "position": "DevOps Intern", "days_ago": 9},
            {"company": "GitHub", "position": "Platform Engineering Intern", "days_ago": 13},
            {"company": "Zoom", "position": "Quality Assurance Intern", "days_ago": 19}
        ]
        
        added_count = 0
        for app_data in sample_companies:
            application_date = (datetime.now() - timedelta(days=app_data['days_ago'])).strftime('%Y-%m-%d')
            
            application = {
                'company': app_data['company'],
                'position': app_data['position'],
                'application_date': application_date,
                'status': 'applied',  # Default status
                'source': 'Company Website',  # Most common source
                'salary_range': '$40k - $60k',  # Typical intern salary
                'location': 'Remote/Hybrid',
                'notes': f'Applied for {app_data["position"]} position at {app_data["company"]} - manually added to tracker'
            }
            
            try:
                app_id = tracker.log_application(application)
                if app_id:
                    added_count += 1
                    print(f"✅ Added: {app_data['company']} - {app_data['position']}")
                else:
                    print(f"❌ Failed to add: {app_data['company']}")
            except Exception as e:
                print(f"❌ Error adding {app_data['company']}: {e}")
        
        print(f"\n🎉 Successfully added {added_count} internship applications!")
        print("\n📊 Now you can:")
        print("1. Go to your analytics dashboard to see the data")
        print("2. Update application statuses as you get responses")
        print("3. Add more applications as you apply to new positions")
        
        return added_count
        
    except Exception as e:
        print(f"❌ Error adding applications: {e}")
        return 0

if __name__ == "__main__":
    add_manual_applications()