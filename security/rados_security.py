
"""
RADOS Quantum Enforcement Policy v2.7
Advanced security and protection system for CodeCraft Studio
© 2025 Ervin Remus Radosavlevici
"""

import os
import hashlib
import logging
from datetime import datetime
from flask import request, session

# Security configuration
SECURITY_CONFIG = {
    'max_requests_per_minute': 60,
    'blocked_extensions': ['.exe', '.bat', '.cmd', '.sh'],
    'max_file_size': 50 * 1024 * 1024,  # 50MB
    'require_https': False,  # Set to True in production
    'session_timeout': 3600  # 1 hour
}

# Global security tracking
security_state = {
    'blocked_ips': set(),
    'suspicious_patterns': [],
    'request_counts': {},
    'security_events': []
}

def log_security_event(event_type, description, severity="INFO"):
    """Log security events with comprehensive tracking"""
    try:
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        # Create security event
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'description': description,
            'severity': severity,
            'ip_address': getattr(request, 'remote_addr', 'unknown') if request else 'system',
            'user_agent': getattr(request, 'user_agent', 'unknown') if request else 'system'
        }
        
        # Add to global tracking
        security_state['security_events'].append(event)
        
        # Keep only last 1000 events
        if len(security_state['security_events']) > 1000:
            security_state['security_events'] = security_state['security_events'][-1000:]
        
        # Log to file
        log_file = f"logs/security_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, 'a') as f:
            f.write(f"{event['timestamp']} - {severity} - {event_type}: {description}\n")
        
        # Log to application logger
        if severity == "ERROR":
            logging.error(f"SECURITY: {event_type} - {description}")
        elif severity == "WARNING":
            logging.warning(f"SECURITY: {event_type} - {description}")
        elif severity == "CRITICAL":
            logging.critical(f"SECURITY: {event_type} - {description}")
        else:
            logging.info(f"SECURITY: {event_type} - {description}")
            
    except Exception as e:
        logging.error(f"Failed to log security event: {e}")

def enforce_rados_protection():
    """Enforce RADOS protection policies"""
    try:
        if not request:
            return True
        
        # Check IP blocking
        client_ip = request.remote_addr
        if client_ip in security_state['blocked_ips']:
            log_security_event("BLOCKED_IP_ACCESS", f"Blocked IP attempted access: {client_ip}", "WARNING")
            return False
        
        # Rate limiting
        current_time = datetime.utcnow()
        if client_ip not in security_state['request_counts']:
            security_state['request_counts'][client_ip] = []
        
        # Clean old requests (older than 1 minute)
        security_state['request_counts'][client_ip] = [
            req_time for req_time in security_state['request_counts'][client_ip]
            if (current_time - req_time).total_seconds() < 60
        ]
        
        # Check rate limit
        if len(security_state['request_counts'][client_ip]) >= SECURITY_CONFIG['max_requests_per_minute']:
            log_security_event("RATE_LIMIT_EXCEEDED", f"IP {client_ip} exceeded rate limit", "WARNING")
            security_state['blocked_ips'].add(client_ip)
            return False
        
        # Add current request
        security_state['request_counts'][client_ip].append(current_time)
        
        return True
        
    except Exception as e:
        log_security_event("PROTECTION_ERROR", str(e), "ERROR")
        return True  # Allow on error to prevent blocking legitimate users

def watermark_content(content, content_type="text"):
    """Add watermark to generated content"""
    try:
        watermark = "© 2025 Ervin Remus Radosavlevici - CodeCraft Studio"
        
        if content_type == "text":
            return f"{content}\n\n{watermark}"
        elif content_type == "json":
            if isinstance(content, dict):
                content['watermark'] = watermark
                content['license'] = "Radosavlevici Game License v1.0"
            return content
        
        return content
        
    except Exception as e:
        log_security_event("WATERMARK_ERROR", str(e), "WARNING")
        return content

def generate_secure_hash(data):
    """Generate secure hash for data integrity"""
    try:
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()
    except Exception as e:
        log_security_event("HASH_ERROR", str(e), "WARNING")
        return None

def validate_file_upload(filename, file_size):
    """Validate file uploads for security"""
    try:
        # Check file extension
        _, ext = os.path.splitext(filename)
        if ext.lower() in SECURITY_CONFIG['blocked_extensions']:
            log_security_event("BLOCKED_FILE_EXTENSION", f"Blocked file: {filename}", "WARNING")
            return False, "File type not allowed"
        
        # Check file size
        if file_size > SECURITY_CONFIG['max_file_size']:
            log_security_event("FILE_SIZE_EXCEEDED", f"Large file rejected: {filename} ({file_size} bytes)", "WARNING")
            return False, "File too large"
        
        return True, "File validated"
        
    except Exception as e:
        log_security_event("FILE_VALIDATION_ERROR", str(e), "ERROR")
        return False, "Validation failed"

def get_security_status():
    """Get current security status"""
    return {
        'blocked_ips_count': len(security_state['blocked_ips']),
        'security_events_count': len(security_state['security_events']),
        'suspicious_patterns_count': len(security_state['suspicious_patterns']),
        'active_requests': len(security_state['request_counts']),
        'protection_active': True,
        'last_updated': datetime.utcnow().isoformat()
    }
