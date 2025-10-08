#!/usr/bin/env python3
"""
🎯 Smart Interview Prep Tool - Simplified Version
This version runs without Gmail integration to avoid dependency conflicts
"""

import os
import sys
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Core imports 
from src.performance_tracker.tracker import PerformanceTracker
from src.interview_detector.detector import InterviewDetector
from src.question_banks.custom_banks import QuestionBanks
from src.company_guides.company_guides import CompanyGuides
from src.mock_interview.simulator import MockInterviewSimulator
from src.application_tracker.tracker import ApplicationTracker

class SmartInterviewPrepApp:
    """Main application class for the Smart Interview Prep Tool"""
    
    def __init__(self):
        """Initialize Flask app and components"""
        self.app = Flask(__name__)
        self.app.secret_key = 'your-secret-key-here'
        
        # Initialize components safely
        self.init_components()
        
        # Setup routes
        self.setup_routes()
        
        print("🎯 Smart Interview Prep Tool initialized successfully!")
        print("📧 Gmail integration disabled to avoid dependency conflicts")
        print("🌐 Access your tool at: http://127.0.0.1:5000")
    
    def init_components(self):
        """Initialize all application components safely"""
        print("🚀 Initializing Smart Interview Prep Tool...")
        
        try:
            # Performance tracking
            self.performance_tracker = PerformanceTracker()
            print("✅ Performance tracking ready")
            
            # Interview detection (without Gmail)
            self.interview_detector = InterviewDetector()
            print("✅ Interview detection ready")
            
            # Question banks
            self.question_banks = QuestionBanks()
            print("✅ Question banks loaded")
            
            # Company guides
            self.company_guides = CompanyGuides()
            print("✅ Company guides ready")
            
            # Mock interview simulator
            self.mock_interview = MockInterviewSimulator()
            print("✅ Mock interview simulator ready")
            
            # Application tracker with stage management
            self.application_tracker = ApplicationTracker()
            print("✅ Application tracker with stage management ready")
            
        except Exception as e:
            print(f"❌ Error initializing components: {e}")
            raise
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def home():
            """Main dashboard"""
            return render_template('index.html')
        
        @self.app.route('/analytics')
        def analytics():
            """Analytics dashboard with stage tracking"""
            return render_template('analytics.html')
        
        @self.app.route('/mock-interview')
        def mock_interview():
            """Mock interview interface"""
            return render_template('mock_interview.html')
        
        @self.app.route('/checklist')
        def checklist():
            """Preparation checklist"""
            return render_template('checklist.html')
        
        @self.app.route('/networking')
        def networking():
            """Networking tools"""
            return render_template('networking.html')
        
        # API Routes for Application Tracking
        @self.app.route('/api/applications', methods=['GET'])
        def get_applications():
            """Get all applications with stage information"""
            try:
                applications = self.application_tracker.get_all_applications()
                return jsonify({'success': True, 'applications': applications})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
        
        @self.app.route('/api/applications', methods=['POST'])
        def add_application():
            """Add new application"""
            try:
                data = request.get_json()
                app_id = self.application_tracker.add_application(
                    company=data.get('company'),
                    position=data.get('position'),
                    application_date=data.get('application_date'),
                    status=data.get('status', 'Applied'),
                    notes=data.get('notes', ''),
                    interview_stage=data.get('interview_stage', 'Applied')
                )
                return jsonify({'success': True, 'application_id': app_id})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
        
        @self.app.route('/api/applications/<int:app_id>/advance-stage', methods=['POST'])
        def advance_stage(app_id):
            """Advance application to next stage"""
            try:
                data = request.get_json()
                new_stage = data.get('new_stage')
                assessment_details = data.get('assessment_details', '')
                
                success = self.application_tracker.advance_interview_stage(
                    app_id, new_stage, assessment_details
                )
                
                if success:
                    return jsonify({'success': True, 'message': f'Advanced to {new_stage}'})
                else:
                    return jsonify({'success': False, 'error': 'Failed to advance stage'})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
        
        @self.app.route('/api/stage-analytics', methods=['GET'])
        def get_stage_analytics():
            """Get comprehensive stage analytics"""
            try:
                analytics = self.application_tracker.get_stage_analytics()
                return jsonify({'success': True, 'analytics': analytics})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
        
        @self.app.route('/api/interview-stages', methods=['GET'])
        def get_interview_stages():
            """Get available interview stages"""
            stages = [
                'Applied',
                'Online Assessment', 
                'Second Stage',
                'Technical Interview',
                'Final Interview',
                'Offer Extended',
                'Rejected'
            ]
            return jsonify({'success': True, 'stages': stages})
        
        # Performance tracking routes
        @self.app.route('/performance-stats')
        def performance_stats():
            """Get performance statistics"""
            try:
                stats = self.performance_tracker.get_performance_stats()
                return jsonify(stats)
            except Exception as e:
                return jsonify({'error': str(e)})
        
        @self.app.route('/log-interview', methods=['POST'])
        def log_interview():
            """Log interview performance"""
            try:
                data = request.get_json()
                self.performance_tracker.log_interview(
                    company=data.get('company'),
                    position=data.get('position'),
                    interview_type=data.get('interview_type'),
                    performance_score=data.get('performance_score'),
                    feedback=data.get('feedback', ''),
                    questions_asked=data.get('questions_asked', [])
                )
                return jsonify({'success': True})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
        
        # Mock interview routes
        @self.app.route('/mock-interview/start', methods=['POST'])
        def start_mock_interview():
            """Start a mock interview session"""
            try:
                data = request.get_json()
                session = self.mock_interview.start_interview(
                    company=data.get('company', 'General'),
                    position=data.get('position', 'Software Engineer'),
                    interview_type=data.get('interview_type', 'behavioral'),
                    difficulty=data.get('difficulty', 'medium')
                )
                return jsonify({'success': True, 'session': session})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
    
    def run(self, debug=True, port=5000):
        """Run the Flask application"""
        print(f"🌟 Starting Smart Interview Prep Tool on port {port}...")
        self.app.run(debug=debug, port=port, host='127.0.0.1')

# Create and run the application
if __name__ == '__main__':
    try:
        app = SmartInterviewPrepApp()
        app.run(debug=True, port=5000)
    except KeyboardInterrupt:
        print("\n👋 Smart Interview Prep Tool stopped by user")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)