"""
Direct database sample data insertion
"""
import sqlite3
from datetime import datetime, timedelta
import random

def add_sample_data_directly():
    """Add sample data directly to the database"""
    
    # Connect to the application tracker database
    conn = sqlite3.connect('application_tracker.db')
    cursor = conn.cursor()
    
    # Sample companies and positions
    companies = [
        ("Google", "Software Engineer"),
        ("Microsoft", "Senior Developer"),
        ("Apple", "iOS Developer"), 
        ("Meta", "Frontend Engineer"),
        ("Amazon", "Full Stack Developer"),
        ("Netflix", "Backend Engineer"),
        ("Tesla", "Software Engineer"),
        ("Spotify", "Python Developer")
    ]
    
    # Application statuses
    statuses = ["applied", "rejected", "interview_scheduled", "offer"]
    status_weights = [0.5, 0.3, 0.15, 0.05]
    
    print("Adding sample applications...")
    
    for i, (company, position) in enumerate(companies):
        # Random application date in the last 60 days
        days_ago = random.randint(1, 60)
        app_date = (datetime.now() - timedelta(days=days_ago)).date()
        
        # Random status based on weights
        status = random.choices(statuses, weights=status_weights)[0]
        
        cursor.execute('''
            INSERT INTO applications (
                company, position, application_date, status, platform,
                salary_range, location, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            company,
            position,
            app_date,
            status,
            random.choice(["LinkedIn", "Indeed", "Company Website"]),
            f"${random.randint(80, 200)}k - ${random.randint(200, 300)}k",
            random.choice(["Remote", "San Francisco, CA", "Seattle, WA"]),
            f"Applied for {position} role at {company}"
        ))
        
        application_id = cursor.lastrowid
        print(f"✅ Added application: {company} - {position} (ID: {application_id})")
        
        # Add some responses for some applications
        if random.random() < 0.4:  # 40% chance of response
            response_types = ["interview_invitation", "rejection", "phone_screen"]
            response_type = random.choice(response_types)
            response_date = app_date + timedelta(days=random.randint(1, 14))
            
            cursor.execute('''
                INSERT INTO responses (
                    application_id, response_type, response_date, message
                ) VALUES (?, ?, ?, ?)
            ''', (
                application_id,
                response_type,
                response_date,
                f"Response from {company} regarding {position} position"
            ))
            print(f"  📧 Added response: {response_type}")
            
            # If interview invitation, add interview session
            if response_type == "interview_invitation":
                interview_date = response_date + timedelta(days=random.randint(1, 10))
                cursor.execute('''
                    INSERT INTO interview_sessions (
                        application_id, interview_type, scheduled_date, 
                        platform, status
                    ) VALUES (?, ?, ?, ?, ?)
                ''', (
                    application_id,
                    random.choice(["phone_screen", "technical", "behavioral"]),
                    interview_date,
                    random.choice(["Zoom", "Teams", "Phone"]),
                    "scheduled"
                ))
                print(f"  🎯 Added interview session")
    
    conn.commit()
    conn.close()
    print(f"\n✅ Sample data added successfully!")

if __name__ == "__main__":
    add_sample_data_directly()