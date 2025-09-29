"""
📊 Application Tracker
Comprehensive tracking system for job applications and outcomes
"""

import os
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


class ApplicationTracker:
    """Track job applications, responses, interviews, and outcomes"""
    
    def __init__(self, db_path: str = "application_tracker.db"):
        """Initialize the application tracker with database"""
        self.db_path = db_path
        self.init_database()
        print("📊 Application tracker initialized")
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Applications table with enhanced status tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                position TEXT NOT NULL,
                application_date DATE NOT NULL,
                status TEXT DEFAULT 'applied',
                interview_stage TEXT DEFAULT 'none',
                current_stage_date DATE,
                platform TEXT,
                job_url TEXT,
                salary_range TEXT,
                location TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Responses table (tracks company responses)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER,
                response_type TEXT NOT NULL,
                response_date DATE NOT NULL,
                message TEXT,
                next_step TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (application_id) REFERENCES applications (id)
            )
        ''')
        
        # Interviews table (detailed interview tracking with stages)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interview_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER,
                interview_type TEXT,
                interview_stage TEXT DEFAULT 'first_stage',
                stage_order INTEGER DEFAULT 1,
                scheduled_date DATE,
                scheduled_time TEXT,
                platform TEXT,
                interviewer_name TEXT,
                status TEXT DEFAULT 'scheduled',
                feedback TEXT,
                outcome TEXT,
                duration INTEGER,
                preparation_time INTEGER,
                assessment_details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (application_id) REFERENCES applications (id)
            )
        ''')
        
        # Application outcomes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS outcomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER,
                final_outcome TEXT NOT NULL,
                outcome_date DATE NOT NULL,
                offer_details TEXT,
                salary_offered REAL,
                rejection_reason TEXT,
                feedback TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (application_id) REFERENCES applications (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_application(self, application_data: Dict[str, Any]) -> int:
        """Log a new job application"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO applications (
                    company, position, application_date, status, platform,
                    job_url, salary_range, location, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                application_data.get('company'),
                application_data.get('position'),
                application_data.get('application_date', datetime.now().date()),
                application_data.get('status', 'applied'),
                application_data.get('platform', ''),
                application_data.get('job_url', ''),
                application_data.get('salary_range', ''),
                application_data.get('location', ''),
                application_data.get('notes', '')
            ))
            
            application_id = cursor.lastrowid
            conn.commit()
            
            print(f"✅ Application logged: {application_data.get('company')} - {application_data.get('position')}")
            return application_id
            
        except Exception as e:
            print(f"❌ Error logging application: {e}")
            return None
        finally:
            conn.close()
    
    def log_response(self, response_data: Dict[str, Any]) -> int:
        """Log a company response"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO responses (
                    application_id, response_type, response_date, message, next_step
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                response_data.get('application_id'),
                response_data.get('response_type'),
                response_data.get('response_date', datetime.now().date()),
                response_data.get('message', ''),
                response_data.get('next_step', '')
            ))
            
            response_id = cursor.lastrowid
            
            # Update application status
            if response_data.get('response_type') in ['interview_invitation', 'phone_screen']:
                cursor.execute('''
                    UPDATE applications 
                    SET status = 'interview_scheduled', updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (response_data.get('application_id'),))
            elif response_data.get('response_type') == 'rejection':
                cursor.execute('''
                    UPDATE applications 
                    SET status = 'rejected', updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (response_data.get('application_id'),))
            
            conn.commit()
            
            print(f"✅ Response logged: {response_data.get('response_type')}")
            return response_id
            
        except Exception as e:
            print(f"❌ Error logging response: {e}")
            return None
        finally:
            conn.close()
    
    def log_interview(self, interview_data: Dict[str, Any]) -> int:
        """Log an interview session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO interview_sessions (
                    application_id, interview_type, scheduled_date, scheduled_time,
                    platform, interviewer_name, status, feedback, outcome, 
                    duration, preparation_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                interview_data.get('application_id'),
                interview_data.get('interview_type'),
                interview_data.get('scheduled_date'),
                interview_data.get('scheduled_time'),
                interview_data.get('platform'),
                interview_data.get('interviewer_name'),
                interview_data.get('status', 'scheduled'),
                interview_data.get('feedback', ''),
                interview_data.get('outcome', ''),
                interview_data.get('duration', 0),
                interview_data.get('preparation_time', 0)
            ))
            
            interview_id = cursor.lastrowid
            conn.commit()
            
            print(f"✅ Interview logged: {interview_data.get('interview_type')}")
            return interview_id
            
        except Exception as e:
            print(f"❌ Error logging interview: {e}")
            return None
        finally:
            conn.close()
    
    def log_outcome(self, outcome_data: Dict[str, Any]) -> int:
        """Log final application outcome"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO outcomes (
                    application_id, final_outcome, outcome_date, offer_details,
                    salary_offered, rejection_reason, feedback
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                outcome_data.get('application_id'),
                outcome_data.get('final_outcome'),
                outcome_data.get('outcome_date', datetime.now().date()),
                outcome_data.get('offer_details', ''),
                outcome_data.get('salary_offered'),
                outcome_data.get('rejection_reason', ''),
                outcome_data.get('feedback', '')
            ))
            
            outcome_id = cursor.lastrowid
            
            # Update application status
            cursor.execute('''
                UPDATE applications 
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (outcome_data.get('final_outcome'), outcome_data.get('application_id')))
            
            conn.commit()
            
            print(f"✅ Outcome logged: {outcome_data.get('final_outcome')}")
            return outcome_id
            
        except Exception as e:
            print(f"❌ Error logging outcome: {e}")
            return None
        finally:
            conn.close()
    
    def get_application_stats(self) -> Dict[str, Any]:
        """Get comprehensive application statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Total applications
            cursor.execute('SELECT COUNT(*) FROM applications')
            total_applications = cursor.fetchone()[0]
            
            # Applications by status
            cursor.execute('''
                SELECT status, COUNT(*) 
                FROM applications 
                GROUP BY status
            ''')
            status_counts = dict(cursor.fetchall())
            
            # Response rate
            cursor.execute('SELECT COUNT(*) FROM responses')
            total_responses = cursor.fetchone()[0]
            response_rate = (total_responses / total_applications * 100) if total_applications > 0 else 0
            
            # Interview rate
            cursor.execute('SELECT COUNT(DISTINCT application_id) FROM interview_sessions')
            interviews_scheduled = cursor.fetchone()[0]
            interview_rate = (interviews_scheduled / total_applications * 100) if total_applications > 0 else 0
            
            # Success rate (offers)
            offers = status_counts.get('offer', 0)
            success_rate = (offers / total_applications * 100) if total_applications > 0 else 0
            
            # Rejection rate
            rejections = status_counts.get('rejected', 0)
            rejection_rate = (rejections / total_applications * 100) if total_applications > 0 else 0
            
            # Recent activity (last 30 days)
            thirty_days_ago = (datetime.now() - timedelta(days=30)).date()
            cursor.execute('''
                SELECT COUNT(*) FROM applications 
                WHERE application_date >= ?
            ''', (thirty_days_ago,))
            recent_applications = cursor.fetchone()[0]
            
            # Top companies applied to
            cursor.execute('''
                SELECT company, COUNT(*) as count
                FROM applications 
                GROUP BY company 
                ORDER BY count DESC 
                LIMIT 10
            ''')
            top_companies = cursor.fetchall()
            
            # Monthly application trend
            cursor.execute('''
                SELECT strftime('%Y-%m', application_date) as month, COUNT(*) as count
                FROM applications 
                WHERE application_date >= date('now', '-12 months')
                GROUP BY month 
                ORDER BY month
            ''')
            monthly_trend = cursor.fetchall()
            
            return {
                'total_applications': total_applications,
                'status_breakdown': status_counts,
                'response_rate': round(response_rate, 1),
                'interview_rate': round(interview_rate, 1),
                'success_rate': round(success_rate, 1),
                'rejection_rate': round(rejection_rate, 1),
                'recent_applications': recent_applications,
                'top_companies': top_companies,
                'monthly_trend': monthly_trend,
                'total_responses': total_responses,
                'interviews_scheduled': interviews_scheduled
            }
            
        except Exception as e:
            print(f"❌ Error getting application stats: {e}")
            return {}
        finally:
            conn.close()
    
    def get_applications_list(self, limit: int = 50, status: str = None) -> List[Dict[str, Any]]:
        """Get list of applications with optional filtering"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            if status:
                cursor.execute('''
                    SELECT * FROM applications 
                    WHERE status = ? 
                    ORDER BY application_date DESC 
                    LIMIT ?
                ''', (status, limit))
            else:
                cursor.execute('''
                    SELECT * FROM applications 
                    ORDER BY application_date DESC 
                    LIMIT ?
                ''', (limit,))
                
            columns = [description[0] for description in cursor.description]
            applications = []
            
            for row in cursor.fetchall():
                app_dict = dict(zip(columns, row))
                applications.append(app_dict)
            
            return applications
            
        except Exception as e:
            print(f"❌ Error getting applications list: {e}")
            return []
        finally:
            conn.close()
    
    def update_application_status(self, application_id: int, new_status: str) -> bool:
        """Update application status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE applications 
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (new_status, application_id))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"❌ Error updating application status: {e}")
            return False
        finally:
            conn.close()
    
    def get_interview_analytics(self) -> Dict[str, Any]:
        """Get interview-specific analytics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Interview outcomes
            cursor.execute('''
                SELECT outcome, COUNT(*) 
                FROM interview_sessions 
                WHERE outcome IS NOT NULL AND outcome != ''
                GROUP BY outcome
            ''')
            interview_outcomes = dict(cursor.fetchall())
            
            # Average interview duration
            cursor.execute('''
                SELECT AVG(duration) 
                FROM interview_sessions 
                WHERE duration > 0
            ''')
            avg_duration = cursor.fetchone()[0] or 0
            
            # Interview types distribution
            cursor.execute('''
                SELECT interview_type, COUNT(*) 
                FROM interview_sessions 
                GROUP BY interview_type
            ''')
            interview_types = dict(cursor.fetchall())
            
            # Success rate by interview type
            cursor.execute('''
                SELECT interview_type, 
                       SUM(CASE WHEN outcome = 'passed' THEN 1 ELSE 0 END) as passed,
                       COUNT(*) as total
                FROM interview_sessions 
                WHERE outcome IS NOT NULL AND outcome != ''
                GROUP BY interview_type
            ''')
            
            success_by_type = {}
            for row in cursor.fetchall():
                interview_type, passed, total = row
                success_rate = (passed / total * 100) if total > 0 else 0
                success_by_type[interview_type] = {
                    'success_rate': round(success_rate, 1),
                    'total': total,
                    'passed': passed
                }
            
            return {
                'interview_outcomes': interview_outcomes,
                'average_duration': round(avg_duration, 1),
                'interview_types': interview_types,
                'success_by_type': success_by_type
            }
            
        except Exception as e:
            print(f"❌ Error getting interview analytics: {e}")
            return {}
        finally:
            conn.close()
    
    def get_interview_stages(self) -> Dict[str, str]:
        """Get available interview stages"""
        return {
            'applied': 'Application Submitted',
            'application_review': 'Application Under Review',
            'online_assessment': 'Online Assessment',
            'phone_screening': 'Phone Screening',
            'first_interview': 'First Round Interview',
            'technical_interview': 'Technical Interview', 
            'second_stage': 'Second Stage Interview',
            'final_interview': 'Final Round Interview',
            'reference_check': 'Reference Check',
            'offer_pending': 'Offer Pending',
            'offer': 'Offer Received',
            'rejected': 'Rejected'
        }
    
    def advance_interview_stage(self, application_id: int, new_stage: str, stage_details: Dict[str, Any] = None) -> bool:
        """Advance application to next interview stage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Update application status and stage
            cursor.execute('''
                UPDATE applications 
                SET status = ?, interview_stage = ?, current_stage_date = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (new_stage, new_stage, datetime.now().date(), application_id))
            
            # Log interview session if stage details provided
            if stage_details:
                self._log_interview_stage(cursor, application_id, new_stage, stage_details)
            
            conn.commit()
            print(f"✅ Application {application_id} advanced to {new_stage}")
            return True
            
        except Exception as e:
            print(f"❌ Error advancing interview stage: {e}")
            return False
        finally:
            conn.close()
    
    def _log_interview_stage(self, cursor, application_id: int, stage: str, details: Dict[str, Any]):
        """Internal method to log interview stage details"""
        stage_order_map = {
            'online_assessment': 1,
            'phone_screening': 2,
            'first_interview': 3,
            'technical_interview': 4,
            'second_stage': 5,
            'final_interview': 6
        }
        
        cursor.execute('''
            INSERT INTO interview_sessions (
                application_id, interview_type, interview_stage, stage_order,
                scheduled_date, scheduled_time, platform, interviewer_name,
                status, assessment_details
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            application_id,
            details.get('interview_type', stage),
            stage,
            stage_order_map.get(stage, 0),
            details.get('scheduled_date'),
            details.get('scheduled_time'),
            details.get('platform', ''),
            details.get('interviewer_name', ''),
            details.get('status', 'scheduled'),
            details.get('assessment_details', '')
        ))
    
    def get_application_with_stages(self, application_id: int) -> Dict[str, Any]:
        """Get application details with all interview stages"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get application details
            cursor.execute('SELECT * FROM applications WHERE id = ?', (application_id,))
            app_row = cursor.fetchone()
            
            if not app_row:
                return {}
            
            # Convert to dict
            columns = [description[0] for description in cursor.description]
            application = dict(zip(columns, app_row))
            
            # Get all interview stages for this application
            cursor.execute('''
                SELECT * FROM interview_sessions 
                WHERE application_id = ? 
                ORDER BY stage_order, created_at
            ''', (application_id,))
            
            stage_columns = [description[0] for description in cursor.description]
            stages = []
            for row in cursor.fetchall():
                stage_dict = dict(zip(stage_columns, row))
                stages.append(stage_dict)
            
            application['interview_stages'] = stages
            return application
            
        except Exception as e:
            print(f"❌ Error getting application with stages: {e}")
            return {}
        finally:
            conn.close()
    
    def get_stage_analytics(self) -> Dict[str, Any]:
        """Get analytics for interview stage progression"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Stage distribution
            cursor.execute('''
                SELECT interview_stage, COUNT(*) 
                FROM applications 
                WHERE interview_stage IS NOT NULL
                GROUP BY interview_stage
            ''')
            stage_distribution = dict(cursor.fetchall())
            
            # Average time in each stage
            cursor.execute('''
                SELECT 
                    interview_stage,
                    AVG(julianday(updated_at) - julianday(current_stage_date)) as avg_days
                FROM applications 
                WHERE interview_stage IS NOT NULL AND current_stage_date IS NOT NULL
                GROUP BY interview_stage
            ''')
            
            stage_durations = {}
            for row in cursor.fetchall():
                stage, avg_days = row
                stage_durations[stage] = round(avg_days or 0, 1)
            
            # Stage progression success rates
            cursor.execute('''
                SELECT 
                    interview_stage,
                    COUNT(*) as total,
                    SUM(CASE WHEN status NOT IN ('rejected') THEN 1 ELSE 0 END) as active
                FROM applications
                WHERE interview_stage IS NOT NULL
                GROUP BY interview_stage
            ''')
            
            stage_success = {}
            for row in cursor.fetchall():
                stage, total, active = row
                success_rate = (active / total * 100) if total > 0 else 0
                stage_success[stage] = {
                    'total': total,
                    'active': active,
                    'success_rate': round(success_rate, 1)
                }
            
            return {
                'stage_distribution': stage_distribution,
                'stage_durations': stage_durations,
                'stage_success_rates': stage_success
            }
            
        except Exception as e:
            print(f"❌ Error getting stage analytics: {e}")
            return {}
        finally:
            conn.close()