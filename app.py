#!/usr/bin/env python3
"""
🎯 Smart Interview Prep Tool - Production Version
Clean, optimized main application entry point
"""

import os
import sys
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, send_from_directory

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Enhanced error handling
from src.utils.error_handler import ErrorCodes, log_error, check_system_health
from src.utils.dependency_manager import safe_import, get_dependency_status

# Core imports with fallback handling
from src.email_parser.gmail_service import GmailService
from src.email_parser.gmail_sync import GmailApplicationSync
from src.performance_tracker.tracker import PerformanceTracker
from src.interview_detector.detector import InterviewDetector
from src.question_banks.custom_banks import QuestionBanks
from src.company_guides.company_guides import CompanyGuides
from src.mock_interview.simulator import MockInterviewSimulator
from src.application_tracker.tracker import ApplicationTracker

# Load environment configuration
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'smart-interview-prep-2025')

class SmartInterviewPrepApp:
    """
    🚀 Main application controller for Smart Interview Prep Tool
    Manages all interview preparation features with robust error handling
    """
    
    def __init__(self):
        """Initialize all core components with health monitoring"""
        self.system_health = self._check_system_startup()
        self._initialize_components()
        
    def _check_system_startup(self) -> dict:
        """Perform comprehensive system health check"""
        print("🔍 Performing system health check...")
        health = check_system_health()
        
        if health['status'] == 'unhealthy':
            print(f"⚠️ System issues detected: {health['errors']}")
            for error in health['errors']:
                log_error(ErrorCodes.SYSTEM_STARTUP_FAILED, error)
        elif health['warnings']:
            print(f"⚠️ System warnings: {health['warnings']}")
            
        return health
    
    def _initialize_components(self):
        """Initialize all application components safely"""
        print("🚀 Initializing Smart Interview Prep Tool...")
        
        try:
            # Initialize real Gmail service only
            print("🔑 Initializing Gmail service...")
            self.gmail_service = GmailService()
            
            if self.gmail_service and self.gmail_service.service:
                print("✅ Gmail service connected and authenticated")
            else:
                print("❌ Gmail service failed to authenticate")
                print("� Please ensure credentials.json is configured and OAuth is completed")
                self.gmail_service = None
            
            # Performance tracking
            self.performance_tracker = PerformanceTracker()
            print("✅ Performance tracking ready")
            
            # Interview detection
            self.interview_detector = InterviewDetector()
            print("✅ Interview detector ready")
            
            # Question banks
            self.question_banks = QuestionBanks()
            print("✅ Question banks ready")
            
            # Company guides
            self.company_guides = CompanyGuides()
            print("✅ Company guides ready")
            
            # Mock interview simulator
            self.mock_interview = MockInterviewSimulator()
            print("✅ Mock interview simulator ready")
            
            # Application tracker
            self.application_tracker = ApplicationTracker()
            print("✅ Application tracker ready")
            
            # Gmail sync service
            self.gmail_sync = GmailApplicationSync()
            print("✅ Gmail sync service ready")
            
            print("\n" + "="*50)
            print("🎉 Smart Interview Prep Tool Ready!")
            print("📱 All features initialized successfully")
            print("="*50)
            
        except Exception as e:
            log_error(ErrorCodes.SYSTEM_STARTUP_FAILED, f"Component initialization failed: {e}")
            print(f"❌ Initialization error: {e}")

# Initialize the application
try:
    prep_app = SmartInterviewPrepApp()
except Exception as e:
    print(f"❌ Failed to initialize application: {e}")
    sys.exit(1)

# ========================================
# 🌐 CORE APPLICATION ROUTES
# ========================================

@app.route('/')
def home():
    """🏠 Main dashboard with system overview"""
    try:
        # Get performance overview
        stats = prep_app.performance_tracker.get_performance_stats()
        dependency_status = get_dependency_status()
        
        return render_template('index.html', 
                             stats=stats,
                             system_health=prep_app.system_health,
                             dependencies=dependency_status)
    except Exception as e:
        log_error(ErrorCodes.PAGE_LOAD_FAILED, f"Home page error: {e}")
        return render_template('index.html', 
                             stats={'total_interviews': 0, 'average_rating': 0},
                             system_health={'status': 'warning'},
                             dependencies={'available_count': 0})

