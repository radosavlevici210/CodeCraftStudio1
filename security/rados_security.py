
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
"""
RADOS Quantum Enforcement Policy v2.7
Advanced Security System for CodeCraft Studio
© 2025 Ervin Remus Radosavlevici
"""

import os
import json
import hashlib
import logging
from datetime import datetime, timedelta
from functools import wraps
from flask import request, abort, current_app
import uuid
import time

# Security Configuration
SECURITY_CONFIG = {
    'max_requests_per_minute': 60,
    'max_generations_per_hour': 10,
    'blocked_ips': set(),
    'security_events': [],
    'rate_limits': {},
    'file_upload_max_size': 10 * 1024 * 1024,  # 10MB
    'allowed_file_types': ['.txt', '.json', '.wav', '.mp3'],
    'owner_identifier': 'Ervin Remus Radosavlevici',
    'rados_version': '2.7',
    'enforcement_active': True
}

def log_security_event(event_type, description, severity="INFO"):
    """Log security events with RADOS protection"""
    try:
        timestamp = datetime.utcnow().isoformat()
        client_ip = get_client_ip()
        
        event = {
            'timestamp': timestamp,
            'type': event_type,
            'description': description,
            'severity': severity,
            'ip_address': client_ip,
            'rados_protected': True,
            'owner': SECURITY_CONFIG['owner_identifier']
        }
        
        # Log to file
        log_file = f"logs/security_{datetime.utcnow().strftime('%Y%m%d')}.log"
        os.makedirs('logs', exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(f"{json.dumps(event)}\n")
        
        # Store in memory for quick access
        SECURITY_CONFIG['security_events'].append(event)
        
        # Keep only last 1000 events in memory
        if len(SECURITY_CONFIG['security_events']) > 1000:
            SECURITY_CONFIG['security_events'] = SECURITY_CONFIG['security_events'][-1000:]
        
        # Console logging
        if severity in ['ERROR', 'CRITICAL']:
            logging.error(f"RADOS SECURITY [{severity}]: {event_type} - {description}")
        elif severity == 'WARNING':
            logging.warning(f"RADOS SECURITY: {event_type} - {description}")
        else:
            logging.info(f"RADOS SECURITY: {event_type} - {description}")
            
    except Exception as e:
        logging.error(f"Security logging failed: {e}")

def get_client_ip():
    """Get client IP address safely"""
    try:
        return request.environ.get('HTTP_X_FORWARDED_FOR', 
                                 request.environ.get('REMOTE_ADDR', 'unknown'))
    except:
        return 'unknown'

def enforce_rados_protection():
    """Main RADOS protection enforcement"""
    if not SECURITY_CONFIG['enforcement_active']:
        return True
    
    client_ip = get_client_ip()
    
    # Check if IP is blocked
    if client_ip in SECURITY_CONFIG['blocked_ips']:
        log_security_event("BLOCKED_ACCESS_ATTEMPT", f"Blocked IP {client_ip} attempted access", "WARNING")
        abort(403)
    
    # Rate limiting
    if not check_rate_limit_internal(client_ip):
        log_security_event("RATE_LIMIT_EXCEEDED", f"IP {client_ip} exceeded rate limit", "WARNING")
        abort(429)
    
    return True

def check_rate_limit_internal(client_ip):
    """Internal rate limiting check"""
    current_time = time.time()
    minute_window = current_time - 60
    
    if client_ip not in SECURITY_CONFIG['rate_limits']:
        SECURITY_CONFIG['rate_limits'][client_ip] = []
    
    # Clean old requests
    SECURITY_CONFIG['rate_limits'][client_ip] = [
        req_time for req_time in SECURITY_CONFIG['rate_limits'][client_ip]
        if req_time > minute_window
    ]
    
    # Check limit
    if len(SECURITY_CONFIG['rate_limits'][client_ip]) >= SECURITY_CONFIG['max_requests_per_minute']:
        return False
    
    # Add current request
    SECURITY_CONFIG['rate_limits'][client_ip].append(current_time)
    return True

def check_rate_limit(client_ip, operation_type, limit=5, window=3600):
    """Advanced rate limiting for specific operations"""
    current_time = time.time()
    window_start = current_time - window
    
    rate_key = f"{client_ip}_{operation_type}"
    
    if rate_key not in SECURITY_CONFIG['rate_limits']:
        SECURITY_CONFIG['rate_limits'][rate_key] = []
    
    # Clean old requests
    SECURITY_CONFIG['rate_limits'][rate_key] = [
        req_time for req_time in SECURITY_CONFIG['rate_limits'][rate_key]
        if req_time > window_start
    ]
    
    # Check limit
    if len(SECURITY_CONFIG['rate_limits'][rate_key]) >= limit:
        return False, f"Rate limit exceeded: {limit} {operation_type} per {window} seconds"
    
    # Add current request
    SECURITY_CONFIG['rate_limits'][rate_key].append(current_time)
    return True, "OK"

def validate_file_upload(filename):
    """Validate file uploads for security"""
    if not filename:
        return False, "No filename provided"
    
    # Check file extension
    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext not in SECURITY_CONFIG['allowed_file_types']:
        return False, f"File type {file_ext} not allowed"
    
    # Check filename for malicious patterns
    dangerous_patterns = ['..', '/', '\\', '<', '>', '|', ':', '*', '?', '"']
    for pattern in dangerous_patterns:
        if pattern in filename:
            return False, f"Filename contains dangerous character: {pattern}"
    
    return True, "File validation passed"

def sanitize_user_input(user_input):
    """Sanitize user input to prevent injection attacks"""
    if not user_input:
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', '`', '|', ';']
    sanitized = str(user_input)
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    # Limit length
    sanitized = sanitized[:1000]
    
    return sanitized.strip()

def generate_secure_filename(original_filename):
    """Generate secure filename with timestamp"""
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    safe_name = ''.join(c for c in original_filename if c.isalnum() or c in '._-')
    unique_id = str(uuid.uuid4())[:8]
    
    return f"{timestamp}_{unique_id}_{safe_name}"

def audit_system_access():
    """Generate security audit report"""
    current_time = datetime.utcnow()
    
    # Count events by type
    event_counts = {}
    for event in SECURITY_CONFIG['security_events']:
        event_type = event.get('type', 'unknown')
        event_counts[event_type] = event_counts.get(event_type, 0) + 1
    
    # Get unique IPs
    unique_ips = set()
    for event in SECURITY_CONFIG['security_events']:
        if event.get('ip_address'):
            unique_ips.add(event['ip_address'])
    
    audit_report = {
        'audit_timestamp': current_time.isoformat(),
        'rados_version': SECURITY_CONFIG['rados_version'],
        'owner': SECURITY_CONFIG['owner_identifier'],
        'enforcement_status': 'ACTIVE' if SECURITY_CONFIG['enforcement_active'] else 'DISABLED',
        'statistics': {
            'total_events': len(SECURITY_CONFIG['security_events']),
            'unique_ips': len(unique_ips),
            'blocked_ips': len(SECURITY_CONFIG['blocked_ips']),
            'events_by_type': event_counts
        },
        'recent_events': SECURITY_CONFIG['security_events'][-10:],
        'blocked_ips': list(SECURITY_CONFIG['blocked_ips']),
        'protection_status': 'QUANTUM_ENFORCEMENT_ACTIVE'
    }
    
    return audit_report

def rados_protection_decorator(f):
    """Decorator to apply RADOS protection to routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        enforce_rados_protection()
        return f(*args, **kwargs)
    return decorated_function

def initialize_rados_security():
    """Initialize RADOS security system"""
    log_security_event("RADOS_INIT", "RADOS Quantum Enforcement Policy v2.7 initialized")
    log_security_event("SYSTEM_STARTUP", f"System started under protection of {SECURITY_CONFIG['owner_identifier']}")
    
    # Create necessary directories
    directories = ['logs', 'logs/security', 'static/uploads']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    return True

# Initialize on import
initialize_rados_security()
