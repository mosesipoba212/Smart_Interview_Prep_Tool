#!/usr/bin/env python3
"""
Smart Interview Prep Tool
Main application entry point
"""

import os
import sys
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.email_parser.gmail_service import GmailService
from src.email_parser.simplified_gmail_service import SimplifiedGmailService
from src.ai_engine.question_generator import QuestionGenerator
# CALENDAR FEATURE REMOVED
from src.performance_tracker.tracker import PerformanceTracker
from src.interview_detector.detector import InterviewDetector
from src.question_banks.custom_banks import QuestionBanks
from src.company_guides.company_guides import CompanyGuides
from src.mock_interview.simulator import MockInterviewSimulator
from src.salary_negotiation.salary_tools import SalaryNegotiationTools
from src.resume_analyzer.analyzer import ResumeAnalyzer
from src.skills_assessment.skills_tool import SkillsAssessmentTool
from src.follow_up.follow_up_manager import FollowUpManager
from src.calendar.interview_calendar import InterviewCalendar
from src.analytics.analytics_dashboard import AnalyticsDashboard
from src.networking.networking_tools import NetworkingTools
from src.checklist.preparation_checklist import PreparationChecklist

# Load environment variables
load_dotenv()

app = Flask(__name__)

class InterviewPrepApp:
    def __init__(self):
        # Try full Gmail service first, fallback to simplified
        try:
            self.gmail_service = GmailService()
            if not self.gmail_service.service:
                print("📧 Falling back to simplified Gmail service...")
                self.gmail_service = SimplifiedGmailService()
        except Exception as e:
            print(f"📧 Using simplified Gmail service: {e}")
            self.gmail_service = SimplifiedGmailService()
            
        self.question_generator = QuestionGenerator()
        # CALENDAR SERVICE REMOVED
        self.performance_tracker = PerformanceTracker()
        self.interview_detector = InterviewDetector()
        self.question_banks = QuestionBanks()
        self.company_guides = CompanyGuides()
        self.mock_interview = MockInterviewSimulator()
        self.salary_tools = SalaryNegotiationTools()
        self.resume_analyzer = ResumeAnalyzer()
        self.skills_assessment = SkillsAssessmentTool()
        self.follow_up_manager = FollowUpManager()
        self.interview_calendar = InterviewCalendar()
        self.analytics_dashboard = AnalyticsDashboard()
        self.networking_tools = NetworkingTools()
        self.preparation_checklist = PreparationChecklist()
    
    def process_emails(self):
        """Fetch and process recent emails for interview invitations"""
        try:
            emails = self.gmail_service.fetch_recent_emails()
            interview_emails = []
            
            for email in emails:
                if self.interview_detector.is_interview_email(email):
                    interview_type = self.interview_detector.detect_interview_type(email)
                    interview_info = self.gmail_service.parse_interview_details(email)
                    interview_info['type'] = interview_type
                    interview_emails.append(interview_info)
            
            return interview_emails
        except Exception as e:
            print(f"Error processing emails: {e}")
            return []
    
    def generate_prep_plan(self, interview_info):
        """Generate a comprehensive prep plan for an interview"""
        interview_type = interview_info.get('type', 'general')
        company = interview_info.get('company', 'Unknown')
        position = interview_info.get('position', 'Unknown')
        
        # Generate tailored questions
        questions = self.question_generator.generate_questions(
            interview_type=interview_type,
            company=company,
            position=position
        )
        
        # Schedule prep blocks in calendar
        prep_schedule = self.calendar_service.schedule_prep_blocks(
            interview_date=interview_info.get('date'),
            interview_type=interview_type,
            duration_hours=2
        )
        
        return {
            'questions': questions,
            'schedule': prep_schedule,
            'interview_info': interview_info
        }

