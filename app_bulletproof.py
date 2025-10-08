#!/usr/bin/env python3
"""
🎯 Smart Interview Prep Tool - BULLETPROOF PRODUCTION VERSION
Ultra-robust application with comprehensive error handling and auto-recovery
"""

import os
import sys
import sqlite3
import logging
import traceback
import json
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.exceptions import BadRequest, InternalServerError

# Configure robust logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('smart_interview_prep_production.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def safe_import_with_fallback(module_name, fallback=None):
    """Safely import modules with fallback options"""
    try:
        module = __import__(module_name, fromlist=[''])
        logger.info(f"✅ {module_name} imported successfully")
        return module
    except ImportError as e:
        logger.warning(f"⚠️ {module_name} not available: {e}")
        return fallback
    except Exception as e:
        logger.error(f"❌ Unexpected error importing {module_name}: {e}")
        return fallback

# Safe imports with fallbacks
CORE_MODULES_AVAILABLE = True
performance_tracker_module = None
interview_detector_module = None
question_banks_module = None
company_guides_module = None
mock_interview_module = None
application_tracker_module = None

try:
    from src.performance_tracker.tracker import PerformanceTracker
    performance_tracker_module = PerformanceTracker
    logger.info("✅ PerformanceTracker imported")
except Exception as e:
    logger.warning(f"⚠️ PerformanceTracker not available: {e}")

try:
    from src.interview_detector.detector import InterviewDetector
    interview_detector_module = InterviewDetector
    logger.info("✅ InterviewDetector imported")
except Exception as e:
    logger.warning(f"⚠️ InterviewDetector not available: {e}")

try:
    from src.question_banks.custom_banks import QuestionBanks
    question_banks_module = QuestionBanks
    logger.info("✅ QuestionBanks imported")
except Exception as e:
    logger.warning(f"⚠️ QuestionBanks not available: {e}")

try:
    from src.company_guides.company_guides import CompanyGuides
    company_guides_module = CompanyGuides
    logger.info("✅ CompanyGuides imported")
except Exception as e:
    logger.warning(f"⚠️ CompanyGuides not available: {e}")

try:
    from src.mock_interview.simulator import MockInterviewSimulator
    mock_interview_module = MockInterviewSimulator
    logger.info("✅ MockInterviewSimulator imported")
except Exception as e:
    logger.warning(f"⚠️ MockInterviewSimulator not available: {e}")

try:
    from src.application_tracker.tracker import ApplicationTracker
    application_tracker_module = ApplicationTracker
    logger.info("✅ ApplicationTracker imported")
except Exception as e:
    logger.warning(f"⚠️ ApplicationTracker not available: {e}")
    CORE_MODULES_AVAILABLE = False

# Initialize Flask application with production settings
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'smart-interview-prep-ultra-secure-2025')
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

