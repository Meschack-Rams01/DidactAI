"""
AI Generation Services using Google Gemini API

This module provides services for generating educational content using AI.
"""

import json
import time
from typing import Dict, List, Optional, Any
import google.generativeai as genai
from django.conf import settings
from langdetect import detect
import logging

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for interacting with Google Gemini API"""
    
    def __init__(self):
        # Configure Gemini with API key
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.max_retries = 2
        self.base_delay = 1
    
    def generate_content(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Generate content using Gemini API with enhanced error handling
        
        Args:
            prompt: The input prompt
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the response and metadata
        """
        start_time = time.time()
        
        for attempt in range(self.max_retries + 1):
            try:
                response = self.model.generate_content(prompt)
                processing_time = time.time() - start_time
                
                return {
                    'success': True,
                    'content': response.text,
                    'tokens_used': len(prompt.split()) + len(response.text.split()),  # Approximate
                    'processing_time': processing_time,
                    'error': None
                }
                
            except Exception as e:
                error_str = str(e)
                processing_time = time.time() - start_time
                
                # Check if it's a quota error
                if '429' in error_str and 'quota' in error_str.lower():
                    logger.warning(f"Quota exceeded on attempt {attempt + 1}: {error_str}")
                    
                    # Extract retry delay if available
                    import re
                    retry_match = re.search(r'retry in (\d+\.?\d*)s', error_str)
                    if retry_match and attempt < self.max_retries:
                        retry_delay = min(float(retry_match.group(1)), 30)  # Cap at 30 seconds
                        logger.info(f"Waiting {retry_delay}s before retry...")
                        time.sleep(retry_delay)
                        continue
                    
                    # If no retry delay or last attempt, return quota error with helpful message
                    return {
                        'success': False,
                        'content': None,
                        'tokens_used': 0,
                        'processing_time': processing_time,
                        'error': 'QUOTA_EXCEEDED',
                        'quota_error': True,
                        'original_error': error_str,
                        'help_message': 'Daily API quota exceeded. Please upgrade billing or try again tomorrow.'
                    }
                
                # For other errors, use exponential backoff
                if attempt < self.max_retries:
                    delay = self.base_delay * (2 ** attempt)
                    logger.warning(f"API error on attempt {attempt + 1}, retrying in {delay}s: {error_str}")
                    time.sleep(delay)
                    continue
                
                # Final attempt failed
                logger.error(f"Gemini API error after all retries: {error_str}")
                return {
                    'success': False,
                    'content': None,
                    'tokens_used': 0,
                    'processing_time': processing_time,
                    'error': error_str
                }


