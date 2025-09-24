# Gunicorn configuration for DidactIA production deployment
# Optimized for educational platform with AI features

# Server socket
bind = "0.0.0.0:8000"

# Worker processes
workers = 2  # Suitable for moderate traffic, can be increased
worker_class = "sync"  # Simple synchronous worker
worker_connections = 1000

# Timeouts
timeout = 120  # Increased for AI generation requests
keepalive = 5
graceful_timeout = 30

# Resource limits
max_requests = 1000
max_requests_jitter = 100
worker_tmp_dir = "/dev/shm"  # Use memory for temporary files

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "info"
capture_output = True

# Performance
preload_app = True  # Load application code before workers
enable_stdio_inheritance = True

# Security
limit_request_line = 8192
limit_request_fields = 100
limit_request_field_size = 8190