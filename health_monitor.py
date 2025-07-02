
"""
Health Monitoring System for CodeCraft Studio
Real-time system health and performance monitoring
© 2025 Ervin Remus Radosavlevici
"""

import psutil
import time
import logging
from datetime import datetime, timedelta
from threading import Thread
import sqlite3
import os

class HealthMonitor:
    """Comprehensive system health monitoring"""
    
    def __init__(self):
        self.monitoring_active = True
        self.health_data = {
            'system': {},
            'database': {},
            'api': {},
            'performance': {}
        }
        self.start_monitoring()
    
    def start_monitoring(self):
        """Start background health monitoring"""
        monitor_thread = Thread(target=self._monitor_loop, daemon=True)
        monitor_thread.start()
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        while self.monitoring_active:
            try:
                self._check_system_health()
                self._check_database_health()
                self._check_api_health()
                self._check_performance()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logging.error(f"Health monitoring error: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _check_system_health(self):
        """Monitor system resources"""
        try:
            self.health_data['system'] = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent,
                'uptime': time.time() - psutil.boot_time(),
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logging.error(f"System health check failed: {e}")
    
    def _check_database_health(self):
        """Monitor database connectivity"""
        try:
            db_path = "instance/codecraft_studio.db"
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path, timeout=5)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM sqlite_master")
                result = cursor.fetchone()
                conn.close()
                
                self.health_data['database'] = {
                    'status': 'healthy',
                    'tables_count': result[0] if result else 0,
                    'file_size': os.path.getsize(db_path),
                    'timestamp': datetime.utcnow().isoformat()
                }
            else:
                self.health_data['database'] = {
                    'status': 'missing',
                    'timestamp': datetime.utcnow().isoformat()
                }
        except Exception as e:
            self.health_data['database'] = {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def _check_api_health(self):
        """Monitor API availability"""
        try:
            openai_key = os.environ.get('OPENAI_API_KEY')
            self.health_data['api'] = {
                'openai_configured': bool(openai_key),
                'openai_key_length': len(openai_key) if openai_key else 0,
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            self.health_data['api'] = {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def _check_performance(self):
        """Monitor performance metrics"""
        try:
            # Check directory sizes
            static_size = self._get_directory_size('static')
            logs_size = self._get_directory_size('logs')
            
            self.health_data['performance'] = {
                'static_files_size': static_size,
                'logs_size': logs_size,
                'generated_files': self._count_generated_files(),
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logging.error(f"Performance check failed: {e}")
    
    def _get_directory_size(self, directory):
        """Get total size of directory"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
        except Exception:
            pass
        return total_size
    
    def _count_generated_files(self):
        """Count generated audio/video files"""
        count = 0
        try:
            for directory in ['static/audio', 'static/video']:
                if os.path.exists(directory):
                    count += len([f for f in os.listdir(directory) 
                                if f.endswith(('.mp3', '.mp4', '.wav'))])
        except Exception:
            pass
        return count
    
    def get_health_status(self):
        """Get current health status"""
        return {
            'overall_status': self._calculate_overall_status(),
            'details': self.health_data,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _calculate_overall_status(self):
        """Calculate overall system status"""
        try:
            system = self.health_data.get('system', {})
            database = self.health_data.get('database', {})
            
            # Check critical thresholds
            if system.get('cpu_percent', 0) > 90:
                return 'critical'
            if system.get('memory_percent', 0) > 90:
                return 'critical'
            if database.get('status') == 'error':
                return 'degraded'
            
            return 'healthy'
        except Exception:
            return 'unknown'
    
    def cleanup_old_files(self):
        """Clean up old generated files"""
        try:
            cleanup_count = 0
            cutoff_time = time.time() - (24 * 60 * 60)  # 24 hours
            
            for directory in ['static/audio', 'static/video', 'logs']:
                if os.path.exists(directory):
                    for filename in os.listdir(directory):
                        filepath = os.path.join(directory, filename)
                        if os.path.isfile(filepath):
                            if os.path.getmtime(filepath) < cutoff_time:
                                os.remove(filepath)
                                cleanup_count += 1
            
            logging.info(f"Cleaned up {cleanup_count} old files")
            return cleanup_count
        except Exception as e:
            logging.error(f"File cleanup failed: {e}")
            return 0

# Global health monitor instance
health_monitor = HealthMonitor()
    """System health monitoring"""
    
    def __init__(self):
        self.start_time = datetime.utcnow()
    
    def get_health_status(self):
        """Get comprehensive system health status"""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Application health
            health_status = {
                'timestamp': datetime.utcnow().isoformat(),
                'uptime_seconds': (datetime.utcnow() - self.start_time).total_seconds(),
                'system': {
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'memory_available_mb': memory.available / (1024 * 1024),
                    'disk_percent': disk.percent,
                    'disk_free_gb': disk.free / (1024 * 1024 * 1024)
                },
                'application': {
                    'status': 'healthy',
                    'openai_configured': bool(os.environ.get('OPENAI_API_KEY')),
                    'database': 'connected'
                },
                'overall_health': self._calculate_overall_health(cpu_percent, memory.percent, disk.percent)
            }
            
            return health_status
            
        except Exception as e:
            log_security_event("HEALTH_MONITOR_ERROR", str(e), "ERROR")
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'status': 'error',
                'error': str(e)
            }
    
    def _calculate_overall_health(self, cpu, memory, disk):
        """Calculate overall system health"""
        if cpu > 90 or memory > 90 or disk > 95:
            return 'critical'
        elif cpu > 70 or memory > 80 or disk > 85:
            return 'warning'
        elif cpu > 50 or memory > 60 or disk > 70:
            return 'good'
        else:
            return 'excellent'

# Global health monitor instance
health_monitor = HealthMonitor()
