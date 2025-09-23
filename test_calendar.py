#!/usr/bin/env python3
"""
Test script for Google Calendar integration
"""

import sys
import os
from datetime import datetime, timedelta

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from calendar_integration.calendar_service import CalendarService

def test_calendar_integration():
    """Test the calendar integration functionality"""
    print("🗓️  Testing Google Calendar Integration...")
    print("=" * 50)
    
    # Initialize calendar service
    calendar_service = CalendarService()
    
    # Test 1: Schedule prep blocks for a mock interview
    print("\n📅 Test 1: Scheduling interview prep blocks")
    print("-" * 40)
    
    # Schedule for an interview next week
    next_week = datetime.now() + timedelta(days=7)
    interview_date = next_week.strftime('%Y-%m-%d')
    
    prep_blocks = calendar_service.schedule_prep_blocks(
        interview_date=interview_date,
        interview_type='technical',
        duration_hours=3
    )
    
    print(f"✅ Scheduled {len(prep_blocks)} prep blocks:")
    for i, block in enumerate(prep_blocks, 1):
        start_time = block['start_time'].strftime('%Y-%m-%d %H:%M')
        print(f"   {i}. {block['title']}")
        print(f"      📅 {start_time}")
        print(f"      📝 {block['description']}")
        print(f"      🔗 Status: {block['status']}")
        print()
    
    # Test 2: Get upcoming interviews
    print("\n📋 Test 2: Getting upcoming interviews")
    print("-" * 40)
    
    upcoming = calendar_service.get_upcoming_interviews(days_ahead=14)
    
    if upcoming:
        print(f"✅ Found {len(upcoming)} upcoming interview-related events:")
        for i, event in enumerate(upcoming, 1):
            print(f"   {i}. {event['title']}")
            print(f"      📅 {event['start_time']}")
            print(f"      📝 {event.get('description', 'No description')}")
            print()
    else:
        print("📭 No upcoming interviews found")
    
    # Test 3: Check calendar conflicts
    print("\n⏰ Test 3: Checking for calendar conflicts")
    print("-" * 40)
    
    # Check for conflicts tomorrow 2-4 PM
    tomorrow = datetime.now() + timedelta(days=1)
    start_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=2)
    
    conflicts = calendar_service.get_calendar_conflicts(start_time, end_time)
    
    if conflicts:
        print(f"⚠️  Found {len(conflicts)} calendar conflicts:")
        for conflict in conflicts:
            print(f"   - {conflict['title']}")
            print(f"     {conflict['start']} - {conflict['end']}")
    else:
        print("✅ No calendar conflicts found for the time slot")
    
    # Test 4: Suggest alternative times
    print("\n💡 Test 4: Suggesting alternative times")
    print("-" * 40)
    
    alternatives = calendar_service.suggest_alternative_times(start_time, 2)
    
    if alternatives:
        print(f"✅ Found {len(alternatives)} alternative time slots:")
        for i, alt_time in enumerate(alternatives, 1):
            print(f"   {i}. {alt_time.strftime('%Y-%m-%d %H:%M')}")
    else:
        print("❌ No alternative times available")
    
    # Test 5: Integration status
    print("\n🔍 Integration Status Report")
    print("-" * 40)
    
    if calendar_service.mock_mode:
        print("⚠️  Calendar service is running in MOCK MODE")
        print("   Reasons this might be happening:")
        print("   • Google Calendar API not enabled")
        print("   • credentials.json missing calendar scopes")
        print("   • OAuth consent screen needs calendar permissions")
        print("\n🔧 To enable full integration:")
        print("   1. Enable Google Calendar API in Google Cloud Console")
        print("   2. Add calendar scopes to OAuth consent screen")
        print("   3. Re-authenticate the application")
    else:
        print("✅ Calendar service is connected to Google Calendar API")
        print("   All calendar features are fully functional!")
    
    print("\n" + "=" * 50)
    print("🎉 Calendar integration test completed!")
    
    return calendar_service.mock_mode

if __name__ == "__main__":
    is_mock_mode = test_calendar_integration()
    
    if is_mock_mode:
        print("\n🚀 Next Steps:")
        print("1. Complete Google Calendar API setup in browser")
        print("2. Add calendar scopes to OAuth consent screen")
        print("3. Re-run this test to verify full integration")
    else:
        print("\n✅ Calendar integration is working perfectly!")