# Initialize the app
prep_app = InterviewPrepApp()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scan-emails', methods=['POST'])
def scan_emails():
    """API endpoint to scan for new interview emails"""
    try:
        interview_emails = prep_app.process_emails()
        return jsonify({
            'success': True,
            'interviews': interview_emails,
            'count': len(interview_emails)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-prep', methods=['POST'])
def generate_prep():
    """API endpoint to generate prep plan for an interview"""
    try:
        interview_data = request.json
        prep_plan = prep_app.generate_prep_plan(interview_data)
        return jsonify({
            'success': True,
            'prep_plan': prep_plan
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/track-performance', methods=['POST'])
def track_performance():
    """API endpoint to track interview performance"""
    try:
        performance_data = request.json
        result = prep_app.performance_tracker.log_performance(performance_data)
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/dashboard')
def dashboard():
    """API endpoint to get dashboard data"""
    try:
        stats = prep_app.performance_tracker.get_performance_stats()
        upcoming_interviews = prep_app.calendar_service.get_upcoming_interviews()
        
        return jsonify({
            'success': True,
            'dashboard': {
                'performance_stats': stats,
                'upcoming_interviews': upcoming_interviews
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/scan-emails', methods=['POST'])
def scan_emails_simple():
    """Scan emails endpoint without /api prefix"""
    try:
        interview_emails = prep_app.process_emails()
        return jsonify({
            'status': 'success',
            'interviews': interview_emails,
            'count': len(interview_emails)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    """Generate AI questions endpoint"""
    try:
        data = request.json
        company = data.get('company', '')
        position = data.get('position', '')
        interview_type = data.get('interview_type', 'general')
        
        questions = prep_app.question_generator.generate_questions(
            interview_type=interview_type,
            company=company,
            position=position
        )
        
        return jsonify({
            'status': 'success',
            'questions': questions
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/schedule-prep', methods=['POST'])
def schedule_prep():
    """Schedule prep session endpoint"""
    try:
        data = request.json
        company = data.get('company', '')
        interview_date = data.get('interview_date', '')
        
        events = prep_app.calendar_service.schedule_prep_session(
            company=company,
            interview_date=interview_date
        )
        
        return jsonify({
            'status': 'success',
            'events': events
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/performance-stats', methods=['GET'])
def performance_stats():
    """Get performance statistics endpoint"""
    try:
        stats = prep_app.performance_tracker.get_performance_stats()
        return jsonify({
            'status': 'success',
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/log-interview', methods=['POST'])
def log_interview():
    """Log interview performance endpoint"""
    try:
        data = request.json
        result = prep_app.performance_tracker.log_performance(data)
        return jsonify({
            'status': 'success',
            'result': result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/question-banks/categories', methods=['GET'])
def get_question_categories():
    """Get available question bank categories"""
    try:
        categories = prep_app.question_banks.get_available_categories()
        return jsonify({
            'status': 'success',
            'categories': categories
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/question-banks/custom', methods=['POST'])
def get_custom_questions():
    """Generate custom question set based on filters"""
    try:
        filters = request.json
        question_set = prep_app.question_banks.get_custom_question_set(filters)
        return jsonify({
            'status': 'success',
            'question_set': question_set
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/question-banks/industry/<industry>', methods=['GET'])
def get_industry_questions(industry):
    """Get questions for specific industry"""
    try:
        question_type = request.args.get('type')
        count = int(request.args.get('count', 10))
        
        questions = prep_app.question_banks.get_questions_by_industry(
            industry, question_type, count
        )
        
        return jsonify({
            'status': 'success',
            'questions': questions,
            'industry': industry,
            'type': question_type,
            'count': len(questions)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/question-banks/role/<role>', methods=['GET'])
def get_role_questions(role):
    """Get questions for specific role"""
    try:
        level = request.args.get('level')
        count = int(request.args.get('count', 10))
        
        questions = prep_app.question_banks.get_questions_by_role(
            role, level, count
        )
        
        return jsonify({
            'status': 'success',
            'questions': questions,
            'role': role,
            'level': level,
            'count': len(questions)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Computing Study Resources Routes
@app.route('/study-resources', methods=['GET'])
def get_study_resources():
    """Get computing/programming study resources"""
    try:
        resources = {
            'coding_practice': [
                {
                    'name': 'LeetCode',
                    'url': 'https://leetcode.com',
                    'description': 'Essential coding interview problems with solutions',
                    'category': 'Algorithm Practice',
                    'difficulty': 'Beginner to Advanced',
                    'best_for': 'Technical interviews, problem-solving skills'
                },
                {
                    'name': 'HackerRank',
                    'url': 'https://www.hackerrank.com',
                    'description': 'Coding challenges and skill assessments',
                    'category': 'Programming Skills',
                    'difficulty': 'Beginner to Advanced',
                    'best_for': 'Multiple programming languages, assessments'
                },
                {
                    'name': 'CodeSignal',
                    'url': 'https://codesignal.com',
                    'description': 'Real-world coding assessments',
                    'category': 'Technical Assessment',
                    'difficulty': 'Intermediate to Advanced',
                    'best_for': 'Company-specific coding tests'
                },
                {
                    'name': 'Codility',
                    'url': 'https://www.codility.com',
                    'description': 'Programming exercises and lessons',
                    'category': 'Algorithm Training',
                    'difficulty': 'Beginner to Advanced',
                    'best_for': 'Algorithm efficiency, complexity analysis'
                }
            ],
            'learning_platforms': [
                {
                    'name': 'Codecademy',
                    'url': 'https://www.codecademy.com',
                    'description': 'Interactive programming courses',
                    'category': 'Programming Fundamentals',
                    'difficulty': 'Beginner to Intermediate',
                    'best_for': 'Learning new languages, hands-on practice'
                },
                {
                    'name': 'FreeCodeCamp',
                    'url': 'https://www.freecodecamp.org',
                    'description': 'Free full-stack development curriculum',
                    'category': 'Web Development',
                    'difficulty': 'Beginner to Intermediate',
                    'best_for': 'Full-stack development, portfolio projects'
                },
                {
                    'name': 'Coursera',
                    'url': 'https://www.coursera.org',
                    'description': 'University-level computer science courses',
                    'category': 'Computer Science Theory',
                    'difficulty': 'Beginner to Advanced',
                    'best_for': 'Theoretical foundations, specialized topics'
                },
                {
                    'name': 'edX',
                    'url': 'https://www.edx.org',
                    'description': 'MIT, Harvard CS courses online',
                    'category': 'Academic CS',
                    'difficulty': 'Intermediate to Advanced',
                    'best_for': 'Rigorous computer science education'
                }
            ],
            'system_design': [
                {
                    'name': 'System Design Primer',
                    'url': 'https://github.com/donnemartin/system-design-primer',
                    'description': 'Comprehensive system design resource',
                    'category': 'System Architecture',
                    'difficulty': 'Intermediate to Advanced',
                    'best_for': 'Senior engineer interviews, scalability concepts'
                },
                {
                    'name': 'High Scalability',
                    'url': 'http://highscalability.com',
                    'description': 'Real-world system architecture case studies',
                    'category': 'Scalability',
                    'difficulty': 'Intermediate to Advanced',
                    'best_for': 'Understanding large-scale systems'
                },
                {
                    'name': 'Designing Data-Intensive Applications',
                    'url': 'https://dataintensive.net',
                    'description': 'Essential book for data system design',
                    'category': 'Data Systems',
                    'difficulty': 'Advanced',
                    'best_for': 'Senior/Staff engineer roles'
                }
            ],
            'interview_prep': [
                {
                    'name': 'Cracking the Coding Interview',
                    'url': 'https://www.crackingthecodinginterview.com',
                    'description': 'The gold standard for technical interview prep',
                    'category': 'Interview Strategy',
                    'difficulty': 'All Levels',
                    'best_for': 'Comprehensive interview preparation'
                },
                {
                    'name': 'Pramp',
                    'url': 'https://www.pramp.com',
                    'description': 'Free peer-to-peer mock interviews',
                    'category': 'Mock Interviews',
                    'difficulty': 'All Levels',
                    'best_for': 'Interview practice, communication skills'
                },
                {
                    'name': 'InterviewBit',
                    'url': 'https://www.interviewbit.com',
                    'description': 'Structured interview preparation path',
                    'category': 'Technical Prep',
                    'difficulty': 'Beginner to Advanced',
                    'best_for': 'Systematic preparation approach'
                }
            ],
            'competitive_programming': [
                {
                    'name': 'Codeforces',
                    'url': 'https://codeforces.com',
                    'description': 'Competitive programming contests',
                    'category': 'Algorithm Contests',
                    'difficulty': 'Intermediate to Expert',
                    'best_for': 'Advanced problem-solving, contest experience'
                },
                {
                    'name': 'AtCoder',
                    'url': 'https://atcoder.jp',
                    'description': 'Japanese competitive programming platform',
                    'category': 'Algorithm Contests',
                    'difficulty': 'Beginner to Expert',
                    'best_for': 'Regular practice, well-structured problems'
                },
                {
                    'name': 'TopCoder',
                    'url': 'https://www.topcoder.com',
                    'description': 'Algorithmic competitions and challenges',
                    'category': 'Algorithm Contests',
                    'difficulty': 'Intermediate to Expert',
                    'best_for': 'Single round matches, algorithm development'
                }
            ]
        }
        
        return jsonify({
            'status': 'success',
            'resources': resources
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Company Guides Routes
@app.route('/company-guides', methods=['GET'])
def get_company_guides():
    """Get all available company guides"""
    try:
        companies = prep_app.company_guides.get_all_companies()
        return jsonify({
            'status': 'success',
            'companies': companies
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/company-guides/<company>', methods=['GET'])
def get_company_guide(company):
    """Get detailed guide for a specific company"""
    try:
        guide = prep_app.company_guides.get_company_guide(company)
        if not guide:
            return jsonify({
                'status': 'error',
                'message': 'Company not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'guide': guide
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/company-guides/search', methods=['GET'])
def search_company_guides():
    """Search company guides"""
    try:
        query = request.args.get('q', '')
        results = prep_app.company_guides.search_companies(query)
        return jsonify({
            'status': 'success',
            'results': results
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Mock Interview Routes
@app.route('/mock-interview/types', methods=['GET'])
def get_interview_types():
    """Get available mock interview types"""
    try:
        types = prep_app.mock_interview.get_interview_types()
        return jsonify({
            'status': 'success',
            'types': types
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/mock-interview/start', methods=['POST'])
def start_mock_interview():
    """Start a new mock interview session"""
    try:
        data = request.json
        interview_type = data.get('type')
        difficulty = data.get('difficulty')
        company = data.get('company')
        role = data.get('role')
        
        session = prep_app.mock_interview.start_interview(
            interview_type, difficulty, company, role
        )
        
        return jsonify({
            'status': 'success',
            'session': session
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/mock-interview/submit-answer', methods=['POST'])
def submit_interview_answer():
    """Submit an answer for evaluation"""
    try:
        data = request.json
        session_id = data.get('session_id')
        question_index = data.get('question_index')
        answer = data.get('answer')
        response_time = data.get('response_time')
        
        feedback = prep_app.mock_interview.submit_answer(
            session_id, question_index, answer, response_time
        )
        
        return jsonify({
            'status': 'success',
            'feedback': feedback
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/mock-interview/report', methods=['POST'])
def get_interview_report():
    """Generate final interview report"""
    try:
        session_data = request.json
        report = prep_app.mock_interview.get_final_report(session_data)
        
        return jsonify({
            'status': 'success',
            'report': report
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/mock-interview/suggestions', methods=['GET'])
def get_practice_suggestions():
    """Get personalized practice suggestions"""
    try:
        interview_type = request.args.get('type', 'technical')
        suggestions = prep_app.mock_interview.get_practice_suggestions(interview_type)
        
        return jsonify({
            'status': 'success',
            'suggestions': suggestions
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Salary Negotiation Routes
@app.route('/salary/calculate-range', methods=['POST'])
def calculate_salary_range():
    """Calculate salary range based on role, level, and location"""
    try:
        data = request.json
        role = data.get('role')
        level = data.get('level')
        location = data.get('location')
        years_experience = data.get('years_experience')
        
        result = prep_app.salary_tools.calculate_salary_range(
            role, level, location, years_experience
        )
        
        return jsonify({
            'status': 'success',
            'salary_data': result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/salary/total-compensation', methods=['POST'])
def calculate_total_compensation():
    """Calculate total compensation including benefits"""
    try:
        data = request.json
        base_salary = data.get('base_salary', 0)
        equity_value = data.get('equity_value', 0)
        bonus = data.get('bonus', 0)
        benefits_value = data.get('benefits_value', 0)
        
        result = prep_app.salary_tools.calculate_total_compensation(
            base_salary, equity_value, bonus, benefits_value
        )
        
        return jsonify({
            'status': 'success',
            'compensation': result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/salary/negotiation-strategy', methods=['POST'])
def get_negotiation_strategy():
    """Get personalized negotiation strategy"""
    try:
        data = request.json
        current_offer = data.get('current_offer')
        target_salary = data.get('target_salary')
        role = data.get('role')
        level = data.get('level')
        
        strategy = prep_app.salary_tools.get_negotiation_strategy(
            current_offer, target_salary, role, level
        )
        
        return jsonify({
            'status': 'success',
            'strategy': strategy
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/salary/benefits-calculator', methods=['POST'])
def calculate_benefits_value():
    """Calculate the value of benefits package"""
    try:
        data = request.json
        base_salary = data.get('base_salary', 0)
        
        result = prep_app.salary_tools.get_benefits_calculator(base_salary)
        
        return jsonify({
            'status': 'success',
            'benefits': result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/salary/personalized-advice', methods=['POST'])
def get_personalized_advice():
    """Get AI-powered personalized negotiation advice"""
    try:
        profile = request.json
        advice = prep_app.salary_tools.generate_personalized_advice(profile)
        
        return jsonify({
            'status': 'success',
            'advice': advice
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/salary/templates', methods=['GET'])
def get_negotiation_templates():
    """Get email templates for salary negotiation"""
    try:
        templates = prep_app.salary_tools.get_negotiation_templates()
        
        return jsonify({
            'status': 'success',
            'templates': templates
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/salary/research-tips', methods=['GET'])
def get_research_tips():
    """Get company research tips for salary negotiation"""
    try:
        tips = prep_app.salary_tools.get_company_research_tips()
        
        return jsonify({
            'status': 'success',
            'tips': tips
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Salary Negotiation Routes
@app.route('/salary/calculate', methods=['POST'])
def calculate_salary():
    """Calculate salary range for given parameters"""
    try:
        data = request.json
        role = data.get('role')
        level = data.get('level')
        location = data.get('location')
        experience = data.get('experience')
        
        result = prep_app.salary_tools.calculate_salary_range(
            role, level, location, experience
        )
        
        return jsonify({
            'status': 'success',
            'salary_data': result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/salary/benefits-calculator', methods=['POST'])
def calculate_benefits():
    """Calculate benefits value"""
    try:
        data = request.json
        base_salary = data.get('base_salary')
        
        benefits = prep_app.salary_tools.get_benefits_calculator(base_salary)
        
        return jsonify({
            'status': 'success',
            'benefits': benefits
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Resume Analyzer Routes
@app.route('/resume/analyze', methods=['POST'])
def analyze_resume():
    """Analyze uploaded resume"""
    try:
        file = request.files.get('resume')
        job_description = request.form.get('job_description', '')
        
        if not file:
            return jsonify({'status': 'error', 'message': 'No file uploaded'}), 400
        
        # Save uploaded file temporarily
        temp_path = f"temp_{file.filename}"
        file.save(temp_path)
        
        try:
            analysis = prep_app.resume_analyzer.analyze_resume(temp_path, job_description)
            return jsonify({'status': 'success', 'analysis': analysis})
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/resume/optimize', methods=['POST'])
def optimize_resume():
    """Get resume optimization suggestions"""
    try:
        data = request.json
        optimization = prep_app.resume_analyzer.optimize_resume_content(data)
        return jsonify({'status': 'success', 'optimization': optimization})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Skills Assessment Routes
@app.route('/skills/categories', methods=['GET'])
def get_skill_categories():
    """Get available skill categories"""
    try:
        categories = prep_app.skills_assessment.get_skill_categories()
        return jsonify({'status': 'success', 'categories': categories})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/skills/assessment', methods=['POST'])
def create_skill_assessment():
    """Create skill assessment"""
    try:
        data = request.json
        assessment = prep_app.skills_assessment.create_assessment(
            data.get('categories', []),
            data.get('difficulty', 'intermediate'),
            data.get('question_count', 10)
        )
        return jsonify({'status': 'success', 'assessment': assessment})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/skills/evaluate', methods=['POST'])
def evaluate_assessment():
    """Evaluate completed assessment"""
    try:
        data = request.json
        evaluation = prep_app.skills_assessment.evaluate_assessment(data.get('responses', []))
        return jsonify({'status': 'success', 'evaluation': evaluation})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Follow-up Management Routes
@app.route('/followup/plan', methods=['POST'])
def create_followup_plan():
    """Create follow-up plan"""
    try:
        interview_data = request.json
        strategy = interview_data.get('strategy', 'standard')
        plan = prep_app.follow_up_manager.create_follow_up_plan(interview_data, strategy)
        return jsonify({'status': 'success', 'plan': plan})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/followup/personalize', methods=['POST'])
def personalize_email():
    """Personalize follow-up email"""
    try:
        data = request.json
        personalized = prep_app.follow_up_manager.personalize_email(
            data.get('template_content'),
            data.get('personal_details')
        )
        return jsonify({'status': 'success', 'email': personalized})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Interview Calendar Routes
@app.route('/calendar/schedule', methods=['POST'])
def create_interview_schedule():
    """Create interview schedule with prep timeline"""
    try:
        interview_data = request.json
        schedule = prep_app.interview_calendar.create_interview_schedule(interview_data)
        return jsonify({'status': 'success', 'schedule': schedule})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/calendar/daily-plan', methods=['POST'])
def get_daily_prep_plan():
    """Get daily preparation plan"""
    try:
        data = request.json
        plan = prep_app.interview_calendar.get_daily_prep_plan(
            data.get('interview_date'),
            data.get('interview_type')
        )
        return jsonify({'status': 'success', 'plan': plan})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Analytics Dashboard Routes
@app.route('/analytics/comprehensive', methods=['POST'])
def get_comprehensive_analytics():
    """Get comprehensive analytics dashboard"""
    try:
        user_data = request.json
        analytics = prep_app.analytics_dashboard.generate_comprehensive_analytics(user_data)
        return jsonify({'status': 'success', 'analytics': analytics})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/analytics/export', methods=['POST'])
def export_analytics():
    """Export analytics report"""
    try:
        data = request.json
        report = prep_app.analytics_dashboard.export_analytics_report(
            data.get('analytics_data'),
            data.get('format', 'json')
        )
        return jsonify({'status': 'success', 'report': report})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Networking Tools Routes
@app.route('/networking/strategy', methods=['POST'])
def create_networking_strategy():
    """Create networking strategy"""
    try:
        data = request.json
        strategy = prep_app.networking_tools.create_networking_strategy(
            data.get('user_profile'),
            data.get('goals')
        )
        return jsonify({'status': 'success', 'strategy': strategy})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/networking/message', methods=['POST'])
def generate_connection_message():
    """Generate personalized connection message"""
    try:
        data = request.json
        message = prep_app.networking_tools.generate_connection_message(
            data.get('template_type'),
            data.get('personalization_data')
        )
        return jsonify({'status': 'success', 'message': message})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/networking/linkedin-optimize', methods=['POST'])
def optimize_linkedin():
    """Optimize LinkedIn profile"""
    try:
        data = request.json
        optimization = prep_app.networking_tools.optimize_linkedin_profile(
            data.get('profile_data'),
            data.get('target_role')
        )
        return jsonify({'status': 'success', 'optimization': optimization})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Preparation Checklist Routes
@app.route('/checklist/create', methods=['POST'])
def create_preparation_checklist():
    """Create personalized preparation checklist"""
    try:
        data = request.json
        checklist = prep_app.preparation_checklist.create_personalized_checklist(
            data.get('interview_data'),
            data.get('user_preferences')
        )
        return jsonify({'status': 'success', 'checklist': checklist})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/checklist/readiness', methods=['POST'])
def calculate_readiness():
    """Calculate interview readiness score"""
    try:
        checklist_data = request.json
        readiness = prep_app.preparation_checklist.calculate_readiness_score(checklist_data)
        return jsonify({'status': 'success', 'readiness': readiness})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/checklist/schedule', methods=['POST'])
def generate_prep_schedule():
    """Generate daily preparation schedule"""
    try:
        data = request.json
        schedule = prep_app.preparation_checklist.generate_daily_prep_schedule(
            data.get('checklist_data'),
            data.get('days_remaining')
        )
        return jsonify({'status': 'success', 'schedule': schedule})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Smart Interview Prep Tool...")
    print("📧 Gmail integration active")
    print("🤖 AI question generator ready")
    print("📅 Calendar integration enabled")
    print("📊 Performance tracking initialized")
    print("🎯 Resume analyzer ready")
    print("🔧 Skills assessment tools loaded")
    print("📬 Follow-up management enabled")
    print("📈 Analytics dashboard active")
    print("🌐 Networking tools ready")
    print("✅ Preparation checklists loaded")
    
    app.run(debug=True, host='0.0.0.0', port=5000)