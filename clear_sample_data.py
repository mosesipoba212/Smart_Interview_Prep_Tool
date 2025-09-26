#!/usr/bin/env python3
"""
Clear sample data from application tracker database
"""
import sqlite3
import sys
import os

def clear_sample_data():
    """Clear all sample data from the application tracker database"""
    try:
        # Connect to database
        db_path = 'application_tracker.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check what tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Found tables: {tables}")
        
        # Clear data from existing tables
        tables_to_clear = ['applications', 'responses', 'outcomes']
        
        for table_name in tables_to_clear:
            try:
                cursor.execute(f"DELETE FROM {table_name}")
                print(f"✅ Cleared data from {table_name}")
            except sqlite3.OperationalError as e:
                print(f"⚠️ Table {table_name} doesn't exist: {e}")
        
        # Commit changes
        conn.commit()
        print("🧹 Sample data cleared successfully!")
        
        # Verify data is cleared
        cursor.execute("SELECT COUNT(*) FROM applications")
        count = cursor.fetchone()[0]
        print(f"📊 Applications remaining: {count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error clearing sample data: {e}")
        return False

if __name__ == "__main__":
    clear_sample_data()