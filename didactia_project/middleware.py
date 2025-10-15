"""
Middleware to ensure database is initialized on first request
"""

from django.utils.deprecation import MiddlewareMixin


class DatabaseInitializationMiddleware(MiddlewareMixin):
    """Middleware to ensure migrations are applied before handling requests"""
    
    def process_request(self, request):
        """Run database initialization before processing any request"""
        try:
            from .initialization import ensure_migrations_applied
            ensure_migrations_applied()
        except Exception as e:
            # Log but don't fail - let the view handle DB errors
            print(f"[MIDDLEWARE] Error during initialization: {e}")
            import traceback
            traceback.print_exc()
        return None
