#!/usr/bin/env python3
"""
Smart Interview Prep Tool - Enhanced Version with Comprehensive Error Handling
Main application entry point
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import enhanced error handling
from src.utils.error_handler import ErrorCodes, log_error, check_system_health, validate_config

try:
    from src.email_parser.simplified_gmail_service import SimplifiedGmailService
    from src.ai_engine.question_generator import QuestionGenerator
    from src.performance_tracker.tracker import PerformanceTracker
    from src.interview_detector.detector import InterviewDetector
    from src.question_banks.custom_banks import QuestionBanks
    from src.company_guides.company_guides import CompanyGuides
    from src.mock_interview.simulator import MockInterviewSimulator
    from src.salary_negotiation.salary_tools import SalaryNegotiationTools
    from src.resume_analyzer.analyzer import ResumeAnalyzer
    from src.skills_assessment.skills_tool import SkillsAssessmentTool
    from src.follow_up.follow_up_manager import FollowUpManager
    from src.analytics.analytics_dashboard import AnalyticsDashboard
    from src.networking.networking_tools import NetworkingTools
    from src.checklist.preparation_checklist import PreparationChecklist
except ImportError as e:
    log_error(ErrorCodes.DEPENDENCY_MISSING, f"Failed to import required modules: {e}", e)
    sys.exit(1)

# Load environment variables
load_dotenv()

app = Flask(__name__)

class InterviewPrepApp:
    def __init__(self):
        # Check system health first
        health = check_system_health()
        if health['status'] == 'unhealthy':
            print(f"⚠️ System health issues detected: {health['errors']}")
            for error in health['errors']:
                log_error(ErrorCodes.SYSTEM_STARTUP_FAILED, error)
        
        # Validate configuration
        config = validate_config()
        if not config['valid']:
            print(f"⚠️ Configuration issues detected: {config['issues']}")
            for issue in config['issues']:
                log_error(ErrorCodes.CONFIG_FILE_MISSING, issue)
        
        try:
            # Use simplified Gmail service (no OAuth required)
            print("📧 Initializing simplified Gmail service...")
            self.gmail_service = SimplifiedGmailService()
        except Exception as e:
            log_error(ErrorCodes.GMAIL_AUTH_FAILED, "Failed to initialize Gmail service", e)
            self.gmail_service = None
            
        try:
            self.question_generator = QuestionGenerator()
        except Exception as e:
            log_error(ErrorCodes.QUESTION_GENERATION_FAILED, "Failed to initialize question generator", e)
            self.question_generator = None
            
        try:
            self.performance_tracker = PerformanceTracker()
        except Exception as e:
            log_error(ErrorCodes.DATABASE_CONNECTION_FAILED, "Failed to initialize performance tracker", e)
            self.performance_tracker = None
            
        try:
            self.interview_detector = InterviewDetector()
            self.question_banks = QuestionBanks()
            self.company_guides = CompanyGuides()
            self.mock_interview = MockInterviewSimulator()
            self.salary_tools = SalaryNegotiationTools()
            self.resume_analyzer = ResumeAnalyzer()
            self.skills_tool = SkillsAssessmentTool()
            self.follow_up_manager = FollowUpManager()
            self.analytics_dashboard = AnalyticsDashboard()
            self.networking_tools = NetworkingTools()
            self.checklist = PreparationChecklist()
        except Exception as e:
            log_error(ErrorCodes.SYSTEM_STARTUP_FAILED, "Failed to initialize some components", e)

    def initialize_services(self):
        """Initialize all services with error handling"""
        try:
            print("🚀 Starting Smart Interview Prep Tool...")
            
            # Check each service
            services_status = {
                'Gmail integration': self.gmail_service is not None,
                'AI question generator': self.question_generator is not None,
                'Performance tracking': self.performance_tracker is not None,
                'Resume analyzer': hasattr(self, 'resume_analyzer'),
                'Skills assessment': hasattr(self, 'skills_tool'),
                'Follow-up management': hasattr(self, 'follow_up_manager'),
                'Analytics dashboard': hasattr(self, 'analytics_dashboard'),
                'Networking tools': hasattr(self, 'networking_tools'),
                'Preparation checklists': hasattr(self, 'checklist')
            }
            
            for service, status in services_status.items():
                if status:
                    print(f"✅ {service} ready")
                else:
                    print(f"❌ {service} failed to initialize")
                    
        except Exception as e:
            log_error(ErrorCodes.SYSTEM_STARTUP_FAILED, "Service initialization failed", e)

# Initialize the app
prep_app = InterviewPrepApp()

@app.route('/')
def home():
    """Home page"""
    # Get performance stats
    try:
        stats = prep_app.performance_tracker.get_performance_stats()
    except Exception as e:
        print(f"⚠️ Error getting performance stats: {e}")
        stats = {
            'total_interviews': 0,
            'average_rating': 0,
            'recent_interviews': []
        }
    
    return render_template('index.html', 
                         stats=stats)

@app.route('/performance-stats')
def performance_stats():
    """Get performance statistics"""
    try:
        stats = prep_app.performance_tracker.get_performance_stats()
        return jsonify(stats)
    except Exception as e:
        print(f"❌ Error getting performance stats: {e}")
        return jsonify({
            'total_interviews': 0,
            'average_rating': 0,
            'recent_interviews': []
        })

@app.route('/scan-emails', methods=['POST'])
def scan_emails():
    """Scan emails for interview opportunities with enhanced error handling"""
    try:
        if not prep_app.gmail_service:
            error_info = log_error(ErrorCodes.GMAIL_AUTH_FAILED, "Gmail service not initialized")
            return jsonify({
                'success': False,
                'error': 'Gmail service unavailable',
                'error_code': error_info['error_code'],
                'suggestions': error_info['suggestions'],
                'emails': [],
                'count': 0
            })
        
        emails = prep_app.gmail_service.scan_for_interviews()
        print(f"📧 Found {len(emails)} potential interview emails")
        
        return jsonify({
            'success': True,
            'emails': emails,
            'count': len(emails),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        error_info = log_error(ErrorCodes.EMAIL_FETCH_FAILED, f"Error scanning emails: {e}", e)
        return jsonify({
            'success': False,
            'error': str(e),
            'error_code': error_info['error_code'],
            'suggestions': error_info['suggestions'],
            'emails': [],
            'count': 0
        })

@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    """Generate AI-powered interview questions with enhanced error handling"""
    try:
        data = request.get_json()
        if not data:
            error_info = log_error(ErrorCodes.INVALID_INPUT_FORMAT, "No JSON data provided")
            return jsonify({
                'success': False,
                'error': 'Invalid request format',
                'error_code': error_info['error_code'],
                'suggestions': error_info['suggestions'],
                'questions': []
            })
        
        # Validate required fields
        company = data.get('company', '')
        position = data.get('position', '')
        interview_type = data.get('interview_type', 'general')
        
        if not prep_app.question_generator:
            error_info = log_error(ErrorCodes.QUESTION_GENERATION_FAILED, "Question generator not initialized")
            return jsonify({
                'success': False,
                'error': 'Question generator unavailable',
                'error_code': error_info['error_code'],
                'suggestions': error_info['suggestions'],
                'questions': []
            })
        
        questions = prep_app.question_generator.generate_questions(
            company=company,
            position=position,
            interview_type=interview_type
        )
        
        return jsonify({
            'success': True,
            'questions': questions,
            'metadata': {
                'company': company,
                'position': position,
                'interview_type': interview_type,
                'generated_at': datetime.now().isoformat(),
                'question_count': len(questions)
            }
        })
        
    except Exception as e:
        error_info = log_error(ErrorCodes.QUESTION_GENERATION_FAILED, f"AI question generation failed: {e}", e)
        return jsonify({
            'success': False,
            'error': str(e),
            'error_code': error_info['error_code'],
            'suggestions': error_info['suggestions'],
            'questions': []
        })

@app.route('/question-banks/industry/<industry>')
def get_industry_questions(industry):
    """Get questions by industry"""
    try:
        question_type = request.args.get('type', 'technical')
        count = int(request.args.get('count', 5))
        
        questions = prep_app.question_banks.get_questions_by_industry(
            industry=industry,
            question_type=question_type,
            count=count
        )
        
        return jsonify({
            'success': True,
            'questions': questions,
            'industry': industry,
            'type': question_type
        })
    except Exception as e:
        print(f"❌ Error getting industry questions: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'questions': []
        })

@app.route('/question-banks/role/<role>')
def get_role_questions(role):
    """Get questions by role"""
    try:
        count = int(request.args.get('count', 5))
        
        questions = prep_app.question_banks.get_questions_by_role(
            role=role,
            count=count
        )
        
        return jsonify({
            'success': True,
            'questions': questions,
            'role': role
        })
    except Exception as e:
        print(f"❌ Error getting role questions: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'questions': []
        })

@app.route('/log-interview', methods=['POST'])
def log_interview():
    """Log interview performance"""
    try:
        data = request.get_json()
        
        # Prepare interview data in the format expected by the tracker
        interview_data = {
            'company': data.get('company', ''),
            'position': data.get('position', ''),
            'interview_type': data.get('interview_type', 'general'),
            'interview_date': data.get('interview_date', datetime.now().isoformat()),
            'outcome': data.get('outcome', 'pending'),
            'overall_rating': data.get('overall_rating', 0),
            'preparation_hours': data.get('preparation_hours', 0),
            'notes': data.get('notes', '')
        }
        
        result = prep_app.performance_tracker.log_interview(interview_data)
        
        return jsonify({
            'success': True,
            'message': 'Interview logged successfully',
            'id': result
        })
    except Exception as e:
        print(f"❌ Error logging interview: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/company-guides/<company>')
def get_company_guide(company):
    """Get company-specific interview guide"""
    try:
        guide = prep_app.company_guides.get_company_guide(company)
        return jsonify({
            'success': True,
            'guide': guide
        })
    except Exception as e:
        print(f"❌ Error getting company guide: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'guide': {}
        })

@app.route('/study-resources')
def study_resources():
    """Study resources page"""
    return render_template('study_resources.html')

@app.route('/analytics')
def analytics():
    """Analytics dashboard page"""
    return render_template('analytics.html')

@app.route('/networking')
def networking():
    """Networking tools page"""
    return render_template('networking.html')

@app.route('/checklist')
def checklist():
    """Preparation checklist page"""
    return render_template('checklist.html')

@app.route('/diagnostics')
def diagnostics():
    """System diagnostics page"""
    return render_template('diagnostics.html')

@app.route('/system-diagnostics')
def system_diagnostics():
    """System diagnostics and health check endpoint"""
    try:
        from src.utils.error_handler import get_diagnostics
        
        health = check_system_health()
        diagnostics = get_diagnostics()
        config = validate_config()
        
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'health': health,
            'diagnostics': diagnostics,
            'configuration': config,
            'services_status': {
                'gmail_service': prep_app.gmail_service is not None,
                'question_generator': prep_app.question_generator is not None,
                'performance_tracker': prep_app.performance_tracker is not None,
                'app_running': True
            }
        })
    except Exception as e:
        error_info = log_error(ErrorCodes.SYSTEM_STARTUP_FAILED, f"Diagnostics failed: {e}", e)
        return jsonify({
            'error': 'Diagnostics unavailable',
            'error_code': error_info['error_code'],
            'message': str(e)
        })

@app.route('/error-report')
def error_report():
    """Generate and download error report"""
    try:
        from src.utils.error_handler import error_handler
        
        filename = error_handler.export_error_report()
        if filename:
            return jsonify({
                'success': True,
                'filename': filename,
                'message': 'Error report generated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to generate error report'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    try:
        prep_app.initialize_services()
        print("\n" + "="*50)
        print("🎉 Smart Interview Prep Tool Ready!")
        print("📱 Access your app at: http://127.0.0.1:5000")
        print("✨ Features available:")
        print("   📧 Email intelligence (simplified)")
        print("   🤖 AI question generation")
        print("   📊 Performance tracking")
        print("   📚 Question banks")
        print("   🏢 Company guides")
        print("   📈 Analytics dashboard")
        print("   🌐 Networking tools")
        print("   ✅ Preparation checklists")
        print("="*50)
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)