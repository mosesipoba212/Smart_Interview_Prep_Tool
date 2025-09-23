"""
Enhanced Error Handling Module
Provides comprehensive error codes, logging, and debugging capabilities
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum
import traceback

class ErrorCodes(Enum):
    """Comprehensive error codes for the Smart Interview Prep Tool"""
    
    # System Errors (1000-1999)
    SYSTEM_STARTUP_FAILED = 1001
    DATABASE_CONNECTION_FAILED = 1002
    CONFIG_FILE_MISSING = 1003
    ENVIRONMENT_VARIABLE_MISSING = 1004
    DEPENDENCY_MISSING = 1005
    PERMISSION_DENIED = 1006
    DISK_SPACE_INSUFFICIENT = 1007
    
    # API Errors (2000-2999)
    OPENAI_API_KEY_MISSING = 2001
    OPENAI_API_QUOTA_EXCEEDED = 2002
    OPENAI_API_INVALID_REQUEST = 2003
    OPENAI_API_NETWORK_ERROR = 2004
    GOOGLE_API_KEY_MISSING = 2005
    GOOGLE_API_QUOTA_EXCEEDED = 2006
    GOOGLE_API_INVALID_CREDENTIALS = 2007
    API_RATE_LIMIT_EXCEEDED = 2008
    API_TIMEOUT = 2009
    
    # Email Service Errors (3000-3999)
    GMAIL_AUTH_FAILED = 3001
    GMAIL_PERMISSION_DENIED = 3002
    EMAIL_PARSING_FAILED = 3003
    EMAIL_FETCH_FAILED = 3004
    EMAIL_SEND_FAILED = 3005
    INVALID_EMAIL_FORMAT = 3006
    
    # Database Errors (4000-4999)
    DATABASE_WRITE_FAILED = 4001
    DATABASE_READ_FAILED = 4002
    DATABASE_CORRUPTION = 4003
    INVALID_SQL_QUERY = 4004
    FOREIGN_KEY_CONSTRAINT = 4005
    DUPLICATE_ENTRY = 4006
    
    # Question Generation Errors (5000-5999)
    QUESTION_GENERATION_FAILED = 5001
    INVALID_QUESTION_TYPE = 5002
    INSUFFICIENT_QUESTION_DATA = 5003
    QUESTION_PARSING_ERROR = 5004
    TEMPLATE_NOT_FOUND = 5005
    
    # Performance Tracking Errors (6000-6999)
    PERFORMANCE_LOG_FAILED = 6001
    INVALID_PERFORMANCE_DATA = 6002
    STATISTICS_CALCULATION_ERROR = 6003
    ANALYTICS_GENERATION_FAILED = 6004
    
    # File System Errors (7000-7999)
    FILE_NOT_FOUND = 7001
    FILE_READ_ERROR = 7002
    FILE_WRITE_ERROR = 7003
    DIRECTORY_CREATION_FAILED = 7004
    FILE_PERMISSION_DENIED = 7005
    
    # Network Errors (8000-8999)
    NETWORK_CONNECTION_FAILED = 8001
    DNS_RESOLUTION_FAILED = 8002
    SSL_CERTIFICATE_ERROR = 8003
    PROXY_ERROR = 8004
    
    # Validation Errors (9000-9999)
    INVALID_INPUT_FORMAT = 9001
    MISSING_REQUIRED_FIELD = 9002
    DATA_TYPE_MISMATCH = 9003
    VALUE_OUT_OF_RANGE = 9004
    INVALID_DATE_FORMAT = 9005

class ErrorHandler:
    """Enhanced error handling with detailed logging and debugging"""
    
    def __init__(self, log_file: str = "smart_interview_prep_errors.log"):
        self.log_file = log_file
        self.setup_logging()
        self.error_count = 0
        self.error_history = []
    
    def setup_logging(self):
        """Setup comprehensive logging configuration"""
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def handle_error(self, error_code: ErrorCodes, error_message: str, 
                    exception: Optional[Exception] = None, 
                    context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Handle errors with comprehensive logging and debugging info"""
        
        error_info = {
            'error_code': error_code.value,
            'error_name': error_code.name,
            'message': error_message,
            'timestamp': datetime.now().isoformat(),
            'context': context or {},
            'traceback': None,
            'suggestions': self.get_error_suggestions(error_code)
        }
        
        if exception:
            error_info['exception_type'] = type(exception).__name__
            error_info['exception_message'] = str(exception)
            error_info['traceback'] = traceback.format_exc()
        
        # Log the error
        self.logger.error(f"[{error_code.name}] {error_message}")
        if exception:
            self.logger.error(f"Exception: {exception}")
        if context:
            self.logger.error(f"Context: {json.dumps(context, indent=2)}")
        
        # Store in error history
        self.error_count += 1
        self.error_history.append(error_info)
        
        # Keep only last 100 errors
        if len(self.error_history) > 100:
            self.error_history = self.error_history[-100:]
        
        return error_info
    
    def get_error_suggestions(self, error_code: ErrorCodes) -> List[str]:
        """Get suggestions for resolving specific errors"""
        suggestions = {
            ErrorCodes.OPENAI_API_KEY_MISSING: [
                "Set the OPENAI_API_KEY environment variable",
                "Check if .env file exists and contains the API key",
                "Verify the API key is valid on OpenAI platform"
            ],
            ErrorCodes.OPENAI_API_QUOTA_EXCEEDED: [
                "Check your OpenAI API usage limits",
                "Upgrade your OpenAI plan if needed",
                "Wait for quota reset or reduce API calls"
            ],
            ErrorCodes.DATABASE_CONNECTION_FAILED: [
                "Check if database file exists and is accessible",
                "Verify file permissions for database operations",
                "Ensure sufficient disk space for database operations"
            ],
            ErrorCodes.GMAIL_AUTH_FAILED: [
                "Verify Google API credentials are correctly configured",
                "Check if OAuth2 token needs refresh",
                "Ensure proper scopes are enabled for Gmail API"
            ],
            ErrorCodes.QUESTION_GENERATION_FAILED: [
                "Check internet connection for AI services",
                "Verify input parameters are valid",
                "Try using fallback question templates"
            ],
            ErrorCodes.FILE_NOT_FOUND: [
                "Check if the file path is correct",
                "Verify the file exists in the expected location",
                "Check file permissions and accessibility"
            ],
            ErrorCodes.NETWORK_CONNECTION_FAILED: [
                "Check internet connection",
                "Verify firewall settings allow the connection",
                "Try again after a short delay"
            ]
        }
        
        return suggestions.get(error_code, ["Contact support with error details"])
    
    def get_diagnostic_info(self) -> Dict[str, Any]:
        """Get comprehensive diagnostic information"""
        return {
            'system_info': {
                'python_version': sys.version,
                'platform': sys.platform,
                'current_directory': os.getcwd(),
                'environment_variables': {
                    'OPENAI_API_KEY': '***SET***' if os.getenv('OPENAI_API_KEY') else 'NOT_SET',
                    'GOOGLE_API_KEY': '***SET***' if os.getenv('GOOGLE_API_KEY') else 'NOT_SET'
                }
            },
            'error_statistics': {
                'total_errors': self.error_count,
                'recent_errors': len([e for e in self.error_history if 
                                    datetime.fromisoformat(e['timestamp']) > 
                                    datetime.now().replace(hour=0, minute=0, second=0)]),
                'error_types': self.get_error_type_distribution()
            },
            'recent_errors': self.error_history[-10:] if self.error_history else []
        }
    
    def get_error_type_distribution(self) -> Dict[str, int]:
        """Get distribution of error types"""
        distribution = {}
        for error in self.error_history:
            error_category = str(error['error_code'])[0] + "000-" + str(error['error_code'])[0] + "999"
            distribution[error_category] = distribution.get(error_category, 0) + 1
        return distribution
    
    def export_error_report(self) -> str:
        """Export comprehensive error report"""
        report = {
            'report_timestamp': datetime.now().isoformat(),
            'diagnostic_info': self.get_diagnostic_info(),
            'all_errors': self.error_history
        }
        
        filename = f"error_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            return filename
        except Exception as e:
            self.logger.error(f"Failed to export error report: {e}")
            return ""

