#!/usr/bin/env python3
"""
Add realistic job application sample data for demonstration
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.application_tracker.tracker import ApplicationTracker

def add_realistic_sample_data():
    """Add realistic job application data"""
    try:
        print("📊 Adding realistic job application sample data...")
        tracker = ApplicationTracker()
        
        # Realistic job applications with proper company names
        realistic_applications = [
            {
                'company': 'Google',
                'position': 'Graduate Software Engineer',
                'application_date': (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'),
                'status': 'applied',
                'source': 'Company Website',
                'salary_range': '$120k - $180k',
                'location': 'London, UK',
                'notes': 'Applied for Graduate Software Engineer position, waiting for response'
            },
            {
                'company': 'Microsoft',
                'position': 'Software Development Engineer',
                'application_date': (datetime.now() - timedelta(days=22)).strftime('%Y-%m-%d'),
                'status': 'interview_scheduled',
                'source': 'LinkedIn',
                'salary_range': '$110k - $170k',
                'location': 'Cambridge, UK',
                'notes': 'Phone interview scheduled for next week'
            },
            {
                'company': 'Amazon',
                'position': 'Junior Developer',
                'application_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'status': 'rejected',
                'source': 'Indeed',
                'salary_range': '$90k - $140k',
                'location': 'Manchester, UK',
                'notes': 'Received rejection email after initial screening'
            },
            {
                'company': 'Meta',
                'position': 'Frontend Engineer',
                'application_date': (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d'),
                'status': 'interview_scheduled',
                'source': 'Company Website',
                'salary_range': '$115k - $175k',
                'location': 'London, UK',
                'notes': 'Technical interview scheduled, preparing for coding questions'
            },
            {
                'company': 'Apple',
                'position': 'iOS Developer',
                'application_date': (datetime.now() - timedelta(days=45)).strftime('%Y-%m-%d'),
                'status': 'offer_received',
                'source': 'Referral',
                'salary_range': '$125k - $185k',
                'location': 'London, UK',
                'notes': 'Received offer! Negotiating salary and benefits'
            }
        ]
        
        # Add applications to database
        added_count = 0
        for app_data in realistic_applications:
            app_id = tracker.log_application(app_data)
            if app_id:
                added_count += 1
                print(f"✅ Added: {app_data['company']} - {app_data['position']} ({app_data['status']})")
        
        print(f"\n🎉 Added {added_count} realistic job applications!")
        print("\nNow your analytics will show:")
        print("- Real company names (Google, Microsoft, Amazon, Meta, Apple)")  
        print("- Different application statuses (applied, interview_scheduled, rejected, offer_received)")
        print("- Realistic salary ranges and job titles")
        print("- Applications spread over time (last 45 days)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        return False

if __name__ == "__main__":
    add_realistic_sample_data()