import openai
import os
import json
from datetime import datetime
import random

class SkillsAssessmentTool:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Comprehensive skill categories
        self.skill_categories = {
            'programming_languages': {
                'name': 'Programming Languages',
                'skills': [
                    'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Go', 'Rust',
                    'TypeScript', 'Swift', 'Kotlin', 'PHP', 'Ruby', 'Scala'
                ],
                'assessment_type': 'technical',
                'weight': 0.25
            },
            'web_development': {
                'name': 'Web Development',
                'skills': [
                    'React', 'Angular', 'Vue.js', 'Node.js', 'Express.js',
                    'HTML5', 'CSS3', 'Sass', 'Webpack', 'Next.js', 'Django', 'Flask'
                ],
                'assessment_type': 'technical',
                'weight': 0.20
            },
            'data_science': {
                'name': 'Data Science & Analytics',
                'skills': [
                    'Machine Learning', 'Deep Learning', 'Statistics', 'Data Analysis',
                    'Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch',
                    'Tableau', 'Power BI', 'R', 'SQL', 'Big Data'
                ],
                'assessment_type': 'technical',
                'weight': 0.15
            },
            'cloud_devops': {
                'name': 'Cloud & DevOps',
                'skills': [
                    'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes',
                    'Jenkins', 'Git', 'CI/CD', 'Terraform', 'Ansible',
                    'Linux', 'Bash', 'Monitoring'
                ],
                'assessment_type': 'technical',
                'weight': 0.15
            },
            'databases': {
                'name': 'Databases & Storage',
                'skills': [
                    'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch',
                    'DynamoDB', 'Cassandra', 'Neo4j', 'SQL Server', 'Oracle'
                ],
                'assessment_type': 'technical',
                'weight': 0.10
            },
            'soft_skills': {
                'name': 'Soft Skills',
                'skills': [
                    'Leadership', 'Communication', 'Problem Solving', 'Teamwork',
                    'Project Management', 'Time Management', 'Adaptability',
                    'Critical Thinking', 'Creativity', 'Conflict Resolution'
                ],
                'assessment_type': 'behavioral',
                'weight': 0.15
            }
        }
        
        # Industry skill requirements
        self.industry_requirements = {
            'software_engineer': {
                'required': ['Programming Languages', 'Web Development', 'Databases'],
                'preferred': ['Cloud & DevOps', 'Soft Skills'],
                'bonus': ['Data Science & Analytics']
            },
            'data_scientist': {
                'required': ['Data Science & Analytics', 'Programming Languages', 'Databases'],
                'preferred': ['Cloud & DevOps', 'Soft Skills'],
                'bonus': ['Web Development']
            },
            'full_stack_developer': {
                'required': ['Programming Languages', 'Web Development', 'Databases'],
                'preferred': ['Cloud & DevOps', 'Soft Skills'],
                'bonus': ['Data Science & Analytics']
            },
            'devops_engineer': {
                'required': ['Cloud & DevOps', 'Programming Languages', 'Databases'],
                'preferred': ['Web Development', 'Soft Skills'],
                'bonus': ['Data Science & Analytics']
            }
        }
        
        # Skill levels
        self.skill_levels = {
            'beginner': {'score': 1, 'description': 'Basic understanding, learning fundamentals'},
            'intermediate': {'score': 2, 'description': 'Can work independently on simple tasks'},
            'proficient': {'score': 3, 'description': 'Solid working knowledge, handles complex tasks'},
            'advanced': {'score': 4, 'description': 'Expert level, can mentor others'},
            'expert': {'score': 5, 'description': 'Industry expert, thought leader'}
        }
        
        # Assessment questions bank
        self.assessment_questions = {
            'programming_languages': {
                'Python': [
                    {
                        'question': 'What is the difference between a list and a tuple in Python?',
                        'type': 'conceptual',
                        'difficulty': 'intermediate',
                        'answer_key': ['mutable vs immutable', 'list can be changed', 'tuple cannot be changed']
                    },
                    {
                        'question': 'Explain Python decorators and provide an example.',
                        'type': 'conceptual',
                        'difficulty': 'advanced',
                        'answer_key': ['wrapper function', 'modifies behavior', '@decorator syntax']
                    }
                ],
                'JavaScript': [
                    {
                        'question': 'What is the difference between var, let, and const?',
                        'type': 'conceptual',
                        'difficulty': 'intermediate',
                        'answer_key': ['scope differences', 'hoisting', 'mutability']
                    },
                    {
                        'question': 'Explain closures in JavaScript with an example.',
                        'type': 'conceptual',
                        'difficulty': 'advanced',
                        'answer_key': ['function inside function', 'access outer variables', 'lexical scoping']
                    }
                ]
            },
            'soft_skills': {
                'Leadership': [
                    {
                        'question': 'Describe a time when you had to lead a team through a challenging project.',
                        'type': 'behavioral',
                        'difficulty': 'intermediate',
                        'answer_key': ['STAR method', 'specific situation', 'actions taken', 'results achieved']
                    }
                ],
                'Problem Solving': [
                    {
                        'question': 'Walk me through your approach to solving a complex technical problem.',
                        'type': 'behavioral',
                        'difficulty': 'intermediate',
                        'answer_key': ['systematic approach', 'break down problem', 'research solutions', 'test and validate']
                    }
                ]
            }
        }
    
    def create_assessment(self, target_role='software_engineer', skill_focus=None, duration_minutes=30):
        """Create a personalized skills assessment"""
        try:
            # Get role requirements
            role_reqs = self.industry_requirements.get(target_role, self.industry_requirements['software_engineer'])
            
            # Calculate questions per category
            total_questions = min(duration_minutes // 2, 20)  # 2 minutes per question, max 20
            
            assessment = {
                'id': f"assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'target_role': target_role,
                'skill_focus': skill_focus,
                'duration_minutes': duration_minutes,
                'total_questions': total_questions,
                'categories': [],
                'questions': [],
                'created_at': datetime.now().isoformat(),
                'status': 'created'
            }
            
            # Select categories based on role requirements
            selected_categories = []
            for category_name in role_reqs['required']:
                category_key = self._get_category_key(category_name)
                if category_key:
                    selected_categories.append(category_key)
            
            # Add preferred categories if we have room
            for category_name in role_reqs['preferred']:
                category_key = self._get_category_key(category_name)
                if category_key and len(selected_categories) < 4:
                    selected_categories.append(category_key)
            
            # Generate questions for each category
            questions_per_category = max(1, total_questions // len(selected_categories))
            
            for category_key in selected_categories:
                category = self.skill_categories[category_key]
                assessment['categories'].append({
                    'key': category_key,
                    'name': category['name'],
                    'weight': category['weight'],
                    'question_count': questions_per_category
                })
                
                # Generate category questions
                category_questions = self._generate_category_questions(
                    category_key, questions_per_category, target_role
                )
                assessment['questions'].extend(category_questions)
            
            return assessment
            
        except Exception as e:
            print(f"Assessment creation error: {e}")
            return {'error': str(e)}
    
    def _get_category_key(self, category_name):
        """Get category key from display name"""
        for key, category in self.skill_categories.items():
            if category['name'] == category_name:
                return key
        return None
    
    def _generate_category_questions(self, category_key, count, target_role):
        """Generate questions for a specific category"""
        questions = []
        category = self.skill_categories[category_key]
        
        if category['assessment_type'] == 'technical':
            questions = self._generate_technical_questions(category_key, count, target_role)
        else:
            questions = self._generate_behavioral_questions(category_key, count)
        
        return questions
    
    def _generate_technical_questions(self, category_key, count, target_role):
        """Generate technical questions using AI"""
        try:
            category = self.skill_categories[category_key]
            skills = category['skills']
            
            # Select most relevant skills for the role
            relevant_skills = random.sample(skills, min(count, len(skills)))
            
            questions = []
            for i, skill in enumerate(relevant_skills):
                # Try to get from question bank first
                if (category_key in self.assessment_questions and 
                    skill in self.assessment_questions[category_key]):
                    bank_questions = self.assessment_questions[category_key][skill]
                    question_data = random.choice(bank_questions)
                else:
                    # Generate with AI
                    question_data = self._generate_ai_question(skill, category_key, target_role)
                
                questions.append({
                    'id': f"q_{category_key}_{i+1}",
                    'category': category_key,
                    'skill': skill,
                    'question': question_data['question'],
                    'type': question_data.get('type', 'conceptual'),
                    'difficulty': question_data.get('difficulty', 'intermediate'),
                    'points': self._calculate_question_points(question_data.get('difficulty', 'intermediate')),
                    'time_limit_minutes': 3
                })
            
            return questions
            
        except Exception as e:
            print(f"Technical question generation error: {e}")
            return []
    
    def _generate_behavioral_questions(self, category_key, count):
        """Generate behavioral questions"""
        try:
            category = self.skill_categories[category_key]
            skills = category['skills']
            
            relevant_skills = random.sample(skills, min(count, len(skills)))
            questions = []
            
            for i, skill in enumerate(relevant_skills):
                if (category_key in self.assessment_questions and 
                    skill in self.assessment_questions[category_key]):
                    bank_questions = self.assessment_questions[category_key][skill]
                    question_data = random.choice(bank_questions)
                else:
                    question_data = {
                        'question': f"Describe a situation where you demonstrated {skill.lower()}. What was the situation, what actions did you take, and what was the result?",
                        'type': 'behavioral',
                        'difficulty': 'intermediate'
                    }
                
                questions.append({
                    'id': f"q_{category_key}_{i+1}",
                    'category': category_key,
                    'skill': skill,
                    'question': question_data['question'],
                    'type': 'behavioral',
                    'difficulty': question_data.get('difficulty', 'intermediate'),
                    'points': self._calculate_question_points(question_data.get('difficulty', 'intermediate')),
                    'time_limit_minutes': 5
                })
            
            return questions
            
        except Exception as e:
            print(f"Behavioral question generation error: {e}")
            return []
    
    def _generate_ai_question(self, skill, category_key, target_role):
        """Generate AI-powered question for a skill"""
        try:
            prompt = f"""
            Generate a technical interview question for the skill: {skill}
            Category: {category_key}
            Target role: {target_role}
            
            Requirements:
            - Question should test practical knowledge
            - Appropriate for intermediate level
            - Clear and specific
            - Can be answered in 2-3 minutes
            
            Return only the question text.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7
            )
            
            return {
                'question': response.choices[0].message.content.strip(),
                'type': 'conceptual',
                'difficulty': 'intermediate'
            }
            
        except Exception as e:
            return {
                'question': f"Explain your experience with {skill} and how you've used it in projects.",
                'type': 'general',
                'difficulty': 'intermediate'
            }
    
    def _calculate_question_points(self, difficulty):
        """Calculate points for a question based on difficulty"""
        points_map = {
            'beginner': 1,
            'intermediate': 2,
            'advanced': 3,
            'expert': 4
        }
        return points_map.get(difficulty, 2)
    
    def evaluate_assessment(self, assessment_id, responses):
        """Evaluate completed assessment and provide results"""
        try:
            # Calculate scores by category
            category_scores = {}
            total_points = 0
            earned_points = 0
            
            for response in responses:
                category = response['category']
                points = response.get('points', 2)
                score = self._evaluate_response(response)
                
                total_points += points
                earned_points += score * points
                
                if category not in category_scores:
                    category_scores[category] = {'total': 0, 'earned': 0, 'count': 0}
                
                category_scores[category]['total'] += points
                category_scores[category]['earned'] += score * points
                category_scores[category]['count'] += 1
            
            # Calculate overall score
            overall_score = (earned_points / total_points * 100) if total_points > 0 else 0
            
            # Generate detailed results
            results = {
                'assessment_id': assessment_id,
                'overall_score': round(overall_score, 1),
                'total_questions': len(responses),
                'category_breakdown': self._create_category_breakdown(category_scores),
                'skill_gaps': self._identify_skill_gaps(category_scores),
                'recommendations': self._generate_skill_recommendations(category_scores, overall_score),
                'next_steps': self._suggest_next_steps(category_scores),
                'completed_at': datetime.now().isoformat()
            }
            
            return results
            
        except Exception as e:
            print(f"Assessment evaluation error: {e}")
            return {'error': str(e)}
    
    def _evaluate_response(self, response):
        """Evaluate a single response and return score (0-1)"""
        # Simple evaluation - in production, this would use more sophisticated AI
        answer = response.get('answer', '').strip()
        
        if not answer:
            return 0
        
        # Basic scoring based on answer length and content
        if len(answer) < 20:
            return 0.3
        elif len(answer) < 100:
            return 0.6
        else:
            return 0.8
    
    def _create_category_breakdown(self, category_scores):
        """Create detailed breakdown by category"""
        breakdown = {}
        
        for category_key, scores in category_scores.items():
            category_name = self.skill_categories[category_key]['name']
            percentage = (scores['earned'] / scores['total'] * 100) if scores['total'] > 0 else 0
            
            breakdown[category_key] = {
                'name': category_name,
                'score_percentage': round(percentage, 1),
                'questions_answered': scores['count'],
                'level': self._determine_skill_level(percentage)
            }
        
        return breakdown
    
    def _determine_skill_level(self, percentage):
        """Determine skill level based on percentage"""
        if percentage >= 85:
            return 'expert'
        elif percentage >= 70:
            return 'advanced'
        elif percentage >= 55:
            return 'proficient'
        elif percentage >= 40:
            return 'intermediate'
        else:
            return 'beginner'
    
    def _identify_skill_gaps(self, category_scores):
        """Identify areas that need improvement"""
        gaps = []
        
        for category_key, scores in category_scores.items():
            percentage = (scores['earned'] / scores['total'] * 100) if scores['total'] > 0 else 0
            category_name = self.skill_categories[category_key]['name']
            
            if percentage < 60:
                gap_severity = 'high' if percentage < 40 else 'medium'
                gaps.append({
                    'category': category_name,
                    'current_level': self._determine_skill_level(percentage),
                    'severity': gap_severity,
                    'improvement_needed': round(70 - percentage, 1) if percentage < 70 else 0
                })
        
        return gaps
    
    def _generate_skill_recommendations(self, category_scores, overall_score):
        """Generate personalized skill improvement recommendations"""
        recommendations = []
        
        # Overall recommendations
        if overall_score < 50:
            recommendations.append({
                'type': 'general',
                'priority': 'high',
                'recommendation': 'Focus on fundamental skill building across all areas'
            })
        elif overall_score < 70:
            recommendations.append({
                'type': 'general',
                'priority': 'medium',
                'recommendation': 'Strengthen weak areas while maintaining strong skills'
            })
        
        # Category-specific recommendations
        for category_key, scores in category_scores.items():
            percentage = (scores['earned'] / scores['total'] * 100) if scores['total'] > 0 else 0
            category_name = self.skill_categories[category_key]['name']
            
            if percentage < 60:
                recommendations.append({
                    'type': 'skill_specific',
                    'category': category_name,
                    'priority': 'high' if percentage < 40 else 'medium',
                    'recommendation': f'Dedicate 2-3 hours weekly to improve {category_name} skills'
                })
        
        return recommendations
    
    def _suggest_next_steps(self, category_scores):
        """Suggest concrete next steps for improvement"""
        next_steps = []
        
        for category_key, scores in category_scores.items():
            percentage = (scores['earned'] / scores['total'] * 100) if scores['total'] > 0 else 0
            category = self.skill_categories[category_key]
            
            if percentage < 70:
                # Suggest specific learning resources
                steps = self._get_learning_resources(category_key, percentage)
                next_steps.extend(steps)
        
        return next_steps[:10]  # Limit to top 10 steps
    
    def _get_learning_resources(self, category_key, current_percentage):
        """Get learning resources for a category"""
        resources = {
            'programming_languages': [
                'Complete online courses in weak programming languages',
                'Build practical projects using target languages',
                'Contribute to open source projects',
                'Practice coding challenges daily'
            ],
            'web_development': [
                'Build full-stack web applications',
                'Follow modern web development tutorials',
                'Learn React/Angular/Vue framework',
                'Practice responsive design principles'
            ],
            'data_science': [
                'Complete machine learning courses',
                'Work on Kaggle competitions',
                'Build data analysis projects',
                'Learn statistical analysis fundamentals'
            ],
            'cloud_devops': [
                'Get AWS/Azure certifications',
                'Practice with Docker and Kubernetes',
                'Set up CI/CD pipelines',
                'Learn infrastructure as code'
            ],
            'soft_skills': [
                'Practice communication skills',
                'Take leadership courses',
                'Join professional groups',
                'Seek mentoring opportunities'
            ]
        }
        
        category_resources = resources.get(category_key, ['General skill improvement'])
        
        # Prioritize based on current level
        if current_percentage < 40:
            return [f"Beginner: {resource}" for resource in category_resources[:2]]
        else:
            return [f"Intermediate: {resource}" for resource in category_resources[2:4]]
    
    def generate_study_plan(self, assessment_results, target_role, timeline_weeks=12):
        """Generate a personalized study plan based on assessment results"""
        try:
            study_plan = {
                'timeline_weeks': timeline_weeks,
                'target_role': target_role,
                'focus_areas': [],
                'weekly_schedule': {},
                'milestones': [],
                'resources': {}
            }
            
            # Identify focus areas from gaps
            skill_gaps = assessment_results.get('skill_gaps', [])
            high_priority_gaps = [gap for gap in skill_gaps if gap['severity'] == 'high']
            medium_priority_gaps = [gap for gap in skill_gaps if gap['severity'] == 'medium']
            
            # Create focus areas
            for gap in high_priority_gaps[:3]:  # Top 3 high priority
                study_plan['focus_areas'].append({
                    'category': gap['category'],
                    'priority': 'high',
                    'current_level': gap['current_level'],
                    'target_level': 'proficient',
                    'weekly_hours': 4
                })
            
            for gap in medium_priority_gaps[:2]:  # Top 2 medium priority
                study_plan['focus_areas'].append({
                    'category': gap['category'],
                    'priority': 'medium',
                    'current_level': gap['current_level'],
                    'target_level': 'intermediate',
                    'weekly_hours': 2
                })
            
            # Generate weekly schedule
            study_plan['weekly_schedule'] = self._create_weekly_schedule(study_plan['focus_areas'])
            
            # Create milestones
            study_plan['milestones'] = self._create_learning_milestones(timeline_weeks, study_plan['focus_areas'])
            
            # Add resources
            study_plan['resources'] = self._compile_learning_resources(study_plan['focus_areas'])
            
            return study_plan
            
        except Exception as e:
            print(f"Study plan generation error: {e}")
            return {'error': str(e)}
    
    def _create_weekly_schedule(self, focus_areas):
        """Create a weekly learning schedule"""
        schedule = {
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': [],
            'sunday': []
        }
        
        days = list(schedule.keys())
        day_index = 0
        
        for area in focus_areas:
            hours = area['weekly_hours']
            sessions = max(1, hours // 2)  # 2-hour sessions
            
            for _ in range(sessions):
                day = days[day_index % len(days)]
                schedule[day].append({
                    'category': area['category'],
                    'duration_hours': min(2, hours / sessions),
                    'activity': f"Study {area['category']}"
                })
                day_index += 1
        
        return schedule
    
    def _create_learning_milestones(self, timeline_weeks, focus_areas):
        """Create learning milestones"""
        milestones = []
        
        # Week 2 milestone
        milestones.append({
            'week': 2,
            'title': 'Foundation Assessment',
            'description': 'Complete basic learning in all focus areas',
            'deliverables': ['Basic concepts understood', 'Learning routine established']
        })
        
        # Mid-point milestone
        mid_week = timeline_weeks // 2
        milestones.append({
            'week': mid_week,
            'title': 'Mid-Point Evaluation',
            'description': 'Assess progress and adjust plan',
            'deliverables': ['Mini-projects completed', 'Skills reassessment']
        })
        
        # Final milestone
        milestones.append({
            'week': timeline_weeks,
            'title': 'Final Assessment',
            'description': 'Complete study plan and validate improvements',
            'deliverables': ['Portfolio projects', 'Skills certification', 'Interview readiness']
        })
        
        return milestones
    
    def _compile_learning_resources(self, focus_areas):
        """Compile learning resources for focus areas"""
        resources = {}
        
        resource_database = {
            'Programming Languages': {
                'courses': ['Codecademy Python', 'freeCodeCamp JavaScript'],
                'books': ['Automate the Boring Stuff with Python', 'Eloquent JavaScript'],
                'practice': ['LeetCode', 'HackerRank', 'Codewars']
            },
            'Web Development': {
                'courses': ['React Official Tutorial', 'The Odin Project'],
                'books': ['You Don\'t Know JS', 'HTML and CSS by Jon Duckett'],
                'practice': ['Build personal website', 'Clone existing websites']
            },
            'Data Science & Analytics': {
                'courses': ['Coursera ML Course', 'Kaggle Learn'],
                'books': ['Hands-On Machine Learning', 'Python for Data Analysis'],
                'practice': ['Kaggle competitions', 'Personal data projects']
            }
        }
        
        for area in focus_areas:
            category = area['category']
            resources[category] = resource_database.get(category, {
                'courses': ['Online courses for ' + category],
                'books': ['Technical books for ' + category],
                'practice': ['Hands-on projects for ' + category]
            })
        
        return resources
    
    def track_progress(self, user_id, study_plan_id, week_number, completed_activities):
        """Track learning progress"""
        try:
            progress_entry = {
                'user_id': user_id,
                'study_plan_id': study_plan_id,
                'week_number': week_number,
                'completed_activities': completed_activities,
                'completion_rate': len(completed_activities) / 7 * 100,  # Assuming 7 activities per week
                'recorded_at': datetime.now().isoformat()
            }
            
            # In a real app, this would be saved to database
            return progress_entry
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_skill_benchmarks(self, target_role):
        """Get industry skill benchmarks for a role"""
        benchmarks = {
            'software_engineer': {
                'Programming Languages': {'min': 70, 'target': 85},
                'Web Development': {'min': 65, 'target': 80},
                'Databases & Storage': {'min': 60, 'target': 75},
                'Cloud & DevOps': {'min': 50, 'target': 70},
                'Soft Skills': {'min': 70, 'target': 85}
            },
            'data_scientist': {
                'Data Science & Analytics': {'min': 80, 'target': 90},
                'Programming Languages': {'min': 75, 'target': 85},
                'Databases & Storage': {'min': 70, 'target': 80},
                'Soft Skills': {'min': 75, 'target': 85}
            }
        }
        
        return benchmarks.get(target_role, benchmarks['software_engineer'])