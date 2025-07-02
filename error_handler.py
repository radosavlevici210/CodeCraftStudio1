
import logging
import traceback
from flask import jsonify, render_template
from datetime import datetime

class ProductionErrorHandler:
    """Production-ready error handler with logging and graceful degradation"""
    
    def __init__(self):
        self.error_count = 0
        self.last_error_time = None
    
    def init_app(self, app):
        """Initialize error handler with Flask app"""
        
        @app.errorhandler(500)
        def handle_500(error):
            self.error_count += 1
            self.last_error_time = datetime.now()
            
            # Log the error
            logging.error(f"Internal Server Error: {error}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            
            # Return JSON for API requests
            if request.path.startswith('/api/'):
                return jsonify({
                    'error': 'Internal server error',
                    'message': 'The server encountered an unexpected error',
                    'timestamp': datetime.now().isoformat()
                }), 500
            
            # Return HTML for web requests
            try:
                return render_template('error.html', 
                                     error_code=500,
                                     error_message='Internal Server Error'), 500
            except:
                return "Internal Server Error - Check logs for details", 500
        
        @app.errorhandler(404)
        def handle_404(error):
            if request.path.startswith('/api/'):
                return jsonify({
                    'error': 'Not found',
                    'message': 'The requested resource was not found'
                }), 404
            
            try:
                return render_template('error.html',
                                     error_code=404,
                                     error_message='Page Not Found'), 404
            except:
                return "Page Not Found", 404
        
        @app.errorhandler(Exception)
        def handle_exception(error):
            """Handle all unhandled exceptions"""
            self.error_count += 1
            self.last_error_time = datetime.now()
            
            logging.error(f"Unhandled exception: {error}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            
            # Don't handle HTTP exceptions
            if hasattr(error, 'code'):
                return error
            
            # Handle all other exceptions
            if request.path.startswith('/api/'):
                return jsonify({
                    'error': 'Server error',
                    'message': 'An unexpected error occurred',
                    'timestamp': datetime.now().isoformat()
                }), 500
            
            try:
                return render_template('error.html',
                                     error_code=500,
                                     error_message='Something went wrong'), 500
            except:
                return "Server Error - Please try again later", 500
    
    def get_error_stats(self):
        """Get error statistics for monitoring"""
        return {
            'error_count': self.error_count,
            'last_error_time': self.last_error_time.isoformat() if self.last_error_time else None
        }

# Global error handler instance
error_handler = ProductionErrorHandler()
