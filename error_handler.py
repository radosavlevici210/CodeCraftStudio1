
"""
Production Error Handler for CodeCraft Studio
Comprehensive error handling and logging
© 2025 Ervin Remus Radosavlevici
"""

import os
import logging
from datetime import datetime
from flask import render_template, request, jsonify
from security.rados_security import log_security_event

class ProductionErrorHandler:
    """Production-ready error handling system"""
    
    def __init__(self):
        self.setup_logging()
    
    def setup_logging(self):
        """Setup production logging configuration"""
        os.makedirs('logs', exist_ok=True)
        
        # Configure logging format
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/application.log'),
                logging.StreamHandler()
            ]
        )
    
    def init_app(self, app):
        """Initialize error handlers for Flask app"""
        
        @app.errorhandler(400)
        def bad_request(error):
            log_security_event("400_ERROR", f"Bad request: {request.url}")
            if request.is_json:
                return jsonify({'error': 'Bad request'}), 400
            return render_template('error.html', 
                                 error_code=400, 
                                 error_message="Bad request"), 400
        
        @app.errorhandler(401)
        def unauthorized(error):
            log_security_event("401_ERROR", f"Unauthorized: {request.url}")
            if request.is_json:
                return jsonify({'error': 'Unauthorized'}), 401
            return render_template('error.html', 
                                 error_code=401, 
                                 error_message="Unauthorized access"), 401
        
        @app.errorhandler(403)
        def forbidden(error):
            log_security_event("403_ERROR", f"Forbidden: {request.url}")
            if request.is_json:
                return jsonify({'error': 'Forbidden'}), 403
            return render_template('error.html', 
                                 error_code=403, 
                                 error_message="Access forbidden"), 403
        
        @app.errorhandler(404)
        def not_found(error):
            log_security_event("404_ERROR", f"Not found: {request.url}")
            if request.is_json:
                return jsonify({'error': 'Not found'}), 404
            return render_template('error.html', 
                                 error_code=404, 
                                 error_message="Page not found"), 404
        
        @app.errorhandler(500)
        def internal_error(error):
            log_security_event("500_ERROR", str(error), "ERROR")
            if request.is_json:
                return jsonify({'error': 'Internal server error'}), 500
            return render_template('error.html', 
                                 error_code=500, 
                                 error_message="Internal server error"), 500
        
        @app.errorhandler(503)
        def service_unavailable(error):
            log_security_event("503_ERROR", f"Service unavailable: {request.url}")
            if request.is_json:
                return jsonify({'error': 'Service temporarily unavailable'}), 503
            return render_template('error.html', 
                                 error_code=503, 
                                 error_message="Service temporarily unavailable"), 503
        
        @app.errorhandler(Exception)
        def handle_exception(error):
            """Handle any unhandled exceptions"""
            log_security_event("UNHANDLED_EXCEPTION", str(error), "CRITICAL")
            logging.exception("Unhandled exception occurred")
            
            if request.is_json:
                return jsonify({'error': 'An unexpected error occurred'}), 500
            return render_template('error.html', 
                                 error_code=500, 
                                 error_message="An unexpected error occurred"), 500

# Global error handler instance
error_handler = ProductionErrorHandler()
