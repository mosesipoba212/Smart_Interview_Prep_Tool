"""
Performance Tracker Module
Tracks interview performance, preparation effectiveness, and provides analytics
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import statistics

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    ANALYTICS_AVAILABLE = True
except ImportError:
    ANALYTICS_AVAILABLE = False
    print("⚠️  Analytics packages not available. Using basic tracking.")

class PerformanceTracker:
    """Tracks and analyzes interview performance across multiple interviews"""
    
    def __init__(self, db_path: str = "interview_performance.db"):
        self.db_path = db_path
        self.init_database()
        print("📊 Performance tracker initialized")
    
    def init_database(self):
        """Initialize SQLite database for storing performance data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create interviews table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                position TEXT NOT NULL,
                interview_type TEXT NOT NULL,
                interview_date TEXT NOT NULL,
                outcome TEXT,
                overall_rating INTEGER,
                preparation_hours REAL,
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        # Create questions_performance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS question_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interview_id INTEGER,
                question_text TEXT NOT NULL,
                question_type TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                confidence_rating INTEGER,
                time_taken INTEGER,
                notes TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (interview_id) REFERENCES interviews (id)
            )
        ''')
        
        # Create preparation_sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preparation_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interview_id INTEGER,
                session_date TEXT NOT NULL,
                duration_minutes INTEGER NOT NULL,
                focus_area TEXT NOT NULL,
                effectiveness_rating INTEGER,
                topics_covered TEXT,
                notes TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (interview_id) REFERENCES interviews (id)
            )
        ''')
        
        # Create skills_assessment table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skill_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interview_id INTEGER,
                skill_name TEXT NOT NULL,
                skill_category TEXT NOT NULL,
                confidence_level INTEGER NOT NULL,
                assessment_date TEXT NOT NULL,
                notes TEXT,
                FOREIGN KEY (interview_id) REFERENCES interviews (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_interview(self, interview_data: Dict[str, Any]) -> int:
        """Log a completed interview"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO interviews (
                company, position, interview_type, interview_date,
                outcome, overall_rating, preparation_hours, notes,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            interview_data.get('company', ''),
            interview_data.get('position', ''),
            interview_data.get('interview_type', ''),
            interview_data.get('interview_date', ''),
            interview_data.get('outcome', ''),
            interview_data.get('overall_rating', 0),
            interview_data.get('preparation_hours', 0),
            interview_data.get('notes', ''),
            now,
            now
        ))
        
        interview_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"📝 Logged interview: {interview_data.get('company')} - {interview_data.get('position')}")
        return interview_id
    
    def log_question_performance(self, interview_id: int, question_data: Dict[str, Any]) -> bool:
        """Log performance on individual questions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO question_performance (
                interview_id, question_text, question_type, difficulty,
                confidence_rating, time_taken, notes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            interview_id,
            question_data.get('question_text', ''),
            question_data.get('question_type', ''),
            question_data.get('difficulty', ''),
            question_data.get('confidence_rating', 0),
            question_data.get('time_taken', 0),
            question_data.get('notes', ''),
            now
        ))
        
        conn.commit()
        conn.close()
        return True
    
    def log_preparation_session(self, session_data: Dict[str, Any]) -> bool:
        """Log a preparation session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO preparation_sessions (
                interview_id, session_date, duration_minutes, focus_area,
                effectiveness_rating, topics_covered, notes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_data.get('interview_id'),
            session_data.get('session_date', now),
            session_data.get('duration_minutes', 0),
            session_data.get('focus_area', ''),
            session_data.get('effectiveness_rating', 0),
            json.dumps(session_data.get('topics_covered', [])),
            session_data.get('notes', ''),
            now
        ))
        
        conn.commit()
        conn.close()
        
        print(f"📚 Logged prep session: {session_data.get('focus_area')}")
        return True
    
    def log_performance(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main method to log interview performance data"""
        try:
            # Log the interview
            interview_id = self.log_interview(performance_data.get('interview', {}))
            
            # Log question performances
            questions = performance_data.get('questions', [])
            for question in questions:
                self.log_question_performance(interview_id, question)
            
            # Log preparation sessions
            prep_sessions = performance_data.get('preparation_sessions', [])
            for session in prep_sessions:
                session['interview_id'] = interview_id
                self.log_preparation_session(session)
            
            return {
                'success': True,
                'interview_id': interview_id,
                'message': 'Performance data logged successfully'
            }
            
        except Exception as e:
            print(f"❌ Error logging performance: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics"""
        conn = sqlite3.connect(self.db_path)
        
        try:
            # Overall interview stats
            interview_stats = self.get_interview_stats(conn)
            
            # Question performance stats
            question_stats = self.get_question_stats(conn)
            
            # Preparation effectiveness
            prep_stats = self.get_preparation_stats(conn)
            
            # Trend analysis
            trends = self.get_performance_trends(conn)
            
            # Recommendations
            recommendations = self.generate_recommendations(conn)
            
            return {
                'interview_stats': interview_stats,
                'question_performance': question_stats,
                'preparation_effectiveness': prep_stats,
                'trends': trends,
                'recommendations': recommendations,
                'last_updated': datetime.now().isoformat()
            }
            
        finally:
            conn.close()
    
    def get_interview_stats(self, conn: sqlite3.Connection) -> Dict[str, Any]:
        """Get overall interview statistics"""
        cursor = conn.cursor()
        
        # Total interviews
        cursor.execute("SELECT COUNT(*) FROM interviews")
        total_interviews = cursor.fetchone()[0]
        
        # Success rate
        cursor.execute("SELECT COUNT(*) FROM interviews WHERE outcome = 'offer'")
        offers = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM interviews WHERE outcome IN ('offer', 'rejection')")
        completed = cursor.fetchone()[0]
        
        success_rate = (offers / completed * 100) if completed > 0 else 0
        
        # Average overall rating
        cursor.execute("SELECT AVG(overall_rating) FROM interviews WHERE overall_rating > 0")
        avg_rating_result = cursor.fetchone()[0]
        avg_rating = avg_rating_result if avg_rating_result else 0
        
        # Interview types breakdown
        cursor.execute("SELECT interview_type, COUNT(*) FROM interviews GROUP BY interview_type")
        interview_types = dict(cursor.fetchall())
        
        # Recent performance (last 30 days)
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        cursor.execute("SELECT COUNT(*) FROM interviews WHERE created_at > ?", (thirty_days_ago,))
        recent_interviews = cursor.fetchone()[0]
        
        return {
            'total_interviews': total_interviews,
            'success_rate': round(success_rate, 1),
            'average_rating': round(avg_rating, 1),
            'interview_types': interview_types,
            'recent_interviews': recent_interviews,
            'offers_received': offers
        }
    
    def get_question_stats(self, conn: sqlite3.Connection) -> Dict[str, Any]:
        """Get question performance statistics"""
        cursor = conn.cursor()
        
        # Average confidence by question type
        cursor.execute('''
            SELECT question_type, AVG(confidence_rating), COUNT(*)
            FROM question_performance
            WHERE confidence_rating > 0
            GROUP BY question_type
        ''')
        confidence_by_type = {row[0]: {'avg_confidence': round(row[1], 1), 'count': row[2]} 
                            for row in cursor.fetchall()}
        
        # Difficulty performance
        cursor.execute('''
            SELECT difficulty, AVG(confidence_rating), AVG(time_taken)
            FROM question_performance
            WHERE confidence_rating > 0
            GROUP BY difficulty
        ''')
        difficulty_performance = {row[0]: {'avg_confidence': round(row[1], 1), 'avg_time': round(row[2], 1)} 
                                for row in cursor.fetchall()}
        
        # Improvement areas (low confidence questions)
        cursor.execute('''
            SELECT question_type, AVG(confidence_rating)
            FROM question_performance
            WHERE confidence_rating > 0
            GROUP BY question_type
            HAVING AVG(confidence_rating) < 6
            ORDER BY AVG(confidence_rating)
        ''')
        improvement_areas = [row[0] for row in cursor.fetchall()]
        
        return {
            'confidence_by_type': confidence_by_type,
            'difficulty_performance': difficulty_performance,
            'improvement_areas': improvement_areas
        }
    
    def get_preparation_stats(self, conn: sqlite3.Connection) -> Dict[str, Any]:
        """Get preparation effectiveness statistics"""
        cursor = conn.cursor()
        
        # Total preparation time
        cursor.execute("SELECT SUM(duration_minutes) FROM preparation_sessions")
        total_prep_time = cursor.fetchone()[0] or 0
        
        # Average session effectiveness
        cursor.execute("SELECT AVG(effectiveness_rating) FROM preparation_sessions WHERE effectiveness_rating > 0")
        avg_effectiveness = cursor.fetchone()[0] or 0
        
        # Preparation vs performance correlation
        cursor.execute('''
            SELECT i.overall_rating, SUM(ps.duration_minutes) as total_prep
            FROM interviews i
            LEFT JOIN preparation_sessions ps ON i.id = ps.interview_id
            WHERE i.overall_rating > 0
            GROUP BY i.id, i.overall_rating
        ''')
        prep_performance_data = cursor.fetchall()
        
        # Calculate correlation if we have enough data
        correlation = 0
        if len(prep_performance_data) > 3:
            ratings = [row[0] for row in prep_performance_data]
            prep_times = [row[1] or 0 for row in prep_performance_data]
            if len(set(prep_times)) > 1:  # Avoid division by zero
                correlation = self.calculate_correlation(prep_times, ratings)
        
        # Most effective focus areas
        cursor.execute('''
            SELECT focus_area, AVG(effectiveness_rating), COUNT(*)
            FROM preparation_sessions
            WHERE effectiveness_rating > 0
            GROUP BY focus_area
            ORDER BY AVG(effectiveness_rating) DESC
            LIMIT 5
        ''')
        effective_focus_areas = [{'area': row[0], 'effectiveness': round(row[1], 1), 'sessions': row[2]}
                               for row in cursor.fetchall()]
        
        return {
            'total_prep_time_hours': round(total_prep_time / 60, 1),
            'average_effectiveness': round(avg_effectiveness, 1),
            'prep_performance_correlation': round(correlation, 2),
            'effective_focus_areas': effective_focus_areas
        }
    
    def get_performance_trends(self, conn: sqlite3.Connection) -> Dict[str, Any]:
        """Analyze performance trends over time"""
        cursor = conn.cursor()
        
        # Performance over time (monthly)
        cursor.execute('''
            SELECT strftime('%Y-%m', interview_date) as month,
                   AVG(overall_rating) as avg_rating,
                   COUNT(*) as interview_count
            FROM interviews
            WHERE overall_rating > 0
            GROUP BY month
            ORDER BY month
        ''')
        monthly_performance = [{'month': row[0], 'avg_rating': round(row[1], 1), 'count': row[2]}
                             for row in cursor.fetchall()]
        
        # Confidence trends by question type
        cursor.execute('''
            SELECT question_type,
                   strftime('%Y-%m', qp.created_at) as month,
                   AVG(confidence_rating) as avg_confidence
            FROM question_performance qp
            WHERE confidence_rating > 0
            GROUP BY question_type, month
            ORDER BY question_type, month
        ''')
        confidence_trends = {}
        for row in cursor.fetchall():
            q_type = row[0]
            if q_type not in confidence_trends:
                confidence_trends[q_type] = []
            confidence_trends[q_type].append({
                'month': row[1],
                'avg_confidence': round(row[2], 1)
            })
        
        return {
            'monthly_performance': monthly_performance,
            'confidence_trends': confidence_trends
        }
    
    def generate_recommendations(self, conn: sqlite3.Connection) -> List[Dict[str, Any]]:
        """Generate personalized recommendations based on performance data"""
        recommendations = []
        cursor = conn.cursor()
        
        # Check for low-performing question types
        cursor.execute('''
            SELECT question_type, AVG(confidence_rating) as avg_conf
            FROM question_performance
            WHERE confidence_rating > 0
            GROUP BY question_type
            HAVING AVG(confidence_rating) < 6
            ORDER BY avg_conf
            LIMIT 3
        ''')
        
        for row in cursor.fetchall():
            recommendations.append({
                'type': 'skill_improvement',
                'priority': 'high',
                'title': f"Focus on {row[0]} questions",
                'description': f"Your average confidence in {row[0]} questions is {row[1]:.1f}/10. Consider dedicated practice.",
                'suggested_action': f"Schedule 2-3 focused practice sessions on {row[0]} topics"
            })
        
        # Check preparation consistency
        cursor.execute('''
            SELECT COUNT(*) as session_count,
                   AVG(duration_minutes) as avg_duration
            FROM preparation_sessions
            WHERE created_at > date('now', '-30 days')
        ''')
        prep_data = cursor.fetchone()
        
        if prep_data[0] < 5:  # Less than 5 sessions in last 30 days
            recommendations.append({
                'type': 'preparation_consistency',
                'priority': 'medium',
                'title': "Increase preparation frequency",
                'description': "You've had fewer than 5 preparation sessions in the last 30 days.",
                'suggested_action': "Aim for 2-3 preparation sessions per week for better consistency"
            })
        
        # Check for interview outcome patterns
        cursor.execute('''
            SELECT interview_type, 
                   SUM(CASE WHEN outcome = 'offer' THEN 1 ELSE 0 END) as offers,
                   COUNT(*) as total
            FROM interviews
            WHERE outcome IN ('offer', 'rejection')
            GROUP BY interview_type
        ''')
        
        for row in cursor.fetchall():
            success_rate = (row[1] / row[2]) * 100 if row[2] > 0 else 0
            if success_rate < 30 and row[2] >= 3:  # Low success rate with sufficient data
                recommendations.append({
                    'type': 'interview_strategy',
                    'priority': 'high',
                    'title': f"Improve {row[0]} interview strategy",
                    'description': f"Your success rate for {row[0]} interviews is {success_rate:.1f}%",
                    'suggested_action': f"Consider mock {row[0]} interviews and targeted preparation"
                })
        
        return recommendations
    
    def calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient"""
        if len(x) != len(y) or len(x) < 2:
            return 0
        
        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
        sum_sq_x = sum((x[i] - mean_x) ** 2 for i in range(len(x)))
        sum_sq_y = sum((y[i] - mean_y) ** 2 for i in range(len(y)))
        
        denominator = (sum_sq_x * sum_sq_y) ** 0.5
        
        if denominator == 0:
            return 0
        
        return numerator / denominator
    
    def export_performance_data(self, format_type: str = 'json') -> str:
        """Export performance data for external analysis"""
        stats = self.get_performance_stats()
        
        if format_type == 'json':
            filename = f"performance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(stats, f, indent=2)
            return filename
        
        elif format_type == 'csv' and ANALYTICS_AVAILABLE:
            # Export to CSV using pandas
            conn = sqlite3.connect(self.db_path)
            
            # Export interviews
            interviews_df = pd.read_sql_query("SELECT * FROM interviews", conn)
            filename = f"interviews_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            interviews_df.to_csv(filename, index=False)
            
            conn.close()
            return filename
        
        return "export_failed"
    
    def generate_performance_charts(self) -> List[str]:
        """Generate performance visualization charts"""
        if not ANALYTICS_AVAILABLE:
            print("⚠️  Analytics packages not available for chart generation")
            return []
        
        conn = sqlite3.connect(self.db_path)
        chart_files = []
        
        try:
            # Performance over time chart
            df = pd.read_sql_query('''
                SELECT interview_date, overall_rating, interview_type
                FROM interviews
                WHERE overall_rating > 0
                ORDER BY interview_date
            ''', conn)
            
            if not df.empty:
                plt.figure(figsize=(12, 6))
                
                # Convert date strings to datetime
                df['interview_date'] = pd.to_datetime(df['interview_date'])
                
                # Plot performance over time
                plt.subplot(1, 2, 1)
                plt.plot(df['interview_date'], df['overall_rating'], marker='o')
                plt.title('Interview Performance Over Time')
                plt.xlabel('Date')
                plt.ylabel('Overall Rating')
                plt.xticks(rotation=45)
                
                # Performance by interview type
                plt.subplot(1, 2, 2)
                type_performance = df.groupby('interview_type')['overall_rating'].mean()
                type_performance.plot(kind='bar')
                plt.title('Average Performance by Interview Type')
                plt.xlabel('Interview Type')
                plt.ylabel('Average Rating')
                plt.xticks(rotation=45)
                
                plt.tight_layout()
                chart_file = f"performance_charts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                plt.savefig(chart_file)
                plt.close()
                chart_files.append(chart_file)
            
        except Exception as e:
            print(f"❌ Error generating charts: {e}")
        finally:
            conn.close()
        
        return chart_files
