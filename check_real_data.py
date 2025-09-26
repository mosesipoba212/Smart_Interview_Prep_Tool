#!/usr/bin/env python3
"""
Check what's actually in the database
"""
import sqlite3

def check_database():
    """Check what data is actually in the database"""
    try:
        conn = sqlite3.connect('application_tracker.db')
        cursor = conn.cursor()
        
        # Get applications
        cursor.execute('SELECT id, company, position, status, application_date, notes FROM applications')
        apps = cursor.fetchall()
        
        print("📊 Current applications in database:")
        print(f"Total applications: {len(apps)}")
        print("-" * 80)
        
        for app in apps:
            print(f"ID {app[0]}:")
            print(f"  Company: '{app[1]}'")
            print(f"  Position: '{app[2]}'") 
            print(f"  Status: '{app[3]}'")
            print(f"  Date: '{app[4]}'")
            print(f"  Notes: '{app[5][:100]}...'")
            print("-" * 40)
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")

if __name__ == "__main__":
    check_database()