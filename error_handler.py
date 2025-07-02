"""
Error Handler for CodeCraft Studio
Production-ready error handling and logging
© 2025 Ervin Remus Radosavlevici
"""

import logging
import traceback
from datetime import datetime
from security.rados_security import log_security_event

class ErrorHandler:
    """Production error handling system"""

    def __init__(self):
        self.error_count = 0
        self.last_errors = []

    def init_app(self, app):
        """Initialize error handling for Flask app"""

        @app.errorhandler(404)
        def handle_404(error):
            log_security_event("404_ERROR", f"Path: {error.description}")
            return {'error': 'Not found'}, 404

        @app.errorhandler(500)
        def handle_500(error):
            self.error_count += 1
            error_msg = str(error)
            log_security_event("500_ERROR", error_msg, "ERROR")

            # Track recent errors
            self.last_errors.append({
                'timestamp': datetime.utcnow().isoformat(),
                'error': error_msg,
                'traceback': traceback.format_exc()
            })

            # Keep only last 10 errors
            if len(self.last_errors) > 10:
                self.last_errors.pop(0)

            return {'error': 'Internal server error'}, 500

        @app.errorhandler(Exception)
        def handle_exception(error):
            self.error_count += 1
            error_msg = str(error)
            log_security_event("UNHANDLED_EXCEPTION", error_msg, "CRITICAL")

            app.logger.error(f"Unhandled exception: {error_msg}")
            app.logger.error(traceback.format_exc())

            return {'error': 'An unexpected error occurred'}, 500

    def get_error_stats(self):
        """Get error statistics"""
        return {
            'total_errors': self.error_count,
            'recent_errors': len(self.last_errors),
            'last_errors': self.last_errors[-5:] if self.last_errors else []
        }

# Global error handler instance
error_handler = ErrorHandler()