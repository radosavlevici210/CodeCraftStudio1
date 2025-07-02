
"""
Comprehensive Error Handling for CodeCraft Studio
Production-ready error handling and recovery
© 2025 Ervin Remus Radosavlevici
"""

import logging
import traceback
from datetime import datetime
from flask import request, jsonify, render_template
from security.rados_security import log_security_event

class ErrorHandler:
    """Centralized error handling system"""
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize error handling for Flask app"""
        app.register_error_handler(404, self.handle_404)
        app.register_error_handler(500, self.handle_500)
        app.register_error_handler(TimeoutError, self.handle_timeout)
        app.register_error_handler(Exception, self.handle_general_error)
    
    def handle_404(self, error):
        """Handle 404 errors"""
        log_security_event("404_ERROR", f"Path: {request.path}")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Not found',
                'message': 'The requested resource was not found'
            }), 404
        
        return render_template('error.html', 
                             error_code=404,
                             error_message="Page not found"), 404
    
    def handle_500(self, error):
        """Handle 500 errors"""
        error_id = f"error_{int(datetime.utcnow().timestamp())}"
        log_security_event("500_ERROR", f"Error ID: {error_id}, Details: {str(error)}", "ERROR")
        
        # Log full traceback for debugging
        logging.error(f"500 Error {error_id}: {traceback.format_exc()}")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Internal server error',
                'error_id': error_id,
                'message': 'An internal error occurred'
            }), 500
        
        return render_template('error.html',
                             error_code=500,
                             error_message="Internal server error",
                             error_id=error_id), 500
    
    def handle_timeout(self, error):
        """Handle timeout errors"""
        log_security_event("TIMEOUT_ERROR", str(error), "WARNING")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Timeout',
                'message': 'The request timed out. Please try again.'
            }), 408
        
        return render_template('error.html',
                             error_code=408,
                             error_message="Request timed out"), 408
    
    def handle_general_error(self, error):
        """Handle general exceptions"""
        error_id = f"error_{int(datetime.utcnow().timestamp())}"
        log_security_event("GENERAL_ERROR", f"Error ID: {error_id}, Type: {type(error).__name__}, Details: {str(error)}", "ERROR")
        
        # Log full traceback
        logging.error(f"General Error {error_id}: {traceback.format_exc()}")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Application error',
                'error_id': error_id,
                'message': 'An error occurred processing your request'
            }), 500
        
        return render_template('error.html',
                             error_code=500,
                             error_message="An error occurred",
                             error_id=error_id), 500

# Create global error handler
error_handler = ErrorHandler()