def handle_errors(f):
    """Decorator for comprehensive error handling"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except BadRequest as e:
            logger.error(f"Bad Request in {f.__name__}: {e}")
            return jsonify({
                'success': False, 
                'error': 'Invalid request format',
                'details': str(e),
                'timestamp': datetime.now().isoformat()
            }), 400
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({
                'success': False, 
                'error': 'Internal server error',
                'details': 'An unexpected error occurred. Please try again.',
                'timestamp': datetime.now().isoformat()
            }), 500
    return decorated_function

def validate_json_request(required_fields=None):
    """Validate JSON request data"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                if request.content_type != 'application/json':
                    # Try to get JSON anyway
                    data = request.get_json(force=True)
                else:
                    data = request.get_json()
                
                if data is None:
                    return jsonify({
                        'success': False,
                        'error': 'No JSON data provided',
                        'timestamp': datetime.now().isoformat()
                    }), 400
                
                if required_fields:
                    missing_fields = [field for field in required_fields if field not in data]
                    if missing_fields:
                        return jsonify({
                            'success': False,
                            'error': 'Missing required fields',
                            'missing_fields': missing_fields,
                            'timestamp': datetime.now().isoformat()
                        }), 400
                
                return f(data, *args, **kwargs)
            except json.JSONDecodeError as e:
                return jsonify({
                    'success': False,
                    'error': 'Invalid JSON format',
                    'details': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 400
            except Exception as e:
                logger.error(f"JSON validation error: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Request validation failed',
                    'timestamp': datetime.now().isoformat()
                }), 400
        return decorated_function
    return decorator

class BulletproofSmartInterviewApp:
    """Ultra-robust Smart Interview Prep Tool with bulletproof error handling"""
    
    def __init__(self):
        """Initialize with comprehensive error handling and recovery"""
        self.app = app
        self.components_status = {}
        
        logger.info("🚀 Initializing Bulletproof Smart Interview Prep Tool...")
        
        # Initialize components with fallbacks
        self.init_components_safely()
        
        # Setup routes with error handling
        self.setup_bulletproof_routes()
        
        # Setup error handlers
        self.setup_error_handlers()
        
        logger.info("🎯 Bulletproof Smart Interview Prep Tool ready!")
        logger.info("🛡️ All error handling systems active")
        logger.info("🌐 Access at: http://127.0.0.1:5000")
    
    def init_components_safely(self):
        """Initialize all components with individual error handling"""
        components = {
            'performance_tracker': performance_tracker_module,
            'interview_detector': interview_detector_module,
            'question_banks': question_banks_module,
            'company_guides': company_guides_module,
            'mock_interview': mock_interview_module,
            'application_tracker': application_tracker_module
        }
        
        for name, component_class in components.items():
            try:
                if component_class:
                    component = component_class()
                    setattr(self, name, component)
                    self.components_status[name] = 'active'
                    logger.info(f"✅ {name}: active")
                else:
                    setattr(self, name, None)
                    self.components_status[name] = 'unavailable'
                    logger.warning(f"⚠️ {name}: unavailable")
            except Exception as e:
                setattr(self, name, None)
                self.components_status[name] = f'error: {str(e)}'
                logger.error(f"❌ {name} failed to initialize: {e}")
    
    def setup_error_handlers(self):
        """Setup global error handlers"""
        
        @self.app.errorhandler(404)
        def not_found_error(error):
            logger.warning(f"404 error: {request.url}")
            return jsonify({
                'success': False,
                'error': 'Endpoint not found',
                'url': request.url,
                'timestamp': datetime.now().isoformat()
            }), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            logger.error(f"500 error: {error}")
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'timestamp': datetime.now().isoformat()
            }), 500
        
        @self.app.errorhandler(BadRequest)
        def bad_request_error(error):
            logger.error(f"Bad request: {error}")
            return jsonify({
                'success': False,
                'error': 'Bad request format',
                'details': str(error),
                'timestamp': datetime.now().isoformat()
            }), 400
    
    def setup_bulletproof_routes(self):
        """Setup all routes with comprehensive error handling"""
        
        # Health check endpoint
        @self.app.route('/health')
        @handle_errors
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'success': True,
                'status': 'healthy',
                'components': self.components_status,
                'timestamp': datetime.now().isoformat(),
                'uptime': 'active'
            })
        
        # Main pages with error handling
        @self.app.route('/')
        @handle_errors
        def home():
            """Main dashboard"""
            return render_template('index.html')
        
        @self.app.route('/analytics')
        @handle_errors
        def analytics():
            """Analytics dashboard"""
            return render_template('analytics.html')
        
        @self.app.route('/mock-interview')
        @handle_errors
        def mock_interview():
            """Mock interview page"""
            return render_template('mock_interview.html')
        
        @self.app.route('/checklist')
        @handle_errors
        def checklist():
            """Preparation checklist"""
            return render_template('checklist.html')
        
        @self.app.route('/networking')
        @handle_errors
        def networking():
            """Networking tools"""
            return render_template('networking.html')
        
        # Bulletproof API endpoints
        @self.app.route('/api/applications', methods=['GET'])
        @handle_errors
        def get_applications():
            """Get all applications with robust error handling"""
            if not self.application_tracker:
                return jsonify({
                    'success': False,
                    'error': 'Application tracker not available',
                    'timestamp': datetime.now().isoformat()
                }), 503
            
            try:
                applications = self.application_tracker.get_all_applications()
                return jsonify({
                    'success': True, 
                    'applications': applications or [],
                    'count': len(applications) if applications else 0,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Error getting applications: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to retrieve applications',
                    'timestamp': datetime.now().isoformat()
                }), 500
        
        @self.app.route('/api/applications', methods=['POST'])
        @validate_json_request(['company', 'position'])
        @handle_errors
        def add_application(data):
            """Add new application with validation"""
            if not self.application_tracker:
                return jsonify({
                    'success': False,
                    'error': 'Application tracker not available',
                    'timestamp': datetime.now().isoformat()
                }), 503
            
            try:
                # Validate and clean data
                clean_data = {
                    'company': str(data.get('company', '')).strip(),
                    'position': str(data.get('position', '')).strip(),
                    'application_date': data.get('application_date', datetime.now().strftime('%Y-%m-%d')),
                    'status': data.get('status', 'Applied'),
                    'notes': str(data.get('notes', '')).strip(),
                    'interview_stage': data.get('interview_stage', 'Applied')
                }
                
                # Additional validation
                if not clean_data['company'] or not clean_data['position']:
                    return jsonify({
                        'success': False,
                        'error': 'Company and position cannot be empty',
                        'timestamp': datetime.now().isoformat()
                    }), 400
                
                app_id = self.application_tracker.add_application(**clean_data)
                
                return jsonify({
                    'success': True,
                    'application_id': app_id,
                    'message': 'Application added successfully',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Error adding application: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to add application',
                    'timestamp': datetime.now().isoformat()
                }), 500
        
        @self.app.route('/api/applications/<int:app_id>/advance-stage', methods=['POST'])
        @validate_json_request(['new_stage'])
        @handle_errors
        def advance_stage(data, app_id):
            """Advance application stage with validation"""
            if not self.application_tracker:
                return jsonify({
                    'success': False,
                    'error': 'Application tracker not available',
                    'timestamp': datetime.now().isoformat()
                }), 503
            
            try:
                valid_stages = [
                    'Applied', 'Online Assessment', 'Second Stage',
                    'Technical Interview', 'Final Interview', 
                    'Offer Extended', 'Rejected'
                ]
                
                new_stage = data.get('new_stage')
                if new_stage not in valid_stages:
                    return jsonify({
                        'success': False,
                        'error': 'Invalid stage',
                        'valid_stages': valid_stages,
                        'timestamp': datetime.now().isoformat()
                    }), 400
                
                assessment_details = str(data.get('assessment_details', '')).strip()
                
                success = self.application_tracker.advance_interview_stage(
                    app_id, new_stage, assessment_details
                )
                
                if success:
                    return jsonify({
                        'success': True,
                        'message': f'Advanced to {new_stage}',
                        'new_stage': new_stage,
                        'timestamp': datetime.now().isoformat()
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Failed to advance stage - application not found',
                        'timestamp': datetime.now().isoformat()
                    }), 404
            except Exception as e:
                logger.error(f"Error advancing stage: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to advance stage',
                    'timestamp': datetime.now().isoformat()
                }), 500
        
        @self.app.route('/api/stage-analytics', methods=['GET'])
        @handle_errors
        def get_stage_analytics():
            """Get stage analytics with error handling"""
            if not self.application_tracker:
                return jsonify({
                    'success': False,
                    'error': 'Application tracker not available',
                    'timestamp': datetime.now().isoformat()
                }), 503
            
            try:
                analytics = self.application_tracker.get_stage_analytics()
                return jsonify({
                    'success': True,
                    'analytics': analytics or {},
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Error getting analytics: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to retrieve analytics',
                    'timestamp': datetime.now().isoformat()
                }), 500
        
        @self.app.route('/api/interview-stages', methods=['GET'])
        @handle_errors
        def get_interview_stages():
            """Get available interview stages"""
            stages = [
                'Applied', 'Online Assessment', 'Second Stage',
                'Technical Interview', 'Final Interview',
                'Offer Extended', 'Rejected'
            ]
            return jsonify({
                'success': True,
                'stages': stages,
                'count': len(stages),
                'timestamp': datetime.now().isoformat()
            })
        
        @self.app.route('/performance-stats')
        @handle_errors
        def performance_stats():
            """Get performance statistics"""
            if not self.performance_tracker:
                return jsonify({
                    'success': False,
                    'error': 'Performance tracker not available',
                    'timestamp': datetime.now().isoformat()
                })
            
            try:
                stats = self.performance_tracker.get_performance_stats()
                return jsonify({
                    'success': True,
                    'stats': stats or {},
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Error getting performance stats: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to retrieve performance stats',
                    'timestamp': datetime.now().isoformat()
                })
        
        @self.app.route('/log-interview', methods=['POST'])
        @validate_json_request(['company', 'position'])
        @handle_errors
        def log_interview(data):
            """Log interview performance"""
            if not self.performance_tracker:
                return jsonify({
                    'success': False,
                    'error': 'Performance tracker not available',
                    'timestamp': datetime.now().isoformat()
                }), 503
            
            try:
                clean_data = {
                    'company': str(data.get('company', '')).strip(),
                    'position': str(data.get('position', '')).strip(),
                    'interview_type': data.get('interview_type', 'behavioral'),
                    'performance_score': float(data.get('performance_score', 0)),
                    'feedback': str(data.get('feedback', '')).strip(),
                    'questions_asked': data.get('questions_asked', [])
                }
                
                self.performance_tracker.log_interview(**clean_data)
                
                return jsonify({
                    'success': True,
                    'message': 'Interview logged successfully',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Error logging interview: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to log interview',
                    'timestamp': datetime.now().isoformat()
                }), 500
        
        @self.app.route('/mock-interview/start', methods=['POST'])
        @handle_errors
        def start_mock_interview():
            """Start mock interview with error handling"""
            if not self.mock_interview:
                return jsonify({
                    'success': False,
                    'error': 'Mock interview simulator not available',
                    'timestamp': datetime.now().isoformat()
                }), 503
            
            try:
                data = request.get_json() or {}
                
                session_data = {
                    'company': data.get('company', 'General'),
                    'position': data.get('position', 'Software Engineer'),
                    'interview_type': data.get('interview_type', 'behavioral'),
                    'difficulty': data.get('difficulty', 'medium')
                }
                
                session = self.mock_interview.start_interview(**session_data)
                
                return jsonify({
                    'success': True,
                    'session': session or {},
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Error starting mock interview: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to start mock interview',
                    'timestamp': datetime.now().isoformat()
                }), 500

# Create global app instance
bulletproof_app = BulletproofSmartInterviewApp()

def run_production_server(host='127.0.0.1', port=5000, debug=False):
    """Run the bulletproof server"""
    logger.info(f"🌟 Starting Bulletproof Smart Interview Prep Tool...")
    logger.info(f"🌐 Server: http://{host}:{port}")
    logger.info(f"🛡️ Debug mode: {debug}")
    logger.info(f"📊 Components status: {bulletproof_app.components_status}")
    
    try:
        app.run(host=host, port=port, debug=debug, threaded=True)
    except Exception as e:
        logger.error(f"❌ Server startup failed: {e}")
        raise

if __name__ == '__main__':
    try:
        # For development
        run_production_server(debug=True, port=5000)
    except KeyboardInterrupt:
        logger.info("👋 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)