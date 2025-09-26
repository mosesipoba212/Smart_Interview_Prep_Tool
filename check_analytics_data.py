#!/usr/bin/env python3
"""
Check what analytics data will be displayed
"""
import sqlite3
import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.application_tracker.tracker import ApplicationTracker

def check_analytics_data():
    """Check what analytics data will be displayed"""
    try:
        print("📊 Checking analytics data...")
        
        # Initialize application tracker
        tracker = ApplicationTracker()
        
        # Get application stats (what the analytics page uses)
        stats = tracker.get_application_stats()
        interview_analytics = tracker.get_interview_analytics()
        
        print("\n📈 Application Statistics:")
        print(f"  - Total Applications: {stats.get('total_applications', 0)}")
        print(f"  - Response Rate: {stats.get('response_rate', 0):.1f}%")
        print(f"  - Interview Rate: {stats.get('interview_rate', 0):.1f}%")
        print(f"  - Success Rate: {stats.get('success_rate', 0):.1f}%")
        
        print("\n📊 Status Breakdown:")
        status_breakdown = stats.get('status_breakdown', {})
        for status, count in status_breakdown.items():
            print(f"  - {status.title()}: {count}")
        
        print("\n🏢 Companies Applied To:")
        companies = stats.get('companies', [])
        for company in companies[:5]:  # Show first 5
            print(f"  - {company}")
        
        print("\n📅 Monthly Breakdown:")
        monthly = stats.get('monthly_breakdown', [])
        for month_data in monthly[-3:]:  # Show last 3 months
            print(f"  - {month_data.get('month', 'Unknown')}: {month_data.get('count', 0)} applications")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking analytics data: {e}")
        return False

if __name__ == "__main__":
    check_analytics_data()