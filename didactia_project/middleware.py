"""
Middleware to ensure database is initialized on first request
"""

from django.utils.deprecation import MiddlewareMixin
from .initialization import ensure_migrations_applied


class DatabaseInitializationMiddleware(MiddlewareMixin):
    """Middleware to ensure migrations are applied before handling requests"""
    
    def process_request(self, request):
        """Run database initialization before processing any request"""
        ensure_migrations_applied()
        return None
