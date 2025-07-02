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
    from app import create_app
    from production_config import ProductionConfig
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def main():
    """Main application entry point"""
    try:
        # Create Flask app
        app = create_app()

        # Apply production configuration
        ProductionConfig.apply_to_app(app)

        # Configure logging for production
        if not app.debug:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            )

        return app

    except Exception as e:
        print(f"Failed to create application: {e}")
        sys.exit(1)

# Create app instance for Gunicorn
app = main()

if __name__ == '__main__':
    # Development server
    app.run(debug=False, host='0.0.0.0', port=5000)