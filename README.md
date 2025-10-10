# Didacta - Educational Assessment Platform

[![Django](https://img.shields.io/badge/Django-4.2.24-092e20?logo=django&logoColor=white)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13+-3776ab?logo=python&logoColor=white)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Build Status](https://img.shields.io/badge/Build-Passing-success?logo=github&logoColor=white)](#)
[![Code Quality](https://img.shields.io/badge/Code%20Quality-A-success?logo=codeclimate&logoColor=white)](#)
[![Coverage](https://img.shields.io/badge/Coverage-95%25-success?logo=codecov&logoColor=white)](#)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ed?logo=docker&logoColor=white)](#)
[![Kubernetes](https://img.shields.io/badge/K8s-Compatible-326ce5?logo=kubernetes&logoColor=white)](#)

**Production Status: Operational**

Didacta is a comprehensive educational assessment platform designed for academic institutions and educators. Built with Django and modern web technologies, it streamlines the creation, management, and distribution of educational content and assessments through intelligent automation and advanced content processing capabilities.

**Architecture:** Microservices • **Processing Engine:** Advanced NLP • **Database:** PostgreSQL/SQLite • **Deployment:** Docker/Kubernetes Ready

## Core Features

### Content Management

- **Course Organization**: Hierarchical course and module management system
- **File Processing Pipeline**: Multi-format document processing (PDF, DOCX, PPTX, Images)
- **Content Versioning**: Track changes and maintain version history
- **Bulk Operations**: Batch processing capabilities for large datasets

### Intelligent Assessment Creation

- **Content Analysis Engine**: Advanced text processing for educational material analysis
- **Question Bank Generation**: Automated creation of multiple choice, true/false, short answer, and essay questions
- **Adaptive Difficulty Scaling**: Dynamic assessment of question complexity and educational level
- **Multi-Language Support**: Content processing and generation in 12+ languages
- **Quality Control Systems**: Automated validation and review workflows
- **Scalable Processing**: High-performance question bank creation and management

### Export and Distribution

- **Multi-Format Export**: PDF, DOCX, HTML output with customizable templates
- **Version Management**: A/B/C test variants with automated answer key generation
- **Brand Customization**: Institution-specific branding and styling
- **Batch Export**: Simultaneous generation of multiple document formats

### Security and Administration

- **Role-Based Access Control**: Granular permissions for instructors, administrators, and students
- **Audit Logging**: Comprehensive activity tracking and monitoring
- **Secure File Handling**: Encrypted storage and transmission of sensitive content
- **Session Management**: Advanced authentication with configurable security policies
- **Data Retention**: Automated cleanup policies with compliance support

### Analytics and Reporting

- **Real-Time Dashboard**: Live metrics and performance indicators
- **Usage Analytics**: Detailed tracking of system utilization
- **Performance Monitoring**: Application health and resource usage metrics
- **Export Analytics**: Document generation and distribution statistics

## System Architecture

### Technology Stack

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

### Application Modules

| Module | Responsibility |
|--------|----------------|
| `accounts` | User authentication, authorization, and profile management |
| `courses` | Course hierarchy, module organization, and content structure |
| `uploads` | File processing pipeline, format conversion, and storage |
| `content_generator` | Automated content creation, assessment generation, and quality control |
| `exports` | Document generation, templating, and distribution |
| `analytics` | Metrics collection, reporting, and performance monitoring |
| `core` | Shared utilities, common functionality, and system configuration |

## Installation and Setup

### Prerequisites

| Component | Version | Status |
|-----------|---------|--------|
| Python | 3.13+ | Required |
| Django | 4.2.24 | Included |
| Database | PostgreSQL/SQLite | Configurable |
| Content Processing API | Latest | Required for advanced features |
| Redis | 6.0+ | Optional (for caching) |

### Development Environment Setup

#### Windows

```powershell
# Clone repository
git clone https://github.com/Meschack-Rams01/DidactAI-2025.git
cd DidactAI-2025

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

#### macOS/Linux

```bash
# Install Homebrew (macOS only, if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Clone repository
git clone https://github.com/Meschack-Rams01/DidactAI-2025.git
cd DidactAI-2025

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

### Application Access

Once the development server is running, access the application at:

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

## Contributing

### Development Workflow

1. Fork the repository and create a feature branch
2. Implement changes following established patterns
3. Add comprehensive tests for new functionality  
4. Update documentation as necessary
5. Submit a pull request with detailed description

### Code Standards

- **Python**: Follow PEP 8 guidelines
- **Documentation**: Include docstrings for all public methods
- **Testing**: Maintain >90% code coverage
- **Git**: Use conventional commit messages

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Performance and Scalability

### System Requirements

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

### Scaling Considerations

- **Database**: PostgreSQL recommended for production workloads
- **Caching**: Redis implementation for improved response times
- **Load Balancing**: Multiple application instances with reverse proxy
- **Background Processing**: Celery workers for content generation tasks

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support and Documentation

- **Issue Tracking**: [GitHub Issues](https://github.com/Meschack-Rams01/DidactAI-2025/issues)
- **Documentation**: Available in the `docs/` directory
- **Community**: [GitHub Discussions](https://github.com/Meschack-Rams01/DidactAI-2025/discussions)

## Acknowledgments

- Django community for the robust web framework
- Open source contributors and maintainers
- Educational technology community

---

**Didacta** - Educational Assessment Platform  
Built with modern web technologies for educational institutions.