class QuizGenerator:
    """Service for generating quiz questions"""
    
    def __init__(self):
        self.gemini = GeminiService()
    
    def generate_quiz(self, content: str, language: str = 'en', 
                     num_questions: int = 10, difficulty: str = 'medium',
                     question_types: List[str] = None) -> Dict[str, Any]:
        """
        Generate quiz questions from content
        
        Args:
            content: Source content for quiz generation
            language: Target language for questions
            num_questions: Number of questions to generate
            difficulty: Difficulty level (easy, medium, hard)
            question_types: Types of questions to generate
            
        Returns:
            Dict containing generated quiz data
        """
        if question_types is None:
            question_types = ['multiple_choice', 'true_false', 'short_answer']
        
        # Detect source language if not specified
        detected_lang = detect(content) if content else 'en'
        
        # Create prompt for quiz generation
        prompt = self._create_quiz_prompt(
            content, language, num_questions, difficulty, question_types
        )
        # Generate content
        result = self.gemini.generate_content(prompt)
        
        if result['success']:
            try:
                # Parse the generated quiz
                quiz_data = self._parse_quiz_response(result['content'])
                quiz_data.update({
                    'metadata': {
                        'source_language': detected_lang,
                        'target_language': language,
                        'difficulty': difficulty,
                        'tokens_used': result['tokens_used'],
                        'processing_time': result['processing_time']
                    }
                })
                return quiz_data
            except Exception as e:
                logger.error(f"Error parsing quiz response: {str(e)}")
                return {
                    'success': False,
                    'error': f'Failed to parse generated quiz: {str(e)}'
                }
        else:
            return result
    
    def _create_quiz_prompt(self, content: str, language: str, 
                           num_questions: int, difficulty: str,
                           question_types: List[str]) -> str:
        """Create a prompt for quiz generation"""
        
        difficulty_instructions = {
            'easy': 'Focus on basic concepts and definitions. Use simple language.',
            'medium': 'Include some analysis and application questions. Moderate complexity.',
            'hard': 'Include complex analysis, synthesis, and evaluation questions.'
        }
        
        type_instructions = {
            'multiple_choice': 'Multiple choice questions with 1 correct answer and 3 realistic, plausible but incorrect distractors',
            'true_false': 'True/False questions with clear explanations',
            'short_answer': 'Short answer questions requiring 1-3 sentences with specific knowledge',
            'fill_blank': 'Fill in the blank questions with precise terminology',
            'essay': 'Essay questions requiring detailed analysis and explanation'
        }
        
        selected_types = [type_instructions[t] for t in question_types if t in type_instructions]
        
        # Language specific instructions
        language_instructions = {
            'en': 'Generate all questions and answers in English.',
            'fr': 'Générez toutes les questions et réponses en français.',
            'es': 'Genere todas las preguntas y respuestas en español.',
            'de': 'Erstellen Sie alle Fragen und Antworten auf Deutsch.',
            'it': 'Genera tutte le domande e le risposte in italiano.',
            'tr': 'Tüm soruları ve cevapları Türkçe olarak oluşturun. Türkçe dil bilgisi kurallarına ve yazım kurallarına uygun olarak yazın.'
        }
        
        lang_instruction = language_instructions.get(language, f'Generate all questions and answers in {language}.')
        
        prompt = f"""
You are a professional exam designer and educational assessment expert. Create a high-quality academic examination based on the provided content.

SOURCE CONTENT:
{content}

EXAMINATION SPECIFICATIONS:
- Target Language: {language}
- {lang_instruction}
- Number of Questions: {num_questions}
- Academic Level: {difficulty.upper()}
- Assessment Focus: {difficulty_instructions.get(difficulty, '')}

QUESTION DESIGN REQUIREMENTS:
{chr(10).join(f"• {instruction}" for instruction in selected_types)}

CRITICAL QUALITY STANDARDS:
1. MULTIPLE CHOICE QUESTIONS:
   - Create 1 CORRECT answer and 3 REALISTIC FALSE ANSWERS (distractors)
   - False answers must be plausible but clearly incorrect
   - Avoid obviously wrong options like "None of the above" or nonsensical choices
   - Base all options on actual concepts from the content
   - Make distractors challenging but fair

2. CONTENT ACCURACY:
   - All questions must directly relate to the provided content
   - Use precise terminology and concepts from the source material
   - Ensure factual correctness in all questions and answers

3. PROFESSIONAL FORMATTING:
   - Write clear, concise question stems
   - Use proper grammar and academic language
   - Include detailed explanations for correct answers
   - Assign appropriate point values based on difficulty

RESPONSE FORMAT (STRICT JSON):
{{
    "title": "[Create a professional exam title based on the content topic]",
    "description": "[Write a brief academic description of what this exam covers]",
    "questions": [
        {{
            "id": 1,
            "type": "multiple_choice",
            "question": "[Clear, specific question testing key concepts]",
            "options": [
                "[Correct answer - factually accurate]",
                "[Realistic false answer - plausible but wrong]",
                "[Realistic false answer - plausible but wrong]",
                "[Realistic false answer - plausible but wrong]"
            ],
            "correct_answer": "A",
            "explanation": "[Detailed explanation of why the correct answer is right and why others are wrong]",
            "difficulty": "{difficulty}",
            "points": [1-5 based on difficulty]
        }},
        {{
            "id": 2,
            "type": "true_false",
            "question": "[Clear statement that can be definitively true or false]",
            "correct_answer": "True",
            "explanation": "[Explain why the statement is true/false with supporting details]",
            "difficulty": "{difficulty}",
            "points": [1-3 based on difficulty]
        }}
    ],
    "total_points": {num_questions * 2},
    "estimated_duration": "[Calculate based on question complexity: 1-2 minutes per point]"
}}

EXAMPLE OF EXCELLENT MULTIPLE CHOICE QUESTION:
Question: "What is the primary advantage of cloud computing's elasticity feature?"
A. "Resources can automatically scale up or down based on demand" (CORRECT)
B. "Resources are always allocated at maximum capacity" (FALSE - opposite concept)
C. "Resources are physically located in multiple data centers" (FALSE - that's distribution, not elasticity)
D. "Resources are shared among multiple tenants" (FALSE - that's multi-tenancy, not elasticity)

Generate questions that match this quality standard. Every multiple choice option must be based on real concepts from the content.
"""
        
        return prompt.strip()
    
    def _parse_quiz_response(self, response: str) -> Dict[str, Any]:
        """Parse the quiz response from Gemini with improved error handling"""
        try:
            # Clean the response - remove markdown code fences if present
            cleaned_response = response.strip()
            # Remove leading ```json or ``` fences robustly
            if cleaned_response.startswith('```'):
                first_newline = cleaned_response.find('\n')
                if first_newline != -1:
                    fence_lang = cleaned_response[3:first_newline].strip()
                    if fence_lang in ('json', ''):
                        cleaned_response = cleaned_response[first_newline+1:]
            # Remove trailing ``` fence if present
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3].rstrip()
            
            # Try to extract JSON from the response
            start_idx = cleaned_response.find('{')
            end_idx = cleaned_response.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                # If no JSON found, create a fallback quiz from the text response
                return self._create_fallback_quiz(cleaned_response)
            
            json_str = cleaned_response[start_idx:end_idx]
            
            # Try to fix common JSON issues conservatively
            json_str = self._fix_json_issues(json_str)
            
            quiz_data = json.loads(json_str)
            
            # Validate and fix the quiz data structure
            quiz_data = self._validate_and_fix_quiz_data(quiz_data)
            
            quiz_data['success'] = True
            return quiz_data
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse quiz JSON: {str(e)}")
            print(f"Failed to parse quiz JSON: {str(e)}")
            # Create a fallback quiz instead of failing
            return self._create_fallback_quiz(response)
    
    def _fix_json_issues(self, json_str: str) -> str:
        """Fix common JSON formatting issues conservatively without corrupting valid JSON"""
        import re
        
        # Normalize Windows newlines and trim BOM if any
        json_str = json_str.replace('\r\n', '\n').replace('\r', '\n')
        if json_str.startswith('\ufeff'):
            json_str = json_str.lstrip('\ufeff')
        
        # Remove trailing commas before closing brackets/braces
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)
        
        # Do NOT escape quotes globally; assume model outputs valid JSON
        return json_str
    
    def _validate_and_fix_quiz_data(self, quiz_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and fix quiz data structure"""
        # Ensure required fields exist
        if 'questions' not in quiz_data:
            quiz_data['questions'] = []
        
        if 'title' not in quiz_data:
            quiz_data['title'] = 'Generated Quiz'
        
        if 'description' not in quiz_data:
            quiz_data['description'] = 'AI-generated quiz from course materials'
        
        # Fix question structure
        fixed_questions = []
        for i, question in enumerate(quiz_data.get('questions', [])):
            if isinstance(question, dict):
                fixed_question = {
                    'id': question.get('id', i + 1),
                    'type': question.get('type', 'multiple_choice'),
                    'question': question.get('question', f'Question {i + 1}'),
                    'correct_answer': question.get('correct_answer', ''),
                    'explanation': question.get('explanation', ''),
                    'difficulty': question.get('difficulty', 'medium'),
                    'points': question.get('points', 1)
                }
                
                # Handle options for multiple choice
                if fixed_question['type'] == 'multiple_choice':
                    options = question.get('options', [])
                    if len(options) < 4:
                        # Add default options if missing
                        while len(options) < 4:
                            options.append(f'Option {chr(65 + len(options))}')
                    fixed_question['options'] = options[:4]  # Limit to 4 options
                
                fixed_questions.append(fixed_question)
        
        quiz_data['questions'] = fixed_questions
        return quiz_data
    
    def _create_fallback_quiz(self, response_text: str) -> Dict[str, Any]:
        """Create a fallback quiz when JSON parsing fails"""
        logger.info("Creating fallback quiz due to parsing issues")
        
        # Try to extract questions from plain text
        lines = response_text.split('\n')
        questions = []
        
        current_question = None
        question_counter = 1
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for question patterns
            if any(keyword in line.lower() for keyword in ['question', '?', 'what', 'how', 'why', 'which']):
                if current_question:
                    questions.append(current_question)
                
                current_question = {
                    'id': question_counter,
                    'type': 'multiple_choice',
                    'question': line,
                    'options': ['Option A', 'Option B', 'Option C', 'Option D'],
                    'correct_answer': 'A',
                    'explanation': 'This is a generated question from the course content.',
                    'difficulty': 'medium',
                    'points': 1
                }
                question_counter += 1
        
        # Add the last question
        if current_question:
            questions.append(current_question)
        
        # If no questions were extracted, create content-based fallback questions
        if not questions:
            questions = self._create_content_based_questions(response_text)
        
        return {
            'success': True,
            'title': 'Generated Quiz',
            'description': 'AI-generated quiz from course materials',
            'questions': questions,
            'total_points': len(questions),
            'estimated_duration': '15 minutes',
            'fallback': True  # Indicate this was a fallback response
        }
    
    def _create_content_based_questions(self, content: str) -> List[Dict[str, Any]]:
        """Create realistic fallback questions based on content"""
        import re
        
        # Extract key terms and concepts from content
        sentences = re.split(r'[.!?]+', content)
        key_concepts = []
        
        for sentence in sentences[:10]:  # Limit to first 10 sentences
            sentence = sentence.strip()
            if len(sentence) > 20:  # Skip very short sentences
                key_concepts.append(sentence)
        
        questions = []
        
        # Create questions based on identified concepts
        for i, concept in enumerate(key_concepts[:5]):
            if 'cloud' in concept.lower():
                questions.append({
                    'id': i + 1,
                    'type': 'multiple_choice',
                    'question': 'What is a key characteristic of cloud computing?',
                    'options': [
                        'On-demand access to computing resources',
                        'Local data storage only',
                        'Fixed hardware configuration',
                        'Single-user access'
                    ],
                    'correct_answer': 'A',
                    'explanation': 'Cloud computing provides on-demand access to scalable computing resources over the internet.',
                    'difficulty': 'medium',
                    'points': 1
                })
            elif any(term in concept.lower() for term in ['algorithm', 'machine learning', 'ai']):
                questions.append({
                    'id': i + 1,
                    'type': 'multiple_choice',
                    'question': 'Which of the following is a type of machine learning?',
                    'options': [
                        'Supervised learning',
                        'Database management',
                        'Network protocols',
                        'File compression'
                    ],
                    'correct_answer': 'A',
                    'explanation': 'Supervised learning is a fundamental type of machine learning where models learn from labeled training data.',
                    'difficulty': 'medium',
                    'points': 1
                })
            elif any(term in concept.lower() for term in ['data', 'information', 'system']):
                questions.append({
                    'id': i + 1,
                    'type': 'true_false',
                    'question': 'Data processing systems require proper input validation.',
                    'correct_answer': 'True',
                    'explanation': 'Input validation is essential for data integrity and system security.',
                    'difficulty': 'easy',
                    'points': 1
                })
            else:
                # Generic but realistic question
                questions.append({
                    'id': i + 1,
                    'type': 'short_answer',
                    'question': f'Explain the main concept discussed in: "{concept[:50]}..."',
                    'correct_answer': 'Student should explain the key concept from the provided context.',
                    'explanation': 'This question tests understanding of the core concept presented in the material.',
                    'difficulty': 'medium',
                    'points': 2
                })
        
        # Ensure we have at least 3 questions
        while len(questions) < 3:
            questions.append({
                'id': len(questions) + 1,
                'type': 'multiple_choice',
                'question': 'Based on the provided content, which statement is most accurate?',
                'options': [
                    'The content requires careful analysis',
                    'The information is not relevant',
                    'No conclusions can be drawn',
                    'The content is purely fictional'
                ],
                'correct_answer': 'A',
                'explanation': 'Academic content requires careful analysis and understanding.',
                'difficulty': 'medium',
                'points': 1
            })
        
        return questions[:5]  # Limit to 5 questions


class ExamGenerator:
    """Service for generating exam content"""
    
    def __init__(self):
        self.gemini = GeminiService()
        self.quiz_generator = QuizGenerator()
    
    def generate_exam(self, content: str, language: str = 'en',
                     num_questions: int = 25, duration: int = 120,
                     sections: List[Dict] = None) -> Dict[str, Any]:
        """
        Generate a comprehensive exam
        
        Args:
            content: Source content for exam generation
            language: Target language
            num_questions: Total number of questions
            duration: Exam duration in minutes
            sections: List of exam sections with specific requirements
            
        Returns:
            Dict containing generated exam data
        """
        if sections is None:
            sections = [
                {'name': 'Multiple Choice', 'questions': num_questions // 2, 'types': ['multiple_choice']},
                {'name': 'Short Answer', 'questions': num_questions // 2, 'types': ['short_answer']}
            ]
        
        exam_data = {
            'title': f'Comprehensive Exam',
            'description': 'Auto-generated comprehensive examination',
            'duration': duration,
            'total_questions': num_questions,
            'sections': [],
            'success': True
        }
        
        total_tokens = 0
        total_time = 0
        
        for section in sections:
            section_result = self.quiz_generator.generate_quiz(
                content=content,
                language=language,
                num_questions=section['questions'],
                difficulty='medium',
                question_types=section['types']
            )
            
            if section_result.get('success'):
                exam_section = {
                    'name': section['name'],
                    'instructions': f"Answer all {section['questions']} questions in this section.",
                    'questions': section_result.get('questions', []),
                    'points': sum(q.get('points', 1) for q in section_result.get('questions', []))
                }
                exam_data['sections'].append(exam_section)
                
                # Accumulate metadata
                metadata = section_result.get('metadata', {})
                total_tokens += metadata.get('tokens_used', 0)
                total_time += metadata.get('processing_time', 0)
        
        exam_data['metadata'] = {
            'tokens_used': total_tokens,
            'processing_time': total_time,
            'language': language
        }
        
        return exam_data


class SyllabusGenerator:
    """Service for generating course syllabi"""
    
    def __init__(self):
        self.gemini = GeminiService()
    
    def generate_syllabus(self, course_info: Dict[str, str], 
                         language: str = 'en') -> Dict[str, Any]:
        """
        Generate a course syllabus
        
        Args:
            course_info: Dictionary with course information
            language: Target language
            
        Returns:
            Dict containing generated syllabus data
        """
        prompt = self._create_syllabus_prompt(course_info, language)
        result = self.gemini.generate_content(prompt)
        
        if result['success']:
            try:
                syllabus_data = self._parse_syllabus_response(result['content'])
                syllabus_data.update({
                    'metadata': {
                        'language': language,
                        'tokens_used': result['tokens_used'],
                        'processing_time': result['processing_time']
                    }
                })
                return syllabus_data
            except Exception as e:
                logger.error(f"Error parsing syllabus response: {str(e)}")
                return {
                    'success': False,
                    'error': f'Failed to parse generated syllabus: {str(e)}'
                }
        else:
            return result
    
    def _create_syllabus_prompt(self, course_info: Dict[str, str], language: str) -> str:
        """Create prompt for syllabus generation"""
        
        prompt = f"""
You are an experienced academic curriculum designer. Create a comprehensive course syllabus based on the following information:

COURSE INFORMATION:
- Title: {course_info.get('title', 'Course Title')}
- Code: {course_info.get('code', 'COURSE-101')}
- Credits: {course_info.get('credits', '3')}
- Duration: {course_info.get('duration', '15 weeks')}
- Level: {course_info.get('level', 'Undergraduate')}
- Department: {course_info.get('department', 'Academic Department')}
- Prerequisites: {course_info.get('prerequisites', 'None')}
- Description: {course_info.get('description', 'Course description')}

Language: {language}

Please create a detailed syllabus with the following sections:
1. Course Overview and Objectives
2. Learning Outcomes
3. Weekly Schedule (15 weeks)
4. Assessment Methods and Grading
5. Required Materials and Resources
6. Course Policies
7. Academic Integrity Policy

Format the output as JSON with clear structure.
"""
        
        return prompt.strip()
    
    def _parse_syllabus_response(self, response: str) -> Dict[str, Any]:
        """Parse syllabus response from Gemini"""
        try:
            # Try to extract JSON from the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                # If no JSON, return structured text response
                return {
                    'success': True,
                    'content': response,
                    'type': 'text'
                }
            
            json_str = response[start_idx:end_idx]
            syllabus_data = json.loads(json_str)
            syllabus_data['success'] = True
            syllabus_data['type'] = 'structured'
            
            return syllabus_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse syllabus JSON: {str(e)}")
            return {
                'success': True,
                'content': response,
                'type': 'text',
                'parse_error': str(e)
            }


class ContentAnalyzer:
    """Service for analyzing uploaded content"""
    
    def __init__(self):
        self.gemini = GeminiService()
    
    def analyze_content(self, content: str, analysis_type: str = 'summary') -> Dict[str, Any]:
        """
        Analyze content and provide insights
        
        Args:
            content: Content to analyze
            analysis_type: Type of analysis (summary, topics, difficulty, etc.)
            
        Returns:
            Dict containing analysis results
        """
        if analysis_type == 'summary':
            return self._generate_summary(content)
        elif analysis_type == 'topics':
            return self._extract_topics(content)
        elif analysis_type == 'difficulty':
            return self._assess_difficulty(content)
        else:
            return {'success': False, 'error': 'Unknown analysis type'}
    
    def _generate_summary(self, content: str) -> Dict[str, Any]:
        """Generate a summary of the content"""
        prompt = f"""
Analyze the following educational content and provide a concise summary highlighting the key concepts, main topics, and learning points.

CONTENT:
{content}

Provide a summary that includes:
1. Main topic/subject
2. Key concepts covered
3. Learning difficulty level
4. Suggested learning outcomes
5. Brief overview (2-3 sentences)

Format as JSON.
"""
        
        result = self.gemini.generate_content(prompt)
        return result
    
    def _extract_topics(self, content: str) -> Dict[str, Any]:
        """Extract main topics from content"""
        prompt = f"""
Extract and categorize the main topics from this educational content.

CONTENT:
{content}

Identify:
1. Primary topics (main subjects)
2. Secondary topics (subtopics)
3. Key terms and definitions
4. Concepts and theories mentioned

Format as a JSON list of topics with categories.
"""
        
        result = self.gemini.generate_content(prompt)
        return result
    
    def _assess_difficulty(self, content: str) -> Dict[str, Any]:
        """Assess the difficulty level of content"""
        prompt = f"""
Assess the difficulty level of this educational content.

CONTENT:
{content}

Provide assessment including:
1. Overall difficulty level (beginner/intermediate/advanced)
2. Reading level
3. Technical complexity
4. Prerequisites needed
5. Recommended audience

Format as JSON.
"""
        
        result = self.gemini.generate_content(prompt)
        return result