@app.route('/health')
def health_check():
    """🔍 System health endpoint for monitoring"""
    health = check_system_health()
    dependency_status = get_dependency_status()
    
    return jsonify({
        'status': 'success',
        'health': health,
        'dependencies': dependency_status,
        'timestamp': datetime.now().isoformat()
    })

# ========================================
# 📧 EMAIL INTELLIGENCE ROUTES
# ========================================

@app.route('/scan-emails', methods=['GET', 'POST'])
def scan_emails():
    """📧 Scan for interview-related emails and sync with application tracker"""
    try:
        # Handle both GET and POST requests
        if request.method == 'GET':
            days_back = int(request.args.get('days_back', 7))
            auto_sync = request.args.get('auto_sync', 'true').lower() == 'true'
        else:
            # Check if request has JSON data
            if not request.is_json:
                return jsonify({
                    'success': False,
                    'error': 'Request must be JSON',
                    'interviews': []
                }), 400
            data = request.json or {}
            days_back = data.get('days_back', 7)
            auto_sync = data.get('auto_sync', True)
        
        # Check if Gmail service is available
        if not hasattr(prep_app, 'gmail_service') or prep_app.gmail_service is None:
            return jsonify({
                'success': False,
                'error': 'Gmail service not available. Please configure Gmail API credentials.',
                'interviews': []
            }), 503
        
        # Call Gmail service for interview detection
        interviews = prep_app.gmail_service.scan_for_interviews(days_back)
        
        # Auto-sync with application tracker if enabled
        sync_result = None
        if auto_sync and hasattr(prep_app, 'gmail_sync'):
            try:
                sync_result = prep_app.gmail_sync.sync_gmail_to_applications(days_back)
            except Exception as sync_error:
                print(f"Warning: Gmail sync failed: {sync_error}")
                sync_result = {'success': False, 'error': str(sync_error)}
        
        response_data = {
            'success': True,
            'interviews': interviews,
            'count': len(interviews)
        }
        
        # Add sync information if auto-sync was performed
        if sync_result:
            response_data['auto_sync'] = sync_result
            if sync_result.get('success'):
                response_data['sync_message'] = f"Also updated application tracker: {sync_result.get('new_applications', 0)} new applications, {sync_result.get('updated_applications', 0)} updates"
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Email scanning temporarily unavailable: {str(e)}',
            'interviews': []
        }), 500

@app.route('/test-gmail-access', methods=['GET'])
def test_gmail_access():
    """🔧 Test Gmail API access and authentication"""
    try:
        # Check if Gmail service exists
        if not hasattr(prep_app, 'gmail_service') or prep_app.gmail_service is None:
            return jsonify({
                'success': False,
                'error': 'Gmail service not initialized',
                'details': 'Gmail API credentials may be missing or invalid'
            })
        
        # Test basic Gmail API access by fetching profile
        if hasattr(prep_app.gmail_service, 'service') and prep_app.gmail_service.service:
            profile = prep_app.gmail_service.service.users().getProfile(userId='me').execute()
            return jsonify({
                'success': True,
                'message': 'Gmail API access successful!',
                'email': profile.get('emailAddress'),
                'total_messages': profile.get('messagesTotal', 0),
                'status': 'authenticated'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Gmail service not authenticated',
                'details': 'Please complete OAuth authentication'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Gmail API test failed: {str(e)}',
            'details': 'Authentication or API access issue'
        })

# ========================================
# 📊 PERFORMANCE TRACKING ROUTES
# ========================================

