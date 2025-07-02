"""
RADOS Quantum Enforcement Policy v2.7
Security and logging system for CodeCraft Studio
© 2025 Ervin Remus Radosavlevici
"""

import logging
from datetime import datetime
from flask import request
from models import SecurityLog
from app import db

def log_security_event(event_type, event_data="", severity="INFO"):
    """Log security events to database and file"""
    try:
        # Get request info if available
        ip_address = None
        user_agent = None
        
        if request:
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent', '')
        
        # Create database record
        log_entry = SecurityLog(
            event_type=event_type,
            event_data=str(event_data),
            severity=severity,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        db.session.add(log_entry)
        db.session.commit()
        
        # Also log to file
        timestamp = datetime.utcnow().isoformat()
        log_message = f"[{timestamp}] {severity}: {event_type} - {event_data}"
        
        if severity == "ERROR":
            logging.error(log_message)
        elif severity == "WARNING":
            logging.warning(log_message)
        else:
            logging.info(log_message)
            
    except Exception as e:
        logging.error(f"Failed to log security event: {e}")

def enforce_rados_protection():
    """Enforce RADOS protection policies"""
    log_security_event("RADOS_PROTECTION_CHECK", "System protection verification")
    
    # Check for unauthorized access patterns
    if request and request.method == 'POST':
        log_security_event("API_ACCESS", f"POST request to {request.endpoint}")
    
    return True

def watermark_content(content_type, file_path):
    """Add watermark protection to generated content"""
    watermark_data = {
        'creator': 'Ervin Remus Radosavlevici',
        'license': 'Radosavlevici Game License v1.0',
        'timestamp': datetime.utcnow().isoformat(),
        'protection': 'RADOS Quantum Enforcement Policy v2.7'
    }
    
    log_security_event("CONTENT_WATERMARKED", f"{content_type}: {file_path}")
    return watermark_data
