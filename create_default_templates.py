#!/usr/bin/env python
"""
Create default export templates for the system
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DidactAI_project.settings')
django.setup()

from exports.models import ExportTemplate
from django.contrib.auth import get_user_model

User = get_user_model()

def create_default_templates():
    """Create default export templates"""
    print("ðŸŽ¯ Creating Default Export Templates")
    print("=" * 50)
    
    # Get or create a system user
    system_user, created = User.objects.get_or_create(
        username='system',
        defaults={
            'email': 'system@DidactAI.com',
            'first_name': 'System',
            'last_name': 'User',
            'is_staff': True,
            'is_active': False
        }
    )
    
    if created:
        print(f"âœ… Created system user: {system_user.username}")
    else:
        print(f"ðŸ“‹ Using existing system user: {system_user.username}")
    
    templates_data = [
        {
            'name': 'University Style Quiz',
            'template_type': 'html',
            'content_type': 'quiz',
            'description': 'Professional university-style quiz template with institutional branding',
            'template_content': '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ quiz.title }}</title>
    <style>
        body {
            font-family: 'Times New Roman', serif;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 1in;
            line-height: 1.6;
            color: #333;
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #333;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .institution {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .department {
            font-size: 14px;
            color: #666;
        }
        .quiz-title {
            font-size: 24px;
            font-weight: bold;
            margin: 20px 0;
        }
        .quiz-info {
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
            font-size: 12px;
        }
        .question {
            margin-bottom: 25px;
            page-break-inside: avoid;
        }
        .question-header {
            font-weight: bold;
            margin-bottom: 10px;
        }
        .question-text {
            margin-bottom: 15px;
        }
        .options {
            margin-left: 20px;
        }
        .option {
            margin-bottom: 8px;
        }
        .instructions {
            background: #f5f5f5;
            padding: 15px;
            margin-bottom: 25px;
            border-left: 4px solid #007acc;
        }
        @media print {
            body { margin: 0; padding: 0.5in; }
            .no-print { display: none; }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="institution">{{ institution_name|default:"University Name" }}</div>
        <div class="department">{{ department|default:"Department of Education" }}</div>
        <div class="quiz-title">{{ quiz.title }}</div>
    </div>
    
    <div class="quiz-info">
        <div>Date: _______________</div>
        <div>Student Name: _______________________________</div>
        <div>Student ID: _______________</div>
    </div>
    
    {% if include_instructions %}
    <div class="instructions">
        <strong>Instructions:</strong>
        <ul>
            <li>Read each question carefully</li>
            <li>Select the best answer for each question</li>
            <li>Fill in your answers clearly</li>
            <li>Total time: {{ quiz.estimated_duration|default:"30 minutes" }}</li>
            <li>Total points: {{ quiz.total_points|default:"100" }}</li>
        </ul>
    </div>
    {% endif %}
    
    {% for question in quiz.questions %}
    <div class="question">
        <div class="question-header">
            Question {{ forloop.counter }} ({{ question.points|default:"1" }} point{{ question.points|default:1|pluralize }})
        </div>
        <div class="question-text">{{ question.question|default:question.question_text }}</div>
        
        {% if question.type == 'multiple_choice' %}
        <div class="options">
            {% for option in question.options %}
            <div class="option">
                <input type="radio" name="q{{ forloop.parentloop.counter }}" id="q{{ forloop.parentloop.counter }}_{{ forloop.counter }}" />
                <label for="q{{ forloop.parentloop.counter }}_{{ forloop.counter }}">{{ forloop.counter|add:"64"|chr }}. {{ option }}</label>
            </div>
            {% endfor %}
        </div>
        {% elif question.type == 'true_false' %}
        <div class="options">
            <div class="option">
                <input type="radio" name="q{{ forloop.counter }}" id="q{{ forloop.counter }}_true" />
                <label for="q{{ forloop.counter }}_true">True</label>
            </div>
            <div class="option">
                <input type="radio" name="q{{ forloop.counter }}" id="q{{ forloop.counter }}_false" />
                <label for="q{{ forloop.counter }}_false">False</label>
            </div>
        </div>
        {% else %}
        <div style="border-bottom: 1px solid #ccc; height: 40px; margin-top: 10px;"></div>
        {% endif %}
        
        {% if include_answer_key and question.explanation %}
        <div style="color: #666; font-size: 0.9em; margin-top: 10px;">
            <strong>Answer:</strong> {{ question.correct_answer }}<br>
            <strong>Explanation:</strong> {{ question.explanation }}
        </div>
        {% endif %}
    </div>
    {% endfor %}
    
    {% if watermark %}
    <div style="position: fixed; bottom: 10px; right: 10px; color: #ddd; font-size: 10px;">
        {{ watermark }}
    </div>
    {% endif %}
</body>
</html>
            ''',
            'css_styles': '''
/* Additional CSS styles for university template */
.question:nth-child(even) {
    background-color: #fafafa;
    padding: 10px;
    border-radius: 4px;
}

.correct-answer {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 4px;
    padding: 5px;
}

.page-break {
    page-break-before: always;
}
            '''
        },
        {
            'name': 'Simple HTML Quiz',
            'template_type': 'html',
            'content_type': 'quiz',
            'description': 'Clean, simple HTML template for quizzes',
            'template_content': '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ quiz.title }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .question { margin-bottom: 20px; }
        .options { margin-left: 20px; }
    </style>
</head>
<body>
    <h1>{{ quiz.title }}</h1>
    {% for question in quiz.questions %}
    <div class="question">
        <p><strong>{{ forloop.counter }}. {{ question.question|default:question.question_text }}</strong></p>
        {% if question.options %}
        <div class="options">
            {% for option in question.options %}
            <p>{{ forloop.counter|add:"64"|chr }}. {{ option }}</p>
            {% endfor %}
        </div>
        {% endif %}
    </div>
    {% endfor %}
</body>
</html>
            '''
        },
        {
            'name': 'Exam Template',
            'template_type': 'html',
            'content_type': 'exam',
            'description': 'Formal exam template with multiple sections',
            'template_content': '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ exam.title }}</title>
    <style>
        body { font-family: serif; margin: 1in; }
        .header { text-align: center; border-bottom: 2px solid black; padding-bottom: 20px; }
        .section { margin-top: 30px; }
        .question { margin-bottom: 25px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ exam.title }}</h1>
        <p>{{ institution_name|default:"Institution Name" }}</p>
    </div>
    
    {% for section in exam.sections %}
    <div class="section">
        <h2>{{ section.name }}</h2>
        {% for question in section.questions %}
        <div class="question">
            <p><strong>{{ forloop.counter }}. {{ question.question }}</strong> ({{ question.points }} points)</p>
            <!-- Question content here -->
        </div>
        {% endfor %}
    </div>
    {% endfor %}
</body>
</html>
            '''
        }
    ]
    
    created_count = 0
    
    for template_data in templates_data:
        template, created = ExportTemplate.objects.get_or_create(
            name=template_data['name'],
            template_type=template_data['template_type'],
            defaults={
                'content_type': template_data['content_type'],
                'description': template_data['description'],
                'template_content': template_data['template_content'],
                'css_styles': template_data.get('css_styles', ''),
                'is_system_template': True,
                'created_by': system_user,
                'usage_count': 0
            }
        )
        
        if created:
            print(f"âœ… Created template: {template.name}")
            created_count += 1
        else:
            print(f"ðŸ“‹ Template already exists: {template.name}")
    
    print("=" * 50)
    print(f"ðŸŽ‰ Created {created_count} new templates")
    print(f"ðŸ“Š Total templates in system: {ExportTemplate.objects.count()}")

if __name__ == "__main__":
    create_default_templates()
