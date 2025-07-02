#!/usr/bin/env python3
"""
CodeCraft Studio - Main Application Entry Point
Production-ready AI music and video generation platform
© 2025 Ervin Remus Radosavlevici
"""

import os
import sys
import logging
from flask import Flask

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from import_handler import check_production_dependencies, AUDIO_LIBS
    from app import create_app
    from production_config import ProductionConfig
    
    # Check dependencies on startup
    if not check_production_dependencies():
        logging.warning("Some dependencies missing - running in limited mode")
    
except ImportError as e:
    print(f"Critical import error: {e}")
    print("Starting in basic mode...")
    logging.basicConfig(level=logging.INFO)
    
    # Create minimal Flask app as fallback
    from flask import Flask
    
    def create_minimal_app():
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'fallback-key'
        
        @app.route('/')
        def index():
            return "CodeCraft Studio - Starting in safe mode..."
        
        @app.route('/health')
        def health():
            return {'status': 'limited', 'mode': 'safe'}, 200
        
        return app

def main():
    """Main application entry point"""
    try:
        # Create Flask app
        app = create_app()

        # Apply production configuration
        if 'ProductionConfig' in globals():
            ProductionConfig.apply_to_app(app)

        # Configure logging for production
        if not app.debug:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            )

        return app

    except Exception as e:
        print(f"Failed to create main application: {e}")
        print("Creating fallback application...")
        
        # Create fallback app
        if 'create_minimal_app' in globals():
            return create_minimal_app()
        else:
            from flask import Flask
            app = Flask(__name__)
            app.config['SECRET_KEY'] = 'emergency-fallback'
            
            @app.route('/')
            def emergency():
                return "CodeCraft Studio - Emergency Mode"
            
            return app

# Create app instance for Gunicorn
app = main()

if __name__ == '__main__':
    # Development server
    app.run(debug=False, host='0.0.0.0', port=5000)