# DidactAI - Intelligent Educational Assessment Platform

<div align="center">

![DidactAI](https://img.shields.io/badge/DidactAI-Educational%20Platform-0066cc?style=for-the-badge&logo=graduationcap&logoColor=white)

[![Django](https://img.shields.io/badge/Django-4.2.7-092e20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13+-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org/)
[![AI Powered](https://img.shields.io/badge/AI-Google%20Gemini-4285f4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Deployment](https://img.shields.io/badge/Deploy-Ready-success?style=flat-square&logo=render&logoColor=white)](#deployment)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=flat-square&logo=github&logoColor=white)](#)
[![Code Quality](https://img.shields.io/badge/Code%20Quality-A-success?style=flat-square&logo=codeclimate&logoColor=white)](#)

![Production Ready](https://img.shields.io/badge/Production-Ready-success?style=flat&logo=checkmarx&logoColor=white)
![AI Powered](https://img.shields.io/badge/AI-Powered-blue?style=flat&logo=brain&logoColor=white)
![Analytics](https://img.shields.io/badge/Analytics-Enabled-purple?style=flat&logo=chartdotjs&logoColor=white)
![Multi Language](https://img.shields.io/badge/Multi-Language-orange?style=flat&logo=translate&logoColor=white)
![Responsive](https://img.shields.io/badge/Mobile-Responsive-teal?style=flat&logo=responsive&logoColor=white)

[Features](#features) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Demo](#demo) • [Contributing](#contributing)

</div>

## <img src="https://img.icons8.com/fluency/24/book.png" alt="Overview" width="24" height="24"/> Overview

DidactAI is a cutting-edge educational assessment platform that revolutionizes how educators create, manage, and distribute academic content. Built with Django and powered by Google Gemini AI, it offers intelligent content generation, multi-format export capabilities, and comprehensive analytics.

**Perfect for:** Universities, Schools, Training Centers, Corporate Learning, Online Education

### <img src="https://img.icons8.com/fluency/20/target.png" alt="Highlights" width="20" height="20"/> Key Highlights

- <img src="https://img.icons8.com/fluency/16/artificial-intelligence.png" alt="AI" width="16" height="16"/> **AI-Powered Content Generation** using Google Gemini
- <img src="https://img.icons8.com/fluency/16/documents.png" alt="Documents" width="16" height="16"/> **Multi-Format Document Processing** (PDF, DOCX, PPTX)
- <img src="https://img.icons8.com/fluency/16/globe.png" alt="Global" width="16" height="16"/> **14+ Language Support** including RTL languages
- <img src="https://img.icons8.com/fluency/16/analytics.png" alt="Analytics" width="16" height="16"/> **Advanced Analytics Dashboard**
- <img src="https://img.icons8.com/fluency/16/security-checked.png" alt="Security" width="16" height="16"/> **Enterprise-Grade Security**
- <img src="https://img.icons8.com/fluency/16/responsive.png" alt="Responsive" width="16" height="16"/> **Responsive Design** for all devices
- <img src="https://img.icons8.com/fluency/16/cloud.png" alt="Cloud" width="16" height="16"/> **Cloud-Ready** deployment options


## <img src="https://img.icons8.com/fluency/24/star.png" alt="Features" width="24" height="24"/> Features

### <img src="https://img.icons8.com/fluency/20/content-management.png" alt="Content" width="20" height="20"/> Intelligent Content Management

- **Hierarchical Course Organization**: Structured course and module management
- **Multi-Format File Processing**: Advanced PDF, DOCX, PPTX document analysis
- **Content Versioning**: Track changes and maintain comprehensive history
- **Bulk Operations**: Efficient batch processing for large datasets
- **Smart Content Analysis**: AI-powered educational material evaluation

### <img src="https://img.icons8.com/fluency/20/artificial-intelligence.png" alt="AI Assessment" width="20" height="20"/> AI-Powered Assessment Creation

- **Automated Question Generation**: Multiple choice, true/false, short answer, and essay questions
- **Adaptive Difficulty Scaling**: Dynamic complexity assessment and educational level matching
- **Quality Control Systems**: Automated validation and review workflows
- **Multi-Language Support**: Content processing in 14+ languages including Arabic, Chinese, Japanese, Korean, Hindi, Turkish, and Greek
- **Context-Aware Generation**: Intelligent content analysis for relevant question creation

### <img src="https://img.icons8.com/fluency/20/export.png" alt="Export" width="20" height="20"/> Professional Export & Distribution

- **Multi-Format Export**: PDF, DOCX, HTML with customizable professional templates
- **Version Management**: A/B/C test variants with automated answer key generation
- **Brand Customization**: Institution-specific branding and styling options
- **Batch Export**: Simultaneous generation of multiple document formats
- **Professional Formatting**: Publication-ready document layouts

### <img src="https://img.icons8.com/fluency/20/security-shield.png" alt="Security" width="20" height="20"/> Security & Administration

- **Role-Based Access Control**: Granular permissions for instructors, administrators, and students
- **Comprehensive Audit Logging**: Complete activity tracking and monitoring
- **Secure File Handling**: Encrypted storage and transmission of sensitive content
- **Advanced Session Management**: Configurable security policies and authentication
- **Data Retention Policies**: Automated cleanup with compliance support

### <img src="https://img.icons8.com/fluency/20/bar-chart.png" alt="Analytics" width="20" height="20"/> Analytics & Reporting

- **Real-Time Dashboard**: Live metrics and key performance indicators
- **Usage Analytics**: Detailed system utilization tracking
- **Performance Monitoring**: Application health and resource usage metrics
- **Export Statistics**: Document generation and distribution analytics
- **User Engagement Metrics**: Comprehensive user activity insights

## <img src="https://img.icons8.com/fluency/24/architecture.png" alt="Architecture" width="24" height="24"/> System Architecture

### <img src="https://img.icons8.com/fluency/20/technology.png" alt="Tech Stack" width="20" height="20"/> Technology Stack

```
┌────────────────────────────────────────────────────────────┐
│ Frontend Layer                                            │
│ - HTML5 + TailwindCSS + Alpine.js                       │
│ - Progressive Web App (PWA) Support                     │
├────────────────────────────────────────────────────────────┤
│ Application Layer                                        │
│ - Django 4.2.24 + Django REST Framework                │
│ - Celery for Background Tasks                           │
├────────────────────────────────────────────────────────────┤
│ Content Processing Layer                                │
│ - Advanced Text Analysis Engine                         │
│ - Educational Content Processing Pipeline               │
├────────────────────────────────────────────────────────────┤
│ Data Layer                                              │
│ - PostgreSQL/SQLite Database                            │
│ - Redis for Caching and Session Management             │
└────────────────────────────────────────────────────────────┘
```

### <img src="https://img.icons8.com/fluency/20/module.png" alt="Modules" width="20" height="20"/> Application Modules

| Module | Responsibility |
|--------|----------------|
| `accounts` | User authentication, authorization, and profile management |
| `courses` | Course hierarchy, module organization, and content structure |
| `uploads` | File processing pipeline, format conversion, and storage |
| `ai_generator` | AI-powered content creation and assessment generation |
| `exports` | Document generation, templating, and distribution |
| `analytics` | Metrics collection, reporting, and performance monitoring |
| `core` | Shared utilities, common functionality, and system configuration |

## <img src="https://img.icons8.com/fluency/24/rocket.png" alt="Quick Start" width="24" height="24"/> Quick Start

### <img src="https://img.icons8.com/fluency/20/checklist.png" alt="Prerequisites" width="20" height="20"/> Prerequisites

| Component | Version | Status |
|-----------|---------|--------|
| Python | 3.13+ | Required |
| Django | 4.2.24 | Included |
| Database | PostgreSQL/SQLite | Configurable |
| Content Processing API | Latest | Required for advanced features |
| Redis | 6.0+ | Optional (for caching) |

### Development Environment Setup

#### <img src="https://img.icons8.com/fluency/20/windows-10.png" alt="Windows" width="20" height="20"/> Windows Installation

```powershell
# Clone repository
git clone https://github.com/meschack-rams01/DidactAI.git
cd DidactAI

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment variables
copy .env.example .env
# Edit .env with your configuration

# Initialize database
python manage.py migrate
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

#### <img src="https://img.icons8.com/fluency/20/mac-os.png" alt="macOS" width="20" height="20"/> macOS/Linux Installation

```bash
# Clone repository
git clone https://github.com/meschack-rams01/DidactAI.git
cd DidactAI

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python3 manage.py migrate
python3 manage.py createsuperuser

# Start development server
python3 manage.py runserver
```

### <img src="https://img.icons8.com/fluency/20/link.png" alt="Access" width="20" height="20"/> Application Access

Once the development server is running:

| Component | URL | Description |
|-----------|-----|-------------|
| Main Application | http://localhost:8000 | Primary user interface |
| Content Generator | http://localhost:8000/content-generator/ | Assessment creation tools |
| Admin Panel | http://localhost:8000/admin | Administrative interface |
| Dashboard | http://localhost:8000/dashboard/ | Analytics and reporting |
| API Documentation | http://localhost:8000/api/docs/ | REST API endpoints |

### System Verification

Verify the installation by running the following commands:

```bash
# Check Python version
python --version  # Should output 3.13+

# Check Django version  
python manage.py --version  # Should output 4.2.24

# Verify Django configuration
python manage.py check

# Test database connectivity
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Start the development server
python manage.py runserver
```

Expected outputs:
- System check: "System check identified no issues (0 silenced)."
- Migration: "Operations to perform: ..."
- Static files: "X static files copied to..."
- Server: "Starting development server at http://127.0.0.1:8000/"

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following configuration:

```bash
# Django Core Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/didacta_db
# Or for SQLite (default):
# DATABASE_URL=sqlite:///db.sqlite3

# Content Processing Configuration
PROCESSING_API_KEY=your-processing-api-key

# Email Configuration (Optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Didacta <noreply@yourdomain.com>

# Cache Configuration (Optional)
REDIS_URL=redis://localhost:6379/0

# Storage Configuration (Optional)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

### Email Service Setup

For Gmail integration:

1. Enable 2-Factor Authentication on your Google account
2. Navigate to Google Account Settings → Security → App passwords
3. Generate an application-specific password
4. Use the generated password in `EMAIL_HOST_PASSWORD`

### Supported Email Features

- **Authentication Notifications**: Login alerts with session details
- **Password Recovery**: Secure password reset workflow
- **Branded Communications**: Customizable email templates
- **Security Monitoring**: IP tracking and device fingerprinting

## Development Guidelines

### Cross-Platform Support

| Platform | Python Command | Virtual Environment | Package Manager |
|----------|----------------|--------------------|-----------------| 
| Windows | `python` | `venv\Scripts\activate` | `pip` |
| macOS | `python3` | `source venv/bin/activate` | `pip` |
| Linux | `python3` | `source venv/bin/activate` | `pip` |

### Development Commands

```bash
# Database operations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Development utilities
python manage.py shell
python manage.py test
python manage.py collectstatic

# Code quality
flake8 .
black .
pytest --cov=. --cov-report=html
```

### Code Quality Standards

- **Linting**: Use `flake8` for code style enforcement
- **Formatting**: Use `black` for consistent code formatting
- **Type Hints**: Include type annotations for better code documentation
- **Documentation**: Maintain comprehensive docstrings
- **Testing**: Achieve minimum 90% test coverage

## Troubleshooting

### Common Issues

#### Django server won't start
```bash
# Check system configuration
python manage.py check

# Apply database migrations
python manage.py migrate

# Start server
python manage.py runserver
```

#### Missing dependencies
```bash
# Install all requirements
pip install -r requirements.txt

# Install core dependencies manually if needed
pip install django python-decouple dj-database-url
```

## User Guide

### Quick Start Workflow

1. **Account Setup**: Register and configure user profile
2. **Course Creation**: Define course structure and metadata
3. **Content Upload**: Process educational materials (PDF, DOCX, PPTX)
4. **Assessment Generation**: Create quizzes and exams using automated tools
5. **Export and Distribution**: Generate professional documents

### Administrative Functions

- **User Management**: Role-based access control and permissions
- **System Monitoring**: Performance metrics and usage analytics  
- **Configuration**: Global settings and security policies
- **Maintenance**: Automated cleanup and data retention

## API Reference

### Authentication
```bash
# Get auth token
POST /api/auth/login/
Content-Type: application/json
{
  "email": "user@example.com",
  "password": "password"
}
```

### Course Management
```bash
# List courses
GET /api/courses/
Authorization: Token your-token-here

# Create course
POST /api/courses/
Authorization: Token your-token-here
Content-Type: application/json
{
  "title": "Machine Learning",
  "code": "CS401",
  "description": "Introduction to ML"
}
```

### Content Generation
```bash
# Generate quiz
POST /api/content-generator/quiz/
Authorization: Token your-token-here
Content-Type: application/json
{
  "course_id": 1,
  "source_files": [1, 2],
  "num_questions": 10,
  "difficulty": "medium",
  "language": "en"
}
```

## Testing

### Running Tests

```bash
# Execute full test suite
python manage.py test

# Run specific application tests
python manage.py test accounts
python manage.py test content_generator
python manage.py test courses

# Generate coverage report
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Test Data Management

```bash
# Load fixture data
python manage.py loaddata fixtures/sample_data.json

# Create test superuser
python manage.py createsuperuser --username=admin --email=admin@example.com

# Reset test database
python manage.py flush --noinput
python manage.py migrate
```

## Production Deployment

### Environment Configuration

```bash
# Production settings
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Security settings
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Deployment Commands

```bash
# Install production dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate --noinput

# Start background worker processes
celery -A didactia_project worker --loglevel=info &
celery -A didactia_project beat --loglevel=info &

# Start application server
gunicorn didactia_project.wsgi:application --bind 0.0.0.0:8000
```

### Deployment Options

#### Render.com
```yaml
# render.yaml
services:
  - type: web
    name: Didacta
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn didactia_project.wsgi:application
    envVars:
      - key: PYTHON_VERSION
        value: 3.13.0
```

#### Railway
```bash
railway login
railway new
railway add
railway up
```

### Container Deployment

#### Dockerfile

```dockerfile
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "didactia_project.wsgi:application"]
```

#### Docker Compose

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://postgres:password@db:5432/didacta
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=didacta
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data/

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

## <img src="https://img.icons8.com/fluency/24/contributing.png" alt="Contributing" width="24" height="24"/> Contributing

We welcome contributions! Here's how you can help:

### <img src="https://img.icons8.com/fluency/20/workflow.png" alt="Workflow" width="20" height="20"/> Development Workflow

1. Fork the repository and create a feature branch
2. Implement changes following established patterns
3. Add comprehensive tests for new functionality  
4. Update documentation as necessary
5. Submit a pull request with detailed description

### <img src="https://img.icons8.com/fluency/20/code.png" alt="Standards" width="20" height="20"/> Code Standards

- **Python**: Follow PEP 8 guidelines
- **Documentation**: Include docstrings for all public methods
- **Testing**: Maintain >90% code coverage
- **Git**: Use conventional commit messages
- **Security**: Follow OWASP guidelines

### <img src="https://img.icons8.com/fluency/20/commit.png" alt="Commits" width="20" height="20"/> Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## <img src="https://img.icons8.com/fluency/24/performance.png" alt="Performance" width="24" height="24"/> Performance & Scalability

### <img src="https://img.icons8.com/fluency/20/requirements.png" alt="Requirements" width="20" height="20"/> System Requirements

**Minimum:**
- CPU: 2 cores, 2.0 GHz
- RAM: 4 GB
- Storage: 10 GB available space
- Network: Stable internet connection for advanced features

**Recommended:**
- CPU: 4 cores, 3.0 GHz
- RAM: 8 GB
- Storage: SSD with 50 GB available space
- Network: High-speed internet connection

### <img src="https://img.icons8.com/fluency/20/scaling.png" alt="Scaling" width="20" height="20"/> Scaling Considerations

- **Database**: PostgreSQL recommended for production workloads
- **Caching**: Redis implementation for improved response times
- **Load Balancing**: Multiple application instances with reverse proxy
- **Background Processing**: Celery workers for AI generation tasks
- **CDN**: Content delivery network for static file serving

## <img src="https://img.icons8.com/fluency/24/license.png" alt="License" width="24" height="24"/> License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## <img src="https://img.icons8.com/fluency/24/support.png" alt="Support" width="24" height="24"/> Support & Documentation

- **Issue Tracking**: [GitHub Issues](https://github.com/meschack-rams01/DidactAI/issues)
- **Documentation**: Available in the `docs/` directory
- **Community**: [GitHub Discussions](https://github.com/meschack-rams01/DidactAI/discussions)
- **Email**: bergermeschack@gmail.com

## <img src="https://img.icons8.com/fluency/24/thanks.png" alt="Acknowledgments" width="24" height="24"/> Acknowledgments

- Django community for the robust web framework
- Google for Gemini AI technology
- Open source contributors and maintainers
- Educational technology community
- my heartfelt thanks go to my supervisor, Mr. Clif, whose guidance, encouragement,
and honest feedback kept me on tract and pushed me to do better. His support made a real difference,
both technically and academically.
- Icons by [Icons8](https://icons8.com)

---

<div align="center">

**DidactAI** - Intelligent Educational Assessment Platform  
Built with ❤️ for the education community

![Made with Django](https://img.shields.io/badge/Made%20with-Django-092e20?style=flat&logo=django&logoColor=white)
![Powered by AI](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285f4?style=flat&logo=google&logoColor=white)

[⭐ Star this project](https://github.com/meschack-rams01/DidactAI) if you find it helpful!

</div>