# Global error handler instance
error_handler = ErrorHandler()

def log_error(error_code: ErrorCodes, message: str, exception: Optional[Exception] = None, 
              context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Convenience function for logging errors"""
    return error_handler.handle_error(error_code, message, exception, context)

def get_diagnostics() -> Dict[str, Any]:
    """Get diagnostic information"""
    return error_handler.get_diagnostic_info()

def check_system_health() -> Dict[str, Any]:
    """Comprehensive system health check with enhanced dependency detection"""
    health_status = {
        'status': 'healthy',
        'checks': {},
        'warnings': [],
        'errors': []
    }
    
    # Import dependency manager
    try:
        from .dependency_manager import get_dependency_status
        dependency_status = get_dependency_status()
        
        # Update health checks based on dependency status
        for module_name, is_available in dependency_status['available'].items():
            health_status['checks'][f'package_{module_name}'] = is_available
        
        if dependency_status['missing']:
            missing_modules = dependency_status['missing']
            # Only warn about truly important missing modules
            important_missing = [m for m in missing_modules if m in ['openai', 'docx']]
            if important_missing:
                health_status['warnings'].append(f"Optional modules not available: {', '.join(important_missing)}")
        
    except ImportError:
        # Fallback to original package checking
        health_status['warnings'].append("Dependency manager not available - using basic checks")
        
        # Check required packages with correct import names
        package_checks = [
            ('flask', 'flask'),
            ('openai', 'openai'), 
            ('python-docx', 'docx'),
            ('requests', 'requests'),
            ('python-dotenv', 'dotenv')
        ]
        
        for package_name, import_name in package_checks:
            try:
                __import__(import_name)
                health_status['checks'][f'package_{package_name}'] = True
            except ImportError:
                health_status['checks'][f'package_{package_name}'] = False
                if package_name in ['flask', 'requests']:  # Only error on truly required packages
                    health_status['errors'].append(f"Required package missing: {package_name}")
                else:
                    health_status['warnings'].append(f"Optional package not available: {package_name}")
    
    # Check environment variables
    if not os.getenv('OPENAI_API_KEY'):
        health_status['warnings'].append("OpenAI API key not configured")
        health_status['checks']['openai_key'] = False
    else:
        health_status['checks']['openai_key'] = True
    
    if not os.getenv('GOOGLE_API_KEY'):
        health_status['warnings'].append("Google API key not configured")
        health_status['checks']['google_key'] = False
    else:
        health_status['checks']['google_key'] = True
    
    # Check database accessibility
    try:
        import sqlite3
        conn = sqlite3.connect("interview_performance.db")
        conn.close()
        health_status['checks']['database'] = True
    except Exception as e:
        health_status['errors'].append(f"Database check failed: {e}")
        health_status['checks']['database'] = False
        health_status['status'] = 'unhealthy'
    
    # Check disk space
    try:
        import shutil
        total, used, free = shutil.disk_usage('.')
        free_mb = free // (1024*1024)
        
        if free_mb < 100:  # Less than 100MB
            health_status['warnings'].append(f"Low disk space: {free_mb}MB available")
            health_status['checks']['disk_space'] = False
        else:
            health_status['checks']['disk_space'] = True
    except Exception as e:
        health_status['warnings'].append(f"Could not check disk space: {e}")
    
    # Determine overall status
    if health_status['errors']:
        health_status['status'] = 'unhealthy'
    elif health_status['warnings']:
        health_status['status'] = 'warning'
    
    return health_status

def validate_config() -> Dict[str, Any]:
    """Validate application configuration"""
    config_status = {
        'valid': True,
        'issues': [],
        'recommendations': []
    }
    
    # Check .env file
    if not os.path.exists('.env'):
        config_status['issues'].append("No .env file found")
        config_status['recommendations'].append("Create .env file with required API keys")
        config_status['valid'] = False
    
    # Check required directories
    required_dirs = ['src', 'templates', 'src/ai_engine', 'src/email_parser']
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            config_status['issues'].append(f"Missing directory: {dir_path}")
            config_status['valid'] = False
    
    return config_status

if __name__ == "__main__":
    # Test error handling
    print("🔧 Testing Enhanced Error Handling System")
    
    # Test error logging
    test_error = log_error(
        ErrorCodes.OPENAI_API_KEY_MISSING,
        "API key not configured",
        context={'component': 'question_generator', 'action': 'initialization'}
    )
    
    print(f"✅ Logged error: {test_error['error_code']}")
    
    # Test system health
    health = check_system_health()
    print(f"🏥 System Health: {health['status']}")
    
    # Test diagnostics
    diagnostics = get_diagnostics()
    print(f"📊 Total errors tracked: {diagnostics['error_statistics']['total_errors']}")
    
    print("✨ Error handling system ready!")