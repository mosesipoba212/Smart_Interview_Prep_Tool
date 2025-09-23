import openai
import os
from datetime import datetime, timedelta
import json
import statistics

class AnalyticsDashboard:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Metrics categories
        self.metric_categories = {
            'interview_performance': [
                'total_interviews', 'success_rate', 'rejection_rate',
                'callback_rate', 'offer_rate', 'average_rounds'
            ],
            'preparation_effectiveness': [
                'prep_time_vs_success', 'most_effective_activities',
                'preparation_completion_rate', 'optimal_prep_timeline'
            ],
            'company_insights': [
                'company_success_rates', 'industry_performance',
                'company_size_correlation', 'role_type_success'
            ],
            'skill_development': [
                'skill_improvement_trends', 'weakness_identification',
                'strength_utilization', 'learning_recommendations'
            ],
            'time_analytics': [
                'interview_frequency', 'seasonal_patterns',
                'response_time_analysis', 'optimal_timing'
            ]
        }
        
        # Performance benchmarks
        self.benchmarks = {
            'success_rates': {
                'excellent': 0.80,
                'good': 0.60,
                'average': 0.40,
                'needs_improvement': 0.20
            },
            'response_times': {
                'fast': 3,      # days
                'normal': 7,    # days
                'slow': 14,     # days
                'very_slow': 21 # days
            },
            'preparation_time': {
                'phone_screening': 2,    # hours
                'technical': 8,          # hours
                'behavioral': 4,         # hours
                'final': 3               # hours
            }
        }
        
        # Industry standards
        self.industry_standards = {
            'technology': {
                'avg_interview_rounds': 4,
                'typical_timeline_days': 21,
                'success_rate': 0.15
            },
            'finance': {
                'avg_interview_rounds': 3,
                'typical_timeline_days': 14,
                'success_rate': 0.25
            },
            'consulting': {
                'avg_interview_rounds': 3,
                'typical_timeline_days': 10,
                'success_rate': 0.20
            },
            'healthcare': {
                'avg_interview_rounds': 2,
                'typical_timeline_days': 7,
                'success_rate': 0.35
            }
        }
    
    def generate_comprehensive_analytics(self, user_data):
        """Generate comprehensive analytics dashboard"""
        try:
            analytics = {
                'overview': self._generate_overview_metrics(user_data),
                'performance_trends': self._analyze_performance_trends(user_data),
                'preparation_insights': self._analyze_preparation_effectiveness(user_data),
                'company_analysis': self._analyze_company_patterns(user_data),
                'skill_insights': self._analyze_skill_development(user_data),
                'time_analysis': self._analyze_timing_patterns(user_data),
                'recommendations': self._generate_recommendations(user_data),
                'benchmarks': self._compare_to_benchmarks(user_data),
                'predictions': self._generate_predictions(user_data),
                'generated_at': datetime.now().isoformat()
            }
            
            return analytics
            
        except Exception as e:
            return {'error': str(e)}
    
    def _generate_overview_metrics(self, user_data):
        """Generate high-level overview metrics"""
        try:
            interviews = user_data.get('interviews', [])
            applications = user_data.get('applications', [])
            
            if not interviews:
                return {'message': 'No interview data available'}
            
            total_interviews = len(interviews)
            successful_interviews = len([i for i in interviews if i.get('outcome') == 'offer'])
            rejected_interviews = len([i for i in interviews if i.get('outcome') == 'rejected'])
            pending_interviews = len([i for i in interviews if i.get('outcome') == 'pending'])
            
            overview = {
                'total_interviews': total_interviews,
                'total_applications': len(applications),
                'success_rate': successful_interviews / total_interviews if total_interviews > 0 else 0,
                'rejection_rate': rejected_interviews / total_interviews if total_interviews > 0 else 0,
                'pending_rate': pending_interviews / total_interviews if total_interviews > 0 else 0,
                'interview_to_application_ratio': total_interviews / len(applications) if applications else 0,
                'current_streak': self._calculate_current_streak(interviews),
                'best_streak': self._calculate_best_streak(interviews),
                'avg_interviews_per_week': self._calculate_interview_frequency(interviews),
                'most_active_month': self._find_most_active_period(interviews)
            }
            
            return overview
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_performance_trends(self, user_data):
        """Analyze performance trends over time"""
        try:
            interviews = user_data.get('interviews', [])
            if not interviews:
                return {'message': 'No interview data for trend analysis'}
            
            # Sort interviews by date
            sorted_interviews = sorted(
                interviews, 
                key=lambda x: datetime.fromisoformat(x.get('date', '2024-01-01'))
            )
            
            trends = {
                'monthly_performance': self._calculate_monthly_trends(sorted_interviews),
                'success_rate_trend': self._calculate_success_rate_trend(sorted_interviews),
                'interview_round_trends': self._analyze_round_progression(sorted_interviews),
                'industry_performance': self._analyze_industry_performance(sorted_interviews),
                'role_level_trends': self._analyze_role_level_trends(sorted_interviews),
                'improvement_areas': self._identify_improvement_trends(sorted_interviews)
            }
            
            return trends
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_preparation_effectiveness(self, user_data):
        """Analyze preparation effectiveness"""
        try:
            interviews = user_data.get('interviews', [])
            prep_data = user_data.get('preparation_data', [])
            
            if not interviews or not prep_data:
                return {'message': 'Insufficient data for preparation analysis'}
            
            effectiveness = {
                'prep_time_correlation': self._analyze_prep_time_success(interviews, prep_data),
                'most_effective_activities': self._find_effective_prep_activities(prep_data),
                'preparation_completion_rates': self._analyze_prep_completion(prep_data),
                'optimal_prep_timeline': self._determine_optimal_timeline(prep_data),
                'skill_specific_prep': self._analyze_skill_specific_prep(prep_data),
                'prep_vs_interview_type': self._analyze_prep_by_interview_type(prep_data)
            }
            
            return effectiveness
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_company_patterns(self, user_data):
        """Analyze patterns by company and industry"""
        try:
            interviews = user_data.get('interviews', [])
            if not interviews:
                return {'message': 'No company data available'}
            
            patterns = {
                'company_success_rates': self._calculate_company_success_rates(interviews),
                'industry_analysis': self._analyze_by_industry(interviews),
                'company_size_correlation': self._analyze_by_company_size(interviews),
                'role_type_performance': self._analyze_by_role_type(interviews),
                'geographic_patterns': self._analyze_geographic_patterns(interviews),
                'timing_by_company_type': self._analyze_timing_by_company(interviews)
            }
            
            return patterns
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_skill_development(self, user_data):
        """Analyze skill development and improvement areas"""
        try:
            assessments = user_data.get('skill_assessments', [])
            interviews = user_data.get('interviews', [])
            
            if not assessments:
                return {'message': 'No skill assessment data available'}
            
            skill_insights = {
                'skill_progression': self._track_skill_progression(assessments),
                'strength_identification': self._identify_strengths(assessments),
                'weakness_areas': self._identify_weaknesses(assessments),
                'skill_interview_correlation': self._correlate_skills_success(assessments, interviews),
                'learning_recommendations': self._generate_learning_recommendations(assessments),
                'skill_gaps': self._identify_skill_gaps(assessments, interviews)
            }
            
            return skill_insights
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_timing_patterns(self, user_data):
        """Analyze timing patterns and optimal scheduling"""
        try:
            interviews = user_data.get('interviews', [])
            if not interviews:
                return {'message': 'No timing data available'}
            
            timing_analysis = {
                'best_interview_days': self._find_best_interview_days(interviews),
                'optimal_time_of_day': self._find_optimal_interview_times(interviews),
                'seasonal_patterns': self._analyze_seasonal_patterns(interviews),
                'response_time_analysis': self._analyze_response_times(interviews),
                'interview_spacing_optimization': self._analyze_interview_spacing(interviews),
                'follow_up_timing_effectiveness': self._analyze_follow_up_timing(interviews)
            }
            
            return timing_analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def _generate_recommendations(self, user_data):
        """Generate AI-powered recommendations"""
        try:
            # Analyze patterns and generate recommendations
            interviews = user_data.get('interviews', [])
            success_rate = len([i for i in interviews if i.get('outcome') == 'offer']) / len(interviews) if interviews else 0
            
            # Create context for AI recommendations
            context = f"""
            User Interview Performance Summary:
            - Total Interviews: {len(interviews)}
            - Success Rate: {success_rate:.2%}
            - Most Common Rejection Reasons: {self._get_common_rejection_reasons(interviews)}
            - Preparation Patterns: {self._summarize_prep_patterns(user_data)}
            - Industry Focus: {self._get_industry_focus(interviews)}
            """
            
            prompt = f"""
            Based on this interview performance data, provide specific, actionable recommendations for improvement:
            
            {context}
            
            Provide recommendations in these categories:
            1. Interview Performance Improvement
            2. Preparation Strategy Optimization  
            3. Application Strategy Refinement
            4. Skill Development Priorities
            5. Timing and Scheduling Optimization
            
            Make recommendations specific, measurable, and actionable.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.7
            )
            
            ai_recommendations = response.choices[0].message.content
            
            # Combine with analytical recommendations
            recommendations = {
                'ai_powered_insights': ai_recommendations,
                'data_driven_recommendations': self._generate_data_recommendations(user_data),
                'quick_wins': self._identify_quick_wins(user_data),
                'long_term_strategies': self._suggest_long_term_strategies(user_data),
                'priority_rankings': self._rank_recommendation_priorities(user_data)
            }
            
            return recommendations
            
        except Exception as e:
            return {'error': str(e)}
    
    def _compare_to_benchmarks(self, user_data):
        """Compare user performance to industry benchmarks"""
        try:
            interviews = user_data.get('interviews', [])
            if not interviews:
                return {'message': 'No data for benchmark comparison'}
            
            user_metrics = self._calculate_user_metrics(interviews)
            
            benchmark_comparison = {
                'success_rate_comparison': self._compare_success_rates(user_metrics),
                'timeline_comparison': self._compare_timelines(user_metrics),
                'preparation_time_comparison': self._compare_prep_times(user_data),
                'industry_specific_comparison': self._compare_by_industry(user_metrics, interviews),
                'percentile_rankings': self._calculate_percentile_rankings(user_metrics),
                'areas_above_benchmark': self._identify_above_benchmark_areas(user_metrics),
                'areas_below_benchmark': self._identify_below_benchmark_areas(user_metrics)
            }
            
            return benchmark_comparison
            
        except Exception as e:
            return {'error': str(e)}
    
    def _generate_predictions(self, user_data):
        """Generate predictive analytics"""
        try:
            interviews = user_data.get('interviews', [])
            if len(interviews) < 5:
                return {'message': 'Need more data for reliable predictions'}
            
            predictions = {
                'success_rate_prediction': self._predict_future_success_rate(interviews),
                'optimal_application_volume': self._predict_optimal_application_volume(user_data),
                'time_to_offer_prediction': self._predict_time_to_offer(interviews),
                'skill_development_timeline': self._predict_skill_improvement_timeline(user_data),
                'market_timing_recommendations': self._predict_optimal_timing(interviews),
                'confidence_intervals': self._calculate_prediction_confidence(interviews)
            }
            
            return predictions
            
        except Exception as e:
            return {'error': str(e)}
    
    # Helper methods for calculations
    def _calculate_current_streak(self, interviews):
        """Calculate current win/loss streak"""
        if not interviews:
            return 0
        
        sorted_interviews = sorted(interviews, key=lambda x: x.get('date', ''), reverse=True)
        current_streak = 0
        last_outcome = None
        
        for interview in sorted_interviews:
            outcome = interview.get('outcome')
            if outcome in ['offer', 'rejected']:
                if last_outcome is None:
                    last_outcome = outcome
                    current_streak = 1
                elif outcome == last_outcome:
                    current_streak += 1
                else:
                    break
        
        return current_streak if last_outcome == 'offer' else -current_streak
    
    def _calculate_best_streak(self, interviews):
        """Calculate best winning streak"""
        if not interviews:
            return 0
        
        sorted_interviews = sorted(interviews, key=lambda x: x.get('date', ''))
        best_streak = current_streak = 0
        
        for interview in sorted_interviews:
            if interview.get('outcome') == 'offer':
                current_streak += 1
                best_streak = max(best_streak, current_streak)
            elif interview.get('outcome') == 'rejected':
                current_streak = 0
        
        return best_streak
    
    def _calculate_interview_frequency(self, interviews):
        """Calculate average interviews per week"""
        if not interviews:
            return 0
        
        dates = [datetime.fromisoformat(i.get('date', '2024-01-01')) for i in interviews]
        if len(dates) < 2:
            return 0
        
        date_range = (max(dates) - min(dates)).days
        weeks = date_range / 7 if date_range > 0 else 1
        
        return len(interviews) / weeks
    
    def _find_most_active_period(self, interviews):
        """Find the most active month"""
        if not interviews:
            return None
        
        monthly_counts = {}
        for interview in interviews:
            date = datetime.fromisoformat(interview.get('date', '2024-01-01'))
            month_key = f"{date.year}-{date.month:02d}"
            monthly_counts[month_key] = monthly_counts.get(month_key, 0) + 1
        
        if monthly_counts:
            most_active = max(monthly_counts, key=monthly_counts.get)
            return {'month': most_active, 'count': monthly_counts[most_active]}
        
        return None
    
    def _calculate_monthly_trends(self, interviews):
        """Calculate monthly performance trends"""
        monthly_data = {}
        
        for interview in interviews:
            date = datetime.fromisoformat(interview.get('date', '2024-01-01'))
            month_key = f"{date.year}-{date.month:02d}"
            
            if month_key not in monthly_data:
                monthly_data[month_key] = {'total': 0, 'offers': 0, 'rejections': 0}
            
            monthly_data[month_key]['total'] += 1
            if interview.get('outcome') == 'offer':
                monthly_data[month_key]['offers'] += 1
            elif interview.get('outcome') == 'rejected':
                monthly_data[month_key]['rejections'] += 1
        
        # Calculate success rates
        for month in monthly_data:
            total = monthly_data[month]['total']
            monthly_data[month]['success_rate'] = monthly_data[month]['offers'] / total if total > 0 else 0
        
        return monthly_data
    
    def _get_common_rejection_reasons(self, interviews):
        """Get most common rejection reasons"""
        reasons = [i.get('rejection_reason', 'Unknown') for i in interviews if i.get('outcome') == 'rejected']
        if not reasons:
            return 'No rejection data available'
        
        from collections import Counter
        most_common = Counter(reasons).most_common(3)
        return [reason for reason, count in most_common]
    
    def _summarize_prep_patterns(self, user_data):
        """Summarize preparation patterns"""
        prep_data = user_data.get('preparation_data', [])
        if not prep_data:
            return 'No preparation data available'
        
        avg_prep_time = statistics.mean([p.get('time_spent', 0) for p in prep_data]) if prep_data else 0
        most_common_activity = 'Research' if prep_data else 'Unknown'
        
        return f"Average prep time: {avg_prep_time:.1f} hours, Most common activity: {most_common_activity}"
    
    def _get_industry_focus(self, interviews):
        """Get primary industry focus"""
        industries = [i.get('industry', 'Unknown') for i in interviews]
        if not industries:
            return 'Unknown'
        
        from collections import Counter
        most_common = Counter(industries).most_common(1)
        return most_common[0][0] if most_common else 'Unknown'
    
    def export_analytics_report(self, analytics_data, format='pdf'):
        """Export analytics report in specified format"""
        try:
            if format == 'pdf':
                # PDF export structure
                report = {
                    'title': 'Interview Performance Analytics Report',
                    'generated_date': datetime.now().strftime('%Y-%m-%d'),
                    'sections': [
                        {'name': 'Executive Summary', 'data': analytics_data.get('overview', {})},
                        {'name': 'Performance Trends', 'data': analytics_data.get('performance_trends', {})},
                        {'name': 'Preparation Analysis', 'data': analytics_data.get('preparation_insights', {})},
                        {'name': 'Recommendations', 'data': analytics_data.get('recommendations', {})},
                        {'name': 'Benchmarks', 'data': analytics_data.get('benchmarks', {})}
                    ]
                }
                return report
            
            elif format == 'excel':
                # Excel export structure
                workbook_data = {
                    'Overview': analytics_data.get('overview', {}),
                    'Trends': analytics_data.get('performance_trends', {}),
                    'Companies': analytics_data.get('company_analysis', {}),
                    'Skills': analytics_data.get('skill_insights', {}),
                    'Recommendations': analytics_data.get('recommendations', {})
                }
                return workbook_data
            
            elif format == 'json':
                return analytics_data
            
            return {'error': 'Unsupported export format'}
            
        except Exception as e:
            return {'error': str(e)}