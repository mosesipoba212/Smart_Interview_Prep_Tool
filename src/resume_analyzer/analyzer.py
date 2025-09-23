import openai
import os
import re
from datetime import datetime
import PyPDF2
from docx import Document
from io import BytesIO

class ResumeAnalyzer:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Key sections to analyze
        self.resume_sections = [
            'contact_info', 'summary', 'experience', 'education', 
            'skills', 'projects', 'achievements', 'certifications'
        ]
        
        # Industry-specific keywords
        self.industry_keywords = {
            'software_engineering': [
                'Python', 'JavaScript', 'Java', 'React', 'Node.js', 'AWS', 'Docker',
                'Kubernetes', 'Git', 'SQL', 'MongoDB', 'REST API', 'Microservices',
                'Machine Learning', 'Data Structures', 'Algorithms', 'Agile', 'CI/CD'
            ],
            'data_science': [
                'Python', 'R', 'SQL', 'Machine Learning', 'Deep Learning', 'TensorFlow',
                'PyTorch', 'Pandas', 'NumPy', 'Scikit-learn', 'Tableau', 'Power BI',
                'Statistics', 'A/B Testing', 'Big Data', 'Spark', 'Hadoop'
            ],
            'product_management': [
                'Product Strategy', 'Roadmapping', 'User Research', 'A/B Testing',
                'Analytics', 'Agile', 'Scrum', 'JIRA', 'SQL', 'Data Analysis',
                'Market Research', 'User Experience', 'Stakeholder Management'
            ],
            'marketing': [
                'Digital Marketing', 'SEO', 'SEM', 'Social Media', 'Content Marketing',
                'Email Marketing', 'Analytics', 'Google Analytics', 'A/B Testing',
                'Campaign Management', 'Brand Management', 'Lead Generation'
            ]
        }
        
        # ATS optimization rules
        self.ats_rules = {
            'formatting': [
                'Use standard section headers',
                'Avoid images, graphics, and fancy formatting',
                'Use simple bullet points',
                'Stick to standard fonts',
                'Save as PDF or Word document'
            ],
            'keywords': [
                'Include job-relevant keywords naturally',
                'Match job description terminology',
                'Use both acronyms and full terms',
                'Include technical skills prominently'
            ],
            'structure': [
                'Contact info at top',
                'Clear section divisions',
                'Consistent formatting',
                'Logical flow of information',
                'Quantified achievements'
            ]
        }
    
    def analyze_resume_text(self, text, target_role='software_engineer', target_company=None):
        """Analyze resume text and provide comprehensive feedback"""
        try:
            # Basic analysis
            word_count = len(text.split())
            sections_found = self._identify_sections(text)
            keywords_analysis = self._analyze_keywords(text, target_role)
            
            # AI-powered deep analysis
            ai_analysis = self._get_ai_analysis(text, target_role, target_company)
            
            # ATS optimization score
            ats_score = self._calculate_ats_score(text, sections_found, keywords_analysis)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                sections_found, keywords_analysis, ats_score, target_role
            )
            
            return {
                'overall_score': self._calculate_overall_score(sections_found, keywords_analysis, ats_score),
                'word_count': word_count,
                'sections_analysis': sections_found,
                'keywords_analysis': keywords_analysis,
                'ats_score': ats_score,
                'ai_insights': ai_analysis,
                'recommendations': recommendations,
                'target_role': target_role,
                'analyzed_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Resume analysis error: {e}")
            return {
                'error': 'Failed to analyze resume',
                'message': str(e)
            }
    
    def _identify_sections(self, text):
        """Identify and analyze resume sections"""
        sections = {}
        text_lower = text.lower()
        
        # Common section patterns
        section_patterns = {
            'contact_info': r'(email|phone|linkedin|github)',
            'summary': r'(summary|objective|profile)',
            'experience': r'(experience|employment|work history)',
            'education': r'(education|degree|university|college)',
            'skills': r'(skills|technologies|technical skills)',
            'projects': r'(projects|portfolio)',
            'achievements': r'(achievements|awards|honors)',
            'certifications': r'(certifications|certificates)'
        }
        
        for section, pattern in section_patterns.items():
            if re.search(pattern, text_lower):
                sections[section] = {
                    'found': True,
                    'quality': self._assess_section_quality(text, section)
                }
            else:
                sections[section] = {'found': False, 'quality': 0}
        
        return sections
    
    def _assess_section_quality(self, text, section):
        """Assess the quality of a specific section"""
        # Simple quality scoring based on content length and keywords
        section_keywords = {
            'experience': ['years', 'led', 'managed', 'developed', 'improved', 'increased'],
            'skills': ['proficient', 'experienced', 'advanced', 'expert'],
            'projects': ['built', 'created', 'developed', 'implemented'],
            'achievements': ['award', 'recognition', 'top', 'best', 'exceeded']
        }
        
        if section not in section_keywords:
            return 7  # Default score
        
        keywords = section_keywords[section]
        text_lower = text.lower()
        found_keywords = sum(1 for keyword in keywords if keyword in text_lower)
        
        return min(10, 5 + found_keywords)
    
    def _analyze_keywords(self, text, target_role):
        """Analyze keyword density and relevance"""
        if target_role not in self.industry_keywords:
            target_role = 'software_engineering'
        
        relevant_keywords = self.industry_keywords[target_role]
        text_lower = text.lower()
        
        found_keywords = []
        missing_keywords = []
        
        for keyword in relevant_keywords:
            if keyword.lower() in text_lower:
                found_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        keyword_density = len(found_keywords) / len(relevant_keywords) * 100
        
        return {
            'found_keywords': found_keywords,
            'missing_keywords': missing_keywords[:10],  # Top 10 missing
            'keyword_density': round(keyword_density, 1),
            'total_relevant_keywords': len(relevant_keywords)
        }
    
    def _calculate_ats_score(self, text, sections, keywords):
        """Calculate ATS optimization score"""
        score = 0
        
        # Section completeness (40%)
        essential_sections = ['contact_info', 'experience', 'skills', 'education']
        sections_score = sum(1 for section in essential_sections if sections[section]['found'])
        score += (sections_score / len(essential_sections)) * 40
        
        # Keyword density (35%)
        keyword_score = min(keywords['keyword_density'], 80) / 80 * 35
        score += keyword_score
        
        # Text quality indicators (25%)
        quality_indicators = [
            len(text) > 200,  # Sufficient content
            len(text) < 2000,  # Not too long
            '@' in text,  # Email present
            any(word in text.lower() for word in ['improved', 'increased', 'led', 'managed']),  # Action words
            any(char.isdigit() for char in text)  # Quantified results
        ]
        quality_score = sum(quality_indicators) / len(quality_indicators) * 25
        score += quality_score
        
        return round(score, 1)
    
    def _get_ai_analysis(self, text, target_role, target_company=None):
        """Get AI-powered analysis of resume"""
        try:
            company_context = f" for {target_company}" if target_company else ""
            
            prompt = f"""
            Analyze this resume for a {target_role} position{company_context}. Provide specific feedback on:
            
            1. Overall impression and strength
            2. Key strengths that stand out
            3. Areas that need improvement
            4. Missing elements for the target role
            5. Specific suggestions for enhancement
            
            Resume text:
            {text[:2000]}  # Limit to avoid token limits
            
            Provide actionable, specific feedback in a professional tone.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.7
            )
            
            return {
                'analysis': response.choices[0].message.content,
                'ai_powered': True
            }
            
        except Exception as e:
            return {
                'analysis': 'AI analysis unavailable. Please use the detailed recommendations below.',
                'ai_powered': False,
                'error': str(e)
            }
    
    def _calculate_overall_score(self, sections, keywords, ats_score):
        """Calculate overall resume score"""
        # Weighted scoring
        section_score = sum(1 for section in sections.values() if section['found']) / len(sections) * 100
        keyword_score = keywords['keyword_density']
        
        overall = (section_score * 0.3 + keyword_score * 0.4 + ats_score * 0.3)
        return round(overall, 1)
    
    def _generate_recommendations(self, sections, keywords, ats_score, target_role):
        """Generate specific recommendations for improvement"""
        recommendations = {
            'high_priority': [],
            'medium_priority': [],
            'low_priority': [],
            'ats_optimization': [],
            'content_improvements': []
        }
        
        # High priority recommendations
        missing_essential = [s for s, data in sections.items() if not data['found'] and s in ['experience', 'skills', 'contact_info']]
        if missing_essential:
            recommendations['high_priority'].append(f"Add missing essential sections: {', '.join(missing_essential)}")
        
        if keywords['keyword_density'] < 30:
            recommendations['high_priority'].append("Increase relevant keyword density - add more technical skills and industry terms")
        
        # Medium priority recommendations
        if ats_score < 70:
            recommendations['medium_priority'].append("Improve ATS optimization for better applicant tracking system compatibility")
        
        if keywords['keyword_density'] < 50:
            recommendations['medium_priority'].extend([
                f"Consider adding these relevant keywords: {', '.join(keywords['missing_keywords'][:5])}",
                "Ensure job description keywords are naturally incorporated"
            ])
        
        # ATS optimization
        recommendations['ats_optimization'].extend([
            "Use standard section headers (Experience, Education, Skills)",
            "Include both acronyms and full terms (e.g., 'AI' and 'Artificial Intelligence')",
            "Use simple bullet points and avoid fancy formatting",
            "Save resume as PDF to preserve formatting",
            "Include relevant keywords naturally in context"
        ])
        
        # Content improvements
        recommendations['content_improvements'].extend([
            "Quantify achievements with specific numbers and percentages",
            "Use strong action verbs (led, developed, improved, increased)",
            "Tailor content specifically to the target role",
            "Include relevant projects that demonstrate skills",
            "Keep descriptions concise but impactful"
        ])
        
        return recommendations
    
    def extract_text_from_pdf(self, pdf_file):
        """Extract text from PDF resume"""
        try:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"PDF extraction error: {e}")
            return None
    
    def extract_text_from_docx(self, docx_file):
        """Extract text from Word document"""
        try:
            doc = Document(docx_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"DOCX extraction error: {e}")
            return None
    
    def optimize_for_ats(self, text, target_keywords):
        """Suggest ATS optimizations"""
        suggestions = []
        
        # Check keyword usage
        text_lower = text.lower()
        missing_keywords = [kw for kw in target_keywords if kw.lower() not in text_lower]
        
        if missing_keywords:
            suggestions.append({
                'type': 'keywords',
                'priority': 'high',
                'suggestion': f"Add these relevant keywords: {', '.join(missing_keywords[:5])}",
                'keywords': missing_keywords
            })
        
        # Check formatting
        if '@' not in text:
            suggestions.append({
                'type': 'contact',
                'priority': 'high',
                'suggestion': 'Include email address in contact information'
            })
        
        # Check quantification
        if not any(char.isdigit() for char in text):
            suggestions.append({
                'type': 'quantification',
                'priority': 'medium',
                'suggestion': 'Add quantified achievements (percentages, numbers, metrics)'
            })
        
        return suggestions
    
    def generate_improvement_report(self, analysis):
        """Generate a comprehensive improvement report"""
        report = {
            'executive_summary': self._create_executive_summary(analysis),
            'score_breakdown': {
                'overall_score': analysis['overall_score'],
                'ats_score': analysis['ats_score'],
                'keyword_density': analysis['keywords_analysis']['keyword_density']
            },
            'action_items': self._prioritize_action_items(analysis['recommendations']),
            'before_after_tips': self._generate_before_after_tips(),
            'industry_benchmarks': self._get_industry_benchmarks(analysis['target_role'])
        }
        
        return report
    
    def _create_executive_summary(self, analysis):
        """Create executive summary of analysis"""
        score = analysis['overall_score']
        
        if score >= 80:
            summary = "Your resume is strong and well-optimized for your target role."
        elif score >= 60:
            summary = "Your resume has good fundamentals but needs some improvements."
        else:
            summary = "Your resume needs significant improvements to be competitive."
        
        key_areas = []
        if analysis['ats_score'] < 70:
            key_areas.append("ATS optimization")
        if analysis['keywords_analysis']['keyword_density'] < 40:
            key_areas.append("keyword relevance")
        
        if key_areas:
            summary += f" Focus on improving: {', '.join(key_areas)}."
        
        return summary
    
    def _prioritize_action_items(self, recommendations):
        """Prioritize action items by impact"""
        all_items = []
        
        for priority, items in recommendations.items():
            for item in items:
                all_items.append({
                    'action': item,
                    'priority': priority,
                    'estimated_impact': self._estimate_impact(item, priority)
                })
        
        # Sort by priority and impact
        priority_order = {'high_priority': 3, 'medium_priority': 2, 'low_priority': 1}
        all_items.sort(key=lambda x: (priority_order.get(x['priority'], 1), x['estimated_impact']), reverse=True)
        
        return all_items[:10]  # Top 10 action items
    
    def _estimate_impact(self, item, priority):
        """Estimate the impact of an action item"""
        high_impact_keywords = ['keyword', 'essential', 'missing', 'ATS']
        medium_impact_keywords = ['improve', 'add', 'quantify']
        
        item_lower = item.lower()
        
        if any(keyword in item_lower for keyword in high_impact_keywords):
            return 3
        elif any(keyword in item_lower for keyword in medium_impact_keywords):
            return 2
        else:
            return 1
    
    def _generate_before_after_tips(self):
        """Generate before/after examples"""
        return {
            'experience_bullets': {
                'before': "Worked on web development projects",
                'after': "Developed 5 responsive web applications using React and Node.js, improving user engagement by 40%"
            },
            'skills_section': {
                'before': "Programming languages: Python, JavaScript",
                'after': "Technical Skills: Python (3+ years), JavaScript/React (2+ years), AWS (certified), Docker/Kubernetes"
            },
            'achievements': {
                'before': "Led team projects successfully",
                'after': "Led cross-functional team of 8 developers, delivering projects 15% ahead of schedule and reducing bugs by 30%"
            }
        }
    
    def _get_industry_benchmarks(self, target_role):
        """Get industry benchmarks for the role"""
        benchmarks = {
            'software_engineer': {
                'keyword_density': 45,
                'ats_score': 75,
                'sections_required': ['contact_info', 'summary', 'experience', 'skills', 'projects']
            },
            'data_scientist': {
                'keyword_density': 50,
                'ats_score': 70,
                'sections_required': ['contact_info', 'summary', 'experience', 'skills', 'education']
            },
            'product_manager': {
                'keyword_density': 40,
                'ats_score': 80,
                'sections_required': ['contact_info', 'summary', 'experience', 'skills', 'achievements']
            }
        }
        
        return benchmarks.get(target_role, benchmarks['software_engineer'])
    
    def compare_to_job_description(self, resume_text, job_description):
        """Compare resume to job description for gap analysis"""
        try:
            prompt = f"""
            Compare this resume to the job description and identify:
            1. Matching qualifications and skills
            2. Missing requirements from the resume
            3. Gaps that need to be addressed
            4. Strengths that align well
            5. Suggested improvements for better alignment
            
            Job Description:
            {job_description[:1000]}
            
            Resume:
            {resume_text[:1000]}
            
            Provide specific, actionable feedback.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            return {
                'comparison_analysis': response.choices[0].message.content,
                'match_score': self._calculate_match_score(resume_text, job_description)
            }
            
        except Exception as e:
            return {
                'comparison_analysis': 'Job description comparison unavailable',
                'error': str(e)
            }
    
    def _calculate_match_score(self, resume_text, job_description):
        """Calculate how well resume matches job description"""
        # Simple keyword overlap analysis
        resume_words = set(resume_text.lower().split())
        job_words = set(job_description.lower().split())
        
        # Filter out common words
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are', 'was', 'were', 'will', 'be', 'have', 'has', 'had'}
        resume_words -= common_words
        job_words -= common_words
        
        overlap = len(resume_words.intersection(job_words))
        total_job_words = len(job_words)
        
        if total_job_words == 0:
            return 0
        
        match_score = (overlap / total_job_words) * 100
        return round(min(match_score, 100), 1)