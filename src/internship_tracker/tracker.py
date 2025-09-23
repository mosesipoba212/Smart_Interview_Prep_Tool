"""
Internship Tracker Module
Comprehensive internship application tracking system with analytics and deadline management
"""

import sqlite3
from datetime import datetime, timedelta
import json
from typing import List, Dict, Optional, Tuple

class InternshipTracker:
    def __init__(self, db_path: str = "internship_tracker.db"):
        """Initialize the internship tracker with database setup"""
        self.db_path = db_path
        self.setup_database()
    
    def setup_database(self):
        """Create database tables for internship tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Internship applications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS internship_applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                position_title TEXT NOT NULL,
                application_date DATE NOT NULL,
                deadline DATE,
                status TEXT NOT NULL DEFAULT 'Applied',
                priority TEXT DEFAULT 'Medium',
                location TEXT,
                job_url TEXT,
                salary_range TEXT,
                requirements TEXT,
                notes TEXT,
                follow_up_date DATE,
                response_date DATE,
                interview_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Application status history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS status_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER,
                old_status TEXT,
                new_status TEXT,
                change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (application_id) REFERENCES internship_applications (id)
            )
        ''')
        
        # Companies table for tracking company information
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT UNIQUE NOT NULL,
                industry TEXT,
                company_size TEXT,
                location TEXT,
                website TEXT,
                notes TEXT,
                rating INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Deadlines and reminders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS deadlines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER,
                deadline_type TEXT NOT NULL,
                deadline_date DATE NOT NULL,
                reminder_sent BOOLEAN DEFAULT FALSE,
                notes TEXT,
                FOREIGN KEY (application_id) REFERENCES internship_applications (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_internship(self, internship_data: Dict) -> int:
        """Add a new internship application"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert the application
        cursor.execute('''
            INSERT INTO internship_applications 
            (company_name, position_title, application_date, deadline, status, 
             priority, location, job_url, salary_range, requirements, notes, follow_up_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            internship_data.get('company_name'),
            internship_data.get('position_title'),
            internship_data.get('application_date', datetime.now().date()),
            internship_data.get('deadline'),
            internship_data.get('status', 'Applied'),
            internship_data.get('priority', 'Medium'),
            internship_data.get('location'),
            internship_data.get('job_url'),
            internship_data.get('salary_range'),
            internship_data.get('requirements'),
            internship_data.get('notes'),
            internship_data.get('follow_up_date')
        ))
        
        application_id = cursor.lastrowid
        
        # Add to status history
        cursor.execute('''
            INSERT INTO status_history (application_id, new_status, notes)
            VALUES (?, ?, ?)
        ''', (application_id, internship_data.get('status', 'Applied'), 'Application created'))
        
        # Add company if not exists
        cursor.execute('''
            INSERT OR IGNORE INTO companies (company_name, industry, location)
            VALUES (?, ?, ?)
        ''', (
            internship_data.get('company_name'),
            internship_data.get('industry'),
            internship_data.get('location')
        ))
        
        # Add deadline reminder if provided
        if internship_data.get('deadline'):
            cursor.execute('''
                INSERT INTO deadlines (application_id, deadline_type, deadline_date, notes)
                VALUES (?, ?, ?, ?)
            ''', (application_id, 'Application', internship_data.get('deadline'), 'Application deadline'))
        
        conn.commit()
        conn.close()
        
        return application_id
    
    def update_status(self, application_id: int, new_status: str, notes: str = "") -> bool:
        """Update application status and track history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current status
        cursor.execute('SELECT status FROM internship_applications WHERE id = ?', (application_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return False
        
        old_status = result[0]
        
        # Update status
        cursor.execute('''
            UPDATE internship_applications 
            SET status = ?, updated_at = CURRENT_TIMESTAMP, response_date = ?
            WHERE id = ?
        ''', (new_status, datetime.now().date() if new_status != 'Applied' else None, application_id))
        
        # Add to history
        cursor.execute('''
            INSERT INTO status_history (application_id, old_status, new_status, notes)
            VALUES (?, ?, ?, ?)
        ''', (application_id, old_status, new_status, notes))
        
        conn.commit()
        conn.close()
        
        return True
    
    def get_all_applications(self, status_filter: str = None) -> List[Dict]:
        """Get all internship applications with optional status filter"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status_filter:
            cursor.execute('''
                SELECT * FROM internship_applications 
                WHERE status = ? 
                ORDER BY application_date DESC
            ''', (status_filter,))
        else:
            cursor.execute('''
                SELECT * FROM internship_applications 
                ORDER BY application_date DESC
            ''')
        
        columns = [description[0] for description in cursor.description]
        applications = []
        
        for row in cursor.fetchall():
            app = dict(zip(columns, row))
            # Calculate days since application
            if app['application_date']:
                app_date = datetime.strptime(app['application_date'], '%Y-%m-%d').date()
                app['days_since_application'] = (datetime.now().date() - app_date).days
            
            # Calculate days until deadline
            if app['deadline']:
                deadline_date = datetime.strptime(app['deadline'], '%Y-%m-%d').date()
                app['days_until_deadline'] = (deadline_date - datetime.now().date()).days
            
            applications.append(app)
        
        conn.close()
        return applications
    
    def get_application_by_id(self, application_id: int) -> Optional[Dict]:
        """Get a specific application by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM internship_applications WHERE id = ?', (application_id,))
        result = cursor.fetchone()
        
        if result:
            columns = [description[0] for description in cursor.description]
            application = dict(zip(columns, result))
            
            # Get status history
            cursor.execute('''
                SELECT * FROM status_history 
                WHERE application_id = ? 
                ORDER BY change_date DESC
            ''', (application_id,))
            
            history_columns = [description[0] for description in cursor.description]
            application['status_history'] = [
                dict(zip(history_columns, row)) for row in cursor.fetchall()
            ]
            
            conn.close()
            return application
        
        conn.close()
        return None
    
    def get_analytics(self) -> Dict:
        """Get comprehensive analytics about internship applications"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        analytics = {}
        
        # Total applications
        cursor.execute('SELECT COUNT(*) FROM internship_applications')
        analytics['total_applications'] = cursor.fetchone()[0]
        
        # Status distribution
        cursor.execute('''
            SELECT status, COUNT(*) 
            FROM internship_applications 
            GROUP BY status
        ''')
        analytics['status_distribution'] = dict(cursor.fetchall())
        
        # Applications by month
        cursor.execute('''
            SELECT strftime('%Y-%m', application_date) as month, COUNT(*) 
            FROM internship_applications 
            GROUP BY month 
            ORDER BY month DESC
        ''')
        analytics['applications_by_month'] = dict(cursor.fetchall())
        
        # Response rate
        cursor.execute('''
            SELECT 
                COUNT(CASE WHEN status != 'Applied' THEN 1 END) as responses,
                COUNT(*) as total
            FROM internship_applications
        ''')
        result = cursor.fetchone()
        if result[1] > 0:
            analytics['response_rate'] = round((result[0] / result[1]) * 100, 2)
        else:
            analytics['response_rate'] = 0
        
        # Average response time
        cursor.execute('''
            SELECT AVG(julianday(response_date) - julianday(application_date)) as avg_response_time
            FROM internship_applications 
            WHERE response_date IS NOT NULL
        ''')
        result = cursor.fetchone()
        analytics['avg_response_time_days'] = round(result[0], 1) if result[0] else None
        
        # Top companies
        cursor.execute('''
            SELECT company_name, COUNT(*) as application_count
            FROM internship_applications 
            GROUP BY company_name 
            ORDER BY application_count DESC 
            LIMIT 5
        ''')
        analytics['top_companies'] = dict(cursor.fetchall())
        
        # Upcoming deadlines
        cursor.execute('''
            SELECT company_name, position_title, deadline
            FROM internship_applications 
            WHERE deadline >= date('now') 
            ORDER BY deadline ASC 
            LIMIT 5
        ''')
        columns = ['company_name', 'position_title', 'deadline']
        analytics['upcoming_deadlines'] = [
            dict(zip(columns, row)) for row in cursor.fetchall()
        ]
        
        # Success rate by priority
        cursor.execute('''
            SELECT 
                priority,
                COUNT(CASE WHEN status IN ('Interview Scheduled', 'Offer', 'Accepted') THEN 1 END) as success,
                COUNT(*) as total
            FROM internship_applications 
            GROUP BY priority
        ''')
        priority_success = {}
        for row in cursor.fetchall():
            priority, success, total = row
            priority_success[priority] = {
                'success_rate': round((success / total) * 100, 2) if total > 0 else 0,
                'total': total,
                'success': success
            }
        analytics['success_by_priority'] = priority_success
        
        conn.close()
        return analytics
    
    def get_upcoming_deadlines(self, days_ahead: int = 7) -> List[Dict]:
        """Get applications with deadlines in the next N days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT company_name, position_title, deadline, status
            FROM internship_applications 
            WHERE deadline BETWEEN date('now') AND date('now', '+' || ? || ' days')
            AND status = 'Applied'
            ORDER BY deadline ASC
        ''', (days_ahead,))
        
        columns = ['company_name', 'position_title', 'deadline', 'status']
        deadlines = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return deadlines
    
    def search_applications(self, search_term: str) -> List[Dict]:
        """Search applications by company name, position, or notes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM internship_applications 
            WHERE company_name LIKE ? OR position_title LIKE ? OR notes LIKE ?
            ORDER BY application_date DESC
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        
        columns = [description[0] for description in cursor.description]
        applications = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return applications
    
    def delete_application(self, application_id: int) -> bool:
        """Delete an internship application and its history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete from status history first
        cursor.execute('DELETE FROM status_history WHERE application_id = ?', (application_id,))
        
        # Delete from deadlines
        cursor.execute('DELETE FROM deadlines WHERE application_id = ?', (application_id,))
        
        # Delete the application
        cursor.execute('DELETE FROM internship_applications WHERE id = ?', (application_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def export_to_csv(self) -> str:
        """Export all applications to CSV format"""
        import csv
        import io
        
        applications = self.get_all_applications()
        
        output = io.StringIO()
        if applications:
            writer = csv.DictWriter(output, fieldnames=applications[0].keys())
            writer.writeheader()
            writer.writerows(applications)
        
        return output.getvalue()
    
    def get_status_options(self) -> List[str]:
        """Get available status options"""
        return [
            'Applied',
            'Under Review',
            'Phone Screen Scheduled',
            'Phone Screen Completed',
            'Interview Scheduled',
            'Interview Completed',
            'Technical Assessment',
            'Final Round',
            'Offer',
            'Accepted',
            'Rejected',
            'Withdrawn',
            'No Response'
        ]
    
    def get_priority_options(self) -> List[str]:
        """Get available priority options"""
        return ['High', 'Medium', 'Low']
    
    def find_application_by_company_and_position(self, company_name: str, position_keywords: List[str] = None) -> Optional[Dict]:
        """Find an application by company name and optional position keywords"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # First try exact company match
        cursor.execute('''
            SELECT * FROM internship_applications 
            WHERE LOWER(company_name) = LOWER(?)
            ORDER BY application_date DESC
        ''', (company_name,))
        
        result = cursor.fetchone()
        
        # If no exact match and we have position keywords, try fuzzy matching
        if not result and position_keywords:
            for keyword in position_keywords:
                cursor.execute('''
                    SELECT * FROM internship_applications 
                    WHERE LOWER(company_name) LIKE LOWER(?) OR LOWER(position_title) LIKE LOWER(?)
                    ORDER BY application_date DESC
                ''', (f'%{company_name}%', f'%{keyword}%'))
                
                result = cursor.fetchone()
                if result:
                    break
        
        if result:
            columns = [description[0] for description in cursor.description]
            application = dict(zip(columns, result))
            conn.close()
            return application
        
        conn.close()
        return None
    
    def update_from_email(self, company_name: str, email_data: Dict) -> Optional[int]:
        """Update application status based on email content"""
        # Find the relevant application
        position_keywords = email_data.get('position_keywords', [])
        application = self.find_application_by_company_and_position(company_name, position_keywords)
        
        if not application:
            return None
        
        application_id = application['id']
        email_type = email_data.get('email_type', 'unknown')
        
        # Determine new status based on email content
        new_status = self._determine_status_from_email(email_type, email_data)
        notes = f"Email update: {email_data.get('subject', 'No subject')}"
        
        # Update the application
        if new_status and new_status != application['status']:
            self.update_status(application_id, new_status, notes)
            return application_id
        
        return None
    
    def _determine_status_from_email(self, email_type: str, email_data: Dict) -> Optional[str]:
        """Determine application status based on email content"""
        email_content = email_data.get('content', '').lower()
        subject = email_data.get('subject', '').lower()
        
        # Keywords that indicate different statuses
        status_keywords = {
            'Interview Scheduled': [
                'interview', 'call', 'meeting', 'zoom', 'teams', 'video call',
                'phone screen', 'technical interview', 'final round'
            ],
            'Under Review': [
                'reviewing', 'review', 'application received', 'next steps',
                'assessment', 'coding challenge', 'test'
            ],
            'Rejected': [
                'unfortunately', 'regret', 'not selected', 'unsuccessful',
                'not moving forward', 'position has been filled'
            ],
            'Offer': [
                'offer', 'congratulations', 'pleased to offer', 'job offer',
                'welcome to', 'contract', 'salary'
            ]
        }
        
        # Check email content for status indicators
        for status, keywords in status_keywords.items():
            for keyword in keywords:
                if keyword in email_content or keyword in subject:
                    return status
        
        # If we can't determine specific status, mark as under review
        return 'Under Review'
    
    def create_application_from_email(self, email_data: Dict) -> int:
        """Create a new application from email data"""
        application_data = {
            'company_name': email_data.get('company', 'Unknown Company'),
            'position_title': email_data.get('position', 'Unknown Position'),
            'application_date': datetime.now().date(),
            'status': 'Applied',
            'priority': 'Medium',
            'notes': f"Auto-created from email: {email_data.get('subject', 'No subject')}",
            'job_url': email_data.get('job_url', ''),
            'location': email_data.get('location', '')
        }
        
        return self.add_internship(application_data)