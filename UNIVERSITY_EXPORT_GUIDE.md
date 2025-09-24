# Professional University-Style Export Template

## 🎓 Overview

Your AI Exam Generator now features a professional university-style export template that creates official-looking academic examinations. The template follows academic standards with proper institutional branding, metadata, and question formatting.

## 🏛️ Key Features

### University Header
- **Logo placeholder**: Circular space for university emblem
- **Institution name**: Bold serif font in uppercase
- **Department**: Professional departmental identification
- **Course info**: Course name and semester details

### Exam Metadata Section
- **Instructor**: Full professor name
- **Date**: Official exam date
- **Duration**: Time allocation
- **Total Points**: Point distribution
- **Student info**: Name and ID fields

### Professional Question Types
- **Multiple Choice**: Checkbox format with lettered options
- **True/False**: Clean boolean choice layout
- **Short Answer**: Underlined answer spaces
- **Fill in the Blank**: Embedded blank spaces
- **Essay**: Lined writing areas for extended responses

## 📋 Usage Example

```python
from exports.services import HTMLExporter

# Define university branding
branding = {
    'university_name': 'HARVARD UNIVERSITY',
    'department': 'Department of Computer Science', 
    'course': 'Introduction to Algorithms - CS 50',
    'semester': 'Spring 2025',
    'instructor': 'Prof. David J. Malan',
    'exam_date': 'May 15, 2025'
}

# Quiz data with multiple question types
quiz_data = {
    'title': 'Data Structures and Algorithms',
    'content_type': 'exam',  # or 'quiz'
    'total_points': 100,
    'estimated_duration': '3 hours',
    'questions': [
        {
            'type': 'multiple_choice',
            'question': 'What is the time complexity of binary search?',
            'points': 10,
            'options': ['O(n)', 'O(log n)', 'O(n²)', 'O(1)'],
            'correct_answer': 'B'
        },
        {
            'type': 'true_false',
            'question': 'A stack follows the LIFO principle.',
            'points': 5,
            'correct_answer': 'True'
        },
        {
            'type': 'short_answer',
            'question': 'Explain the difference between arrays and linked lists.',
            'points': 15,
            'correct_answer': 'Arrays store elements in contiguous memory with O(1) access, while linked lists use pointers with O(n) access but dynamic sizing.'
        },
        {
            'type': 'essay',
            'question': 'Compare and contrast different sorting algorithms, discussing their time complexities and use cases.',
            'points': 25,
            'correct_answer': 'Bubble sort is O(n²) but simple, merge sort is O(n log n) and stable, quicksort averages O(n log n) but worst-case O(n²)...'
        }
    ]
}

# Generate exports
html_exporter = HTMLExporter()

# Student version (no answers)
student_html = html_exporter.export_quiz(quiz_data, branding, show_answers=False)

# Instructor version (with answer keys)  
instructor_html = html_exporter.export_quiz(quiz_data, branding, show_answers=True)
```

## 🎨 Customization Options

### University Information
```python
branding = {
    'university_name': 'YOUR UNIVERSITY',           # Main institution name
    'department': 'Department of [Subject]',       # Academic department
    'course': 'Course Name - Code',                # Course identifier
    'semester': 'Fall/Spring YYYY',                # Academic term
    'instructor': 'Prof. Full Name',               # Instructor name
    'exam_date': 'Month DD, YYYY'                  # Exam date
}
```

### Question Point Values
```python
question = {
    'points': 15,  # Individual question worth
    # ... other question data
}

quiz_data = {
    'total_points': 100,  # Overall exam value
    # ... other quiz data
}
```

## 📄 Output Features

### Student Version
- Clean, professional layout
- No answer indicators
- Clear instructions
- Answer spaces for all question types
- Print-optimized formatting

### Instructor Version  
- All student features plus:
- ✅ Correct answer highlighting
- 📘 Answer key boxes
- 💡 Expected answer text
- 📋 Grading assistance

## 🖨️ Print Optimization

The template includes print-specific CSS that:
- Removes screen-only elements
- Optimizes page breaks
- Ensures proper spacing
- Maintains readability at 12pt font

## 🌍 Language Support

Currently optimized for:
- ✅ English (primary)
- ✅ Turkish (tested)
- ✅ International characters
- ✅ RTL text support (partial)

## 📱 Responsive Design

- Desktop: Full layout with proper margins
- Tablet: Adjusted spacing and font sizes
- Print: Professional A4/Letter optimization
- Mobile: Readable but optimized for desktop use

## 🔧 Technical Specifications

### Fonts
- **Headers**: Crimson Text (serif) for academic formality
- **Body**: Inter (sans-serif) for modern readability
- **Fallbacks**: System fonts for compatibility

### Colors
- **Primary**: Professional navy (#2c3e50)
- **Secondary**: Subtle gray (#34495e) 
- **Accents**: Academic blue (#3498db)
- **Backgrounds**: Clean whites and light grays

### Layout
- **Container**: A4 paper size (210mm width)
- **Margins**: Professional 40px padding
- **Typography**: 1.6 line height for readability
- **Spacing**: Consistent 25px question gaps

## 💼 Use Cases

### Perfect For
- Official university examinations
- Department-level assessments
- Professional certification tests
- Academic research questionnaires
- Standardized testing formats
- Faculty evaluations

### Industries
- Higher education institutions
- Professional training organizations
- Certification bodies
- Corporate learning departments
- Government testing agencies

## 🚀 Integration

The university template is automatically used when exporting through:

1. **Web Interface**: Select "Export" → Choose format → Download
2. **API Calls**: Standard export endpoints with branding parameters
3. **Bulk Generation**: Multiple versions with randomized question orders
4. **Direct Service**: HTMLExporter class with branding configuration

## ✨ Example Output

The template generates professional documents that look like official university exams, complete with:

- Institutional headers matching university standards
- Proper academic formatting and typography
- Professional question presentation
- Answer spaces appropriate for each question type  
- Official footer with institution identification
- Print-ready layout for paper distribution

## 📞 Support

For customization requests or additional features:
- Template modifications
- Custom branding elements
- Additional question types
- Language localization
- Corporate styling

Your AI Exam Generator now produces university-quality assessments ready for official academic use!