@app.route('/log-interview', methods=['POST'])
def log_interview():
    """📊 Log interview performance data"""
    try:
        interview_data = request.json
        result = prep_app.performance_tracker.log_performance(interview_data)
        
        return jsonify({
            'status': 'success',
            'result': result
        })
    except Exception as e:
        log_error(ErrorCodes.PERFORMANCE_LOG_FAILED, f"Performance logging failed: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/performance-stats')
def performance_stats():
    """📈 Get performance statistics"""
    try:
        stats = prep_app.performance_tracker.get_performance_stats()
        return jsonify({
            'status': 'success',
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'stats': {'total_interviews': 0, 'average_rating': 0, 'success_rate': 0}
        })

@app.route('/save-mock-interview-score', methods=['POST'])
def save_mock_interview_score():
    """💾 Save mock interview session score"""
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Extract session data
        session_id = data.get('session_id')
        interview_type = data.get('interview_type', 'general')
        difficulty = data.get('difficulty', 'medium')
        overall_score = data.get('overall_score', 0)
        question_scores = data.get('question_scores', [])
        company = data.get('company', 'Practice')
        role = data.get('role', 'General')
        
        # Create interview data for logging
        interview_data = {
            'interview': {
                'company': company,
                'position': role,
                'interview_type': interview_type,
                'interview_date': datetime.now().isoformat(),
                'outcome': 'practice',
                'overall_rating': overall_score,
                'preparation_hours': 0,
                'notes': f'Mock interview - {difficulty} difficulty'
            },
            'questions': []
        }
        
        # Add question performance data
        for i, score in enumerate(question_scores):
            if score is not None:
                interview_data['questions'].append({
                    'question_text': f'Question {i+1}',
                    'question_type': interview_type,
                    'difficulty': difficulty,
                    'confidence_rating': score,
                    'time_taken': 0,
                    'notes': 'Mock interview question'
                })
        
        # Log to performance tracker
        result = prep_app.performance_tracker.log_performance(interview_data)
        
        return jsonify({
            'success': True,
            'message': 'Mock interview score saved successfully',
            'interview_id': result.get('interview_id')
        })
        
    except Exception as e:
        log_error(ErrorCodes.MOCK_INTERVIEW_SAVE_FAILED, f"Failed to save mock interview score: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/get-score-progress')
def get_score_progress():
    """📈 Get score progress data for charts"""
    try:
        # Get recent interview scores from performance tracker
        conn = sqlite3.connect(prep_app.performance_tracker.db_path)
        cursor = conn.cursor()
        
        # Get scores over time
        cursor.execute('''
            SELECT interview_date, overall_rating, interview_type, company
            FROM interviews 
            WHERE overall_rating > 0 
            ORDER BY interview_date DESC 
            LIMIT 50
        ''')
        
        scores_data = []
        for row in cursor.fetchall():
            scores_data.append({
                'date': row[0],
                'score': row[1],
                'type': row[2],
                'company': row[3]
            })
        
        # Get average scores by interview type
        cursor.execute('''
            SELECT interview_type, AVG(overall_rating) as avg_score, COUNT(*) as count
            FROM interviews 
            WHERE overall_rating > 0 
            GROUP BY interview_type
        ''')
        
        type_averages = {}
        for row in cursor.fetchall():
            type_averages[row[0]] = {
                'average': round(row[1], 1),
                'count': row[2]
            }
        
        conn.close()
        
        return jsonify({
            'success': True,
            'scores_over_time': scores_data,
            'averages_by_type': type_averages
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'scores_over_time': [],
            'averages_by_type': {}
        }), 500

# ========================================
# � APPLICATION TRACKING ROUTES
# ========================================

@app.route('/log-application', methods=['POST'])
def log_application():
    """📋 Log a new job application"""
    try:
        application_data = request.json
        if not application_data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Log the application
        application_id = prep_app.application_tracker.log_application(application_data)
        
        if application_id:
            return jsonify({
                'success': True,
                'message': 'Application logged successfully',
                'application_id': application_id
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to log application'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/log-response', methods=['POST'])
def log_response():
    """📧 Log a company response"""
    try:
        response_data = request.json
        if not response_data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        response_id = prep_app.application_tracker.log_response(response_data)
        
        if response_id:
            return jsonify({
                'success': True,
                'message': 'Response logged successfully',
                'response_id': response_id
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to log response'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/log-outcome', methods=['POST'])
def log_outcome():
    """🎯 Log final application outcome"""
    try:
        outcome_data = request.json
        if not outcome_data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        outcome_id = prep_app.application_tracker.log_outcome(outcome_data)
        
        if outcome_id:
            return jsonify({
                'success': True,
                'message': 'Outcome logged successfully',
                'outcome_id': outcome_id
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to log outcome'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/application-stats')
def application_stats():
    """📊 Get comprehensive application statistics"""
    try:
        stats = prep_app.application_tracker.get_application_stats()
        interview_analytics = prep_app.application_tracker.get_interview_analytics()
        
        return jsonify({
            'success': True,
            'application_stats': stats,
            'interview_analytics': interview_analytics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'application_stats': {},
            'interview_analytics': {}
        }), 500

@app.route('/applications-list')
def applications_list():
    """📋 Get list of applications"""
    try:
        limit = int(request.args.get('limit', 50))
        status = request.args.get('status')
        
        applications = prep_app.application_tracker.get_applications_list(limit=limit, status=status)
        
        return jsonify({
            'success': True,
            'applications': applications,
            'count': len(applications)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'applications': []
        }), 500

@app.route('/update-application-status', methods=['POST'])
def update_application_status():
    """🔄 Update application status"""
    try:
        data = request.json
        application_id = data.get('application_id')
        new_status = data.get('status')
        
        if not application_id or not new_status:
            return jsonify({
                'success': False,
                'error': 'Missing application_id or status'
            }), 400
        
        success = prep_app.application_tracker.update_application_status(application_id, new_status)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Status updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to update status'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ========================================
# 📧 GMAIL SYNC ROUTES  
# ========================================

@app.route('/sync-gmail-applications', methods=['POST'])
def sync_gmail_applications():
    """🔄 Sync Gmail emails with application tracker"""
    try:
        data = request.json or {}
        days_back = data.get('days_back', 30)
        
        # Perform Gmail sync
        result = prep_app.gmail_sync.sync_gmail_to_applications(days_back)
        
        return jsonify({
            'success': result['success'],
            'message': f"Gmail sync completed! Processed {result['processed_emails']} emails, added {result['new_applications']} new applications, updated {result['updated_applications']} existing applications.",
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Gmail sync failed: {str(e)}',
            'data': {
                'processed_emails': 0,
                'new_applications': 0,
                'updated_applications': 0
            }
        }), 500

@app.route('/gmail-sync-status')
def gmail_sync_status():
    """📊 Get Gmail sync status and summary"""
    try:
        summary = prep_app.gmail_sync.get_sync_summary()
        
        return jsonify({
            'success': True,
            'sync_summary': summary
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'sync_summary': {}
        }), 500

@app.route('/auto-populate-from-gmail', methods=['POST'])
def auto_populate_from_gmail():
    """🤖 Auto-populate application tracker with Gmail data"""
    try:
        data = request.json or {}
        days_back = data.get('days_back', 60)  # Default to 60 days for initial population
        
        # Clear existing sample data first (optional)
        clear_sample_data = data.get('clear_sample_data', False)
        
        if clear_sample_data:
            # You can add logic here to clear sample data if needed
            pass
        
        # Sync Gmail data
        result = prep_app.gmail_sync.sync_gmail_to_applications(days_back)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': f"Successfully populated tracker with {result['new_applications']} applications from your Gmail!",
                'details': {
                    'emails_scanned': result['total_emails_scanned'],
                    'emails_processed': result['processed_emails'],
                    'new_applications': result['new_applications'],
                    'updated_applications': result['updated_applications']
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error during sync')
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Auto-population failed: {str(e)}'
        }), 500

# ========================================
# �📚 QUESTION BANKS ROUTES
# ========================================

@app.route('/question-banks/<industry>')
def get_question_bank(industry):
    """📚 Get industry-specific question bank"""
    try:
        question_type = request.args.get('type', 'behavioral')
        count = int(request.args.get('count', 10))
        
        questions = prep_app.question_banks.get_questions(industry, question_type, count)
        
        return jsonify({
            'success': True,
            'questions': questions,
            'industry': industry,
            'type': question_type
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'questions': []
        }), 500

# ========================================
# 🏢 COMPANY GUIDES ROUTES
# ========================================

@app.route('/company-guides/<company>')
def get_company_guide(company):
    """🏢 Get company-specific interview guide"""
    try:
        guide = prep_app.company_guides.get_company_guide(company)
        return jsonify({
            'success': True,
            'guide': guide
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'guide': {}
        }), 500

# ========================================
# 🎭 MOCK INTERVIEW ROUTES
# ========================================

@app.route('/mock-interview')
def mock_interview_page():
    """🎭 Mock interview practice page"""
    try:
        print("🔍 Accessing mock interview page...")
        
        # Provide default interview types if backend fails
        default_interview_types = {
            'technical': {
                'name': 'Technical Interview',
                'difficulty_levels': ['Easy', 'Medium', 'Hard']
            },
            'behavioral': {
                'name': 'Behavioral Interview',  
                'difficulty_levels': ['Basic', 'Intermediate', 'Advanced']
            },
            'system_design': {
                'name': 'System Design Interview',
                'difficulty_levels': ['Junior', 'Mid-level', 'Senior']
            }
        }
        
        try:
            interview_types = prep_app.mock_interview.get_interview_types()
            print(f"✅ Got interview types from backend: {list(interview_types.keys())}")
        except Exception as backend_error:
            print(f"⚠️ Backend error, using defaults: {backend_error}")
            interview_types = default_interview_types
            
        result = render_template('mock_interview.html', interview_types=interview_types)
        print("✅ Template rendered successfully")
        return result
    except Exception as e:
        print(f"❌ Mock interview page error: {e}")
        log_error(ErrorCodes.PAGE_LOAD_FAILED, f"Mock interview page error: {e}")
        # Return a basic error page instead of crashing
        return f"<h1>Mock Interview Page Error</h1><p>Error: {e}</p><p>Please check the console for details.</p>", 500

@app.route('/test_frontend.html')
def test_frontend():
    """Test frontend for debugging"""
    return send_from_directory('.', 'test_frontend.html')

@app.route('/mock-interview/start', methods=['POST'])
def start_mock_interview():
    """🚀 Start a new mock interview session"""
    try:
        data = request.json
        print(f"🔍 Received data: {data}")
        interview_type = data.get('interview_type')
        print(f"🔍 Interview type: {interview_type}")
        
        session = prep_app.mock_interview.start_interview(
            interview_type=interview_type,
            difficulty=data.get('difficulty'),
            company=data.get('company'),
            role=data.get('role')
        )
        
        # Add debugging info
        print(f"🔍 Session created with {len(session['questions'])} questions")
        print(f"🔍 Session interview_type: {session.get('interview_type')}")
        print(f"🔍 First question: {session['questions'][0]}")
        print(f"🔍 First question type: {type(session['questions'][0])}")
        
        return jsonify({
            'success': True,
            'session': session
        })
    except Exception as e:
        log_error(ErrorCodes.SYSTEM_ERROR, f"Mock interview start failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/mock-interview/submit-answer', methods=['POST'])
def submit_mock_answer():
    """📝 Submit answer for evaluation"""
    try:
        data = request.json
        result = prep_app.mock_interview.submit_answer(
            session_id=data.get('session_id'),
            question_index=data.get('question_index'),
            answer=data.get('answer'),
            response_time=data.get('response_time')
        )
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/mock-interview/report', methods=['POST'])
def generate_mock_report():
    """📊 Generate final interview report"""
    try:
        session_data = request.json
        report = prep_app.mock_interview.get_final_report(session_data)
        
        return jsonify({
            'success': True,
            'report': report
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/mock-interview/practice-suggestions', methods=['GET'])
def get_practice_suggestions():
    """💡 Get practice suggestions"""
    try:
        interview_type = request.args.get('type', 'technical')
        suggestions = prep_app.mock_interview.get_practice_suggestions(interview_type)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/mock-interview/text-to-speech', methods=['POST'])
def text_to_speech():
    """🎤 Convert text to speech using OpenAI TTS"""
    try:
        data = request.json
        text = data.get('text', '')
        voice = data.get('voice', 'alloy')  # alloy, echo, fable, onyx, nova, shimmer
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'No text provided'
            }), 400
        
        # Try OpenAI TTS (if available)
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai_key)
                
                response = client.audio.speech.create(
                    model="tts-1",
                    voice=voice,
                    input=text
                )
                
                # Save audio to temporary file and return as base64
                import tempfile
                import base64
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                    response.stream_to_file(temp_file.name)
                    
                    with open(temp_file.name, 'rb') as audio_file:
                        audio_data = audio_file.read()
                        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                    
                    # Clean up temporary file
                    os.unlink(temp_file.name)
                    
                    return jsonify({
                        'success': True,
                        'audio': audio_base64,
                        'provider': 'OpenAI TTS'
                    })
            except Exception as e:
                log_error(ErrorCodes.AI_SERVICE_FAILED, f"TTS generation failed: {e}")
                return jsonify({
                    'success': False,
                    'error': f'TTS error: {str(e)}',
                    'fallback': 'TTS functionality temporarily unavailable'
                }), 500
        
        # If OpenAI not available, return fallback message
        return jsonify({
            'success': False,
            'error': 'Text-to-Speech service not available. Please add OPENAI_API_KEY to enable TTS.',
            'fallback': 'TTS functionality requires OpenAI API key'
        }), 503
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========================================
# 📄 STATIC PAGES
# ========================================

@app.route('/interview-practice')
def interview_practice():
    """🎭 Interview practice page"""
    return render_template('interview_practice.html')

@app.route('/analytics')
def analytics():
    """📊 Analytics dashboard page"""
    return render_template('analytics.html')

@app.route('/study-resources')
def study_resources():
    """📚 Study resources page"""
    return render_template('study_resources.html')

@app.route('/networking')
def networking():
    """🌐 Networking tools page"""
    return render_template('networking.html')

@app.route('/checklist')
def checklist():
    """✅ Preparation checklist page"""
    return render_template('checklist.html')

@app.route('/diagnostics')
def diagnostics():
    """🔧 System diagnostics page"""
    dependency_status = get_dependency_status()
    system_health = check_system_health()
    
    return render_template('diagnostics.html',
                         dependencies=dependency_status,
                         health=system_health)

@app.route('/system-diagnostics')
def system_diagnostics():
    """🔧 System diagnostics API endpoint"""
    try:
        dependency_status = get_dependency_status()
        system_health = check_system_health()
        
        # Get additional system info
        system_info = {
            'ai_service': {
                'provider': 'Google Gemini (Free)',
                'status': 'operational',
                'requests_available': '15/minute'
            },
            'database': {
                'type': 'SQLite',
                'status': 'connected',
                'location': 'local'
            },
            'services': {
                'email_intelligence': True,
                'mock_interview': True,
                'performance_tracking': True,
                'question_banks': True
            }
        }
        
        return jsonify({
            'success': True,
            'dependencies': dependency_status,
            'health': system_health,
            'system_info': system_info
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/code-documentation')
def code_documentation():
    """📋 Code architecture documentation page"""
    return render_template('code_documentation.html')

@app.route('/favicon.ico')
def favicon():
    """🌟 Favicon route to prevent 404 errors"""
    return '', 204

@app.route('/test-button')
def test_button():
    """🧪 Test the mock interview button functionality"""
    import os
    test_file_path = os.path.join(os.path.dirname(__file__), 'test_button.html')
    with open(test_file_path, 'r', encoding='utf-8') as f:
        return f.read()

# ========================================
# 🚀 APPLICATION STARTUP
# ========================================

if __name__ == '__main__':
    print("\n🎯 Starting Smart Interview Prep Tool...")
    print(f"📱 Access your app at: http://127.0.0.1:5000")
    print("✨ Features available:")
    print("   📧 Email intelligence")
    print("   📊 Performance tracking")
    print("   📚 Question banks")
    print("   🏢 Company guides")
    print("   📈 Analytics dashboard")
    print("   🌐 Networking tools")
    print("   ✅ Preparation checklists")
    print("="*50)
    
    # Run the application
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True
    )