"""
Health Monitor for CodeCraft Studio
Production-ready system health monitoring
© 2025 Ervin Remus Radosavlevici
"""

import os
import psutil
import time
from datetime import datetime
from security.rados_security import log_security_event

class HealthMonitor:
    """Production health monitoring system"""

    def __init__(self):
        self.start_time = time.time()
        self.health_checks = []

    def get_health_status(self):
        """Get comprehensive health status"""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            # Database check
            db_status = self._check_database()

            # File system check
            fs_status = self._check_filesystem()

            # Overall status
            overall_status = 'healthy'
            if cpu_percent > 90 or memory.percent > 90 or disk.percent > 95:
                overall_status = 'warning'
            if not db_status or not fs_status:
                overall_status = 'unhealthy'

            health_data = {
                'timestamp': datetime.utcnow().isoformat(),
                'overall_status': overall_status,
                'uptime_seconds': int(time.time() - self.start_time),
                'system': {
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'disk_percent': disk.percent,
                    'available_memory_mb': memory.available // (1024 * 1024)
                },
                'services': {
                    'database': 'healthy' if db_status else 'unhealthy',
                    'filesystem': 'healthy' if fs_status else 'unhealthy',
                    'rados_protection': 'active'
                }
            }

            return health_data

        except Exception as e:
            log_security_event("HEALTH_CHECK_ERROR", str(e), "ERROR")
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'overall_status': 'error',
                'error': str(e)
            }

    def _check_database(self):
        """Check database connectivity"""
        try:
            from app import db
            from sqlalchemy import text
            with db.engine.connect() as conn:
                conn.execute(text('SELECT 1'))
            return True
        except Exception:
            return False

    def _check_filesystem(self):
        """Check filesystem access"""
        try:
            test_file = 'health_check.tmp'
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            return True
        except Exception:
            return False

# Global health monitor instance
health_monitor = HealthMonitor()