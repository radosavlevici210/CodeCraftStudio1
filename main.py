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
    print("Loading CodeCraft Studio in stable mode...")
    
    # Use the simple app as primary for now to ensure stability
    try:
        from simple_app import app
        print("Simple app loaded successfully")
        return app
    except ImportError as e:
        print(f"Simple app failed to load: {e}")
        
        # Try the full app as backup
        try:
            app = create_app()
            print("Full app loaded as backup")
            return app
        except Exception as full_e:
            print(f"Full app also failed: {full_e}")
            
            # Last resort emergency app
            from flask import Flask
            app = Flask(__name__)
            app.config['SECRET_KEY'] = 'emergency-fallback'
            
            @app.route('/')
            def emergency():
                return "CodeCraft Studio - Emergency Mode"
            
            @app.route('/health')
            def health():
                return {'status': 'emergency', 'mode': 'minimal'}
            
            return app

# Create app instance for Gunicorn
app = main()

if __name__ == '__main__':
    # Development server
    app.run(debug=False, host='0.0.0.0', port=5000)