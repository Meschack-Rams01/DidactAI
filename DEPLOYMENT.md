# DidactAI Production Deployment Guide

## 🚀 Production Deployment Checklist

### Prerequisites
- [ ] Python 3.9+
- [ ] PostgreSQL database
- [ ] Redis server (for caching/Celery)
- [ ] Domain name and SSL certificate
- [ ] Web server (Nginx recommended)

## 📋 Step-by-Step Deployment

### 1. Environment Setup

#### 1.1 Clone Repository
```bash
git clone <your-repo-url> didactai
cd didactai
```

#### 1.2 Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 1.3 Install Dependencies
```bash
pip install -r requirements-production.txt
```

### 2. Environment Variables

Create a `.env` file with the following variables:

```bash
# Security
SECRET_KEY=your-super-secure-secret-key-minimum-50-characters
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-app-name.render.com

# Database
DATABASE_URL=postgresql://username:password@host:port/database

# AI Services
GEMINI_API_KEY=your-gemini-api-key
HUGGINGFACE_API_TOKEN=your-huggingface-token

# File Storage
MAX_UPLOAD_SIZE=50000000
ALLOWED_FILE_EXTENSIONS=pdf,docx,pptx,png,jpg,jpeg

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Caching/Background Tasks
REDIS_URL=redis://localhost:6379/0

# Monitoring (Optional)
SENTRY_DSN=your-sentry-dsn

# Admin Security
ADMIN_URL=secure-admin/
```

### 3. Database Setup

#### 3.1 Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 3.2 Create Superuser
```bash
python manage.py createsuperuser
```

#### 3.3 Load Initial Data (Optional)
```bash
python manage.py loaddata initial_data.json
```

### 4. Static Files

#### 4.1 Collect Static Files
```bash
python manage.py collectstatic --noinput
```

#### 4.2 Set Up Media Directory
```bash
mkdir -p media/uploads
mkdir -p media/exports
```

### 5. Security Configuration

#### 5.1 Run Security Checks
```bash
python manage.py check --deploy
```

#### 5.2 Generate New Secret Key
```python
# Use the deploy.py script to generate a secure secret key
python deploy.py
```

### 6. Web Server Configuration

#### 6.1 Nginx Configuration
Create `/etc/nginx/sites-available/didactai`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    ssl_certificate /path/to/your/cert.pem;
    ssl_certificate_key /path/to/your/key.pem;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /path/to/didactai/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /path/to/didactai/media/;
        expires 1y;
    }
}
```

#### 6.2 Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/didactai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 7. Process Management

#### 7.1 Gunicorn Service
Create `/etc/systemd/system/didactai.service`:

```ini
[Unit]
Description=DidactAI Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/didactai
ExecStart=/path/to/didactai/venv/bin/gunicorn \
    --config /path/to/didactai/gunicorn.conf.py \
    didactia_project.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

#### 7.2 Celery Service (For Background Tasks)
Create `/etc/systemd/system/didactai-celery.service`:

```ini
[Unit]
Description=DidactAI Celery daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/didactai
ExecStart=/path/to/didactai/venv/bin/celery -A didactia_project worker \
    --loglevel=info --concurrency=2
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

#### 7.3 Start Services
```bash
sudo systemctl enable didactai
sudo systemctl enable didactai-celery
sudo systemctl start didactai
sudo systemctl start didactai-celery
```

## 🔧 Platform-Specific Deployments

### Render.com Deployment

#### 1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: didactai
    env: python
    buildCommand: |
      pip install -r requirements-production.txt
      python manage.py collectstatic --noinput
      python manage.py migrate
    startCommand: gunicorn didactia_project.wsgi:application
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: DJANGO_SETTINGS_MODULE
        value: didactia_project.settings_production

databases:
  - name: didactai-db
    databaseName: didactai
    user: didactai
```

#### 2. Environment Variables in Render:
- Set all required environment variables in Render dashboard

### Railway Deployment

#### 1. Create `railway.toml`:
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "gunicorn didactia_project.wsgi:application"

[env]
DJANGO_SETTINGS_MODULE = "didactia_project.settings_production"
```

## 📊 Monitoring and Maintenance

### Health Checks

#### 1. Django Health Check
```bash
python manage.py check --deploy
```

#### 2. Database Health
```bash
python manage.py dbshell
```

#### 3. Static Files Check
```bash
curl -I https://yourdomain.com/static/admin/css/base.css
```

### Logging

#### Check Application Logs
```bash
sudo journalctl -u didactai -f
```

#### Check Nginx Logs
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Backup Strategy

#### 1. Database Backup
```bash
# Daily backup script
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql
```

#### 2. Media Files Backup
```bash
# Rsync media files
rsync -avz media/ /backup/media/
```

#### 3. Automated Backup Script
Create `/scripts/backup.sh`:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup"

# Database backup
pg_dump $DATABASE_URL > $BACKUP_DIR/db_backup_$DATE.sql

# Media files backup
rsync -avz /path/to/didactai/media/ $BACKUP_DIR/media/

# Keep only last 30 days of backups
find $BACKUP_DIR -name "db_backup_*.sql" -mtime +30 -delete
```

## 🔒 Security Best Practices

1. **SSL/TLS**: Always use HTTPS in production
2. **Secrets**: Never commit secrets to version control
3. **Database**: Use connection pooling and read replicas
4. **Firewalls**: Configure proper firewall rules
5. **Updates**: Keep dependencies updated
6. **Monitoring**: Set up error tracking (Sentry)
7. **Backups**: Implement regular automated backups

## 🧪 Testing Production Setup

### 1. Automated Tests
```bash
python manage.py test
```

### 2. Load Testing
```bash
# Using Apache Bench
ab -n 1000 -c 10 https://yourdomain.com/

# Using wrk
wrk -t12 -c400 -d30s https://yourdomain.com/
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Static Files Not Loading
```bash
# Check static files configuration
python manage.py findstatic admin/css/base.css
python manage.py collectstatic --dry-run
```

#### 2. Database Connection Issues
```bash
# Test database connection
python manage.py dbshell
```

#### 3. Memory Issues
```bash
# Monitor memory usage
htop
# Adjust Gunicorn workers
```

#### 4. SSL Certificate Issues
```bash
# Test SSL
openssl s_client -connect yourdomain.com:443
```

## 📞 Support

For deployment issues:
1. Check application logs
2. Verify environment variables
3. Test database connectivity
4. Review security settings

Remember to keep this deployment guide updated as your application evolves!