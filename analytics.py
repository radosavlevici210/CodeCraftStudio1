
"""
Production Analytics System for CodeCraft Studio
Real-time analytics and performance monitoring
© 2025 Ervin Remus Radosavlevici
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from threading import Lock

class ProductionAnalytics:
    """Comprehensive production analytics system"""
    
    def __init__(self):
        self.analytics_lock = Lock()
        
        # Core metrics
        self.page_views = defaultdict(list)
        self.generation_metrics = {
            'total_started': 0,
            'total_completed': 0,
            'total_failed': 0,
            'average_duration': 0,
            'by_style': defaultdict(int),
            'by_voice': defaultdict(int)
        }
        
        # Performance tracking
        self.performance_metrics = []
        self.error_tracking = defaultdict(int)
        self.user_sessions = defaultdict(dict)
        
        # System metrics
        self.system_metrics = {
            'uptime_start': datetime.utcnow(),
            'requests_per_minute': [],
            'response_times': [],
            'memory_usage': [],
            'cpu_usage': []
        }
        
        # Create analytics directory
        os.makedirs('logs/analytics', exist_ok=True)
    
    def track_page_view(self, path, user_agent="", ip_address=""):
        """Track page views with comprehensive data"""
        with self.analytics_lock:
            view_data = {
                'timestamp': datetime.utcnow().isoformat(),
                'user_agent': user_agent,
                'ip_address': ip_address,
                'path': path
            }
            
            self.page_views[path].append(view_data)
            
            # Keep only last 1000 views per page
            if len(self.page_views[path]) > 1000:
                self.page_views[path] = self.page_views[path][-1000:]
    
    def track_generation_start(self, style='unknown', voice='unknown'):
        """Track generation start with style/voice info"""
        with self.analytics_lock:
            self.generation_metrics['total_started'] += 1
            self.generation_metrics['by_style'][style] += 1
            self.generation_metrics['by_voice'][voice] += 1
    
    def track_generation_complete(self, duration_seconds, style='unknown'):
        """Track successful generation completion"""
        with self.analytics_lock:
            self.generation_metrics['total_completed'] += 1
            
            # Update average duration
            if self.generation_metrics['total_completed'] > 0:
                current_avg = self.generation_metrics['average_duration']
                total_completed = self.generation_metrics['total_completed']
                new_avg = ((current_avg * (total_completed - 1)) + duration_seconds) / total_completed
                self.generation_metrics['average_duration'] = new_avg
    
    def track_generation_failure(self, error_type='unknown'):
        """Track generation failure with error classification"""
        with self.analytics_lock:
            self.generation_metrics['total_failed'] += 1
            self.error_tracking[error_type] += 1
    
    def track_response_time(self, endpoint, response_time_ms):
        """Track API response times"""
        with self.analytics_lock:
            response_data = {
                'endpoint': endpoint,
                'response_time_ms': response_time_ms,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            self.performance_metrics.append(response_data)
            
            # Keep only last 10000 records
            if len(self.performance_metrics) > 10000:
                self.performance_metrics = self.performance_metrics[-10000:]
    
    def track_system_metrics(self, cpu_percent, memory_percent):
        """Track system resource usage"""
        with self.analytics_lock:
            metric_data = {
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            self.system_metrics['cpu_usage'].append(metric_data)
            self.system_metrics['memory_usage'].append(metric_data)
            
            # Keep only last 1440 records (24 hours at 1 per minute)
            for key in ['cpu_usage', 'memory_usage']:
                if len(self.system_metrics[key]) > 1440:
                    self.system_metrics[key] = self.system_metrics[key][-1440:]
    
    def get_analytics_summary(self):
        """Get comprehensive analytics summary"""
        with self.analytics_lock:
            now = datetime.utcnow()
            
            # Calculate success rate
            total_attempts = (self.generation_metrics['total_started'] or 1)
            success_rate = (self.generation_metrics['total_completed'] / total_attempts) * 100
            
            # Calculate uptime
            uptime_seconds = (now - self.system_metrics['uptime_start']).total_seconds()
            
            # Recent page views (last 24 hours)
            recent_views = 0
            cutoff_time = now - timedelta(hours=24)
            
            for path_views in self.page_views.values():
                for view in path_views:
                    try:
                        view_time = datetime.fromisoformat(view['timestamp'])
                        if view_time >= cutoff_time:
                            recent_views += 1
                    except:
                        pass
            
            # Average response time
            avg_response_time = 0
            if self.performance_metrics:
                total_time = sum(m['response_time_ms'] for m in self.performance_metrics[-100:])
                avg_response_time = total_time / min(len(self.performance_metrics), 100)
            
            summary = {
                'timestamp': now.isoformat(),
                'uptime_seconds': uptime_seconds,
                'uptime_formatted': self._format_uptime(uptime_seconds),
                
                # Generation metrics
                'generations': {
                    'total_started': self.generation_metrics['total_started'],
                    'total_completed': self.generation_metrics['total_completed'],
                    'total_failed': self.generation_metrics['total_failed'],
                    'success_rate_percent': round(success_rate, 2),
                    'average_duration_seconds': round(self.generation_metrics['average_duration'], 2),
                    'popular_styles': dict(self.generation_metrics['by_style']),
                    'popular_voices': dict(self.generation_metrics['by_voice'])
                },
                
                # Traffic metrics
                'traffic': {
                    'total_page_views': sum(len(views) for views in self.page_views.values()),
                    'recent_page_views_24h': recent_views,
                    'unique_pages_accessed': len(self.page_views),
                    'popular_pages': self._get_popular_pages()
                },
                
                # Performance metrics
                'performance': {
                    'average_response_time_ms': round(avg_response_time, 2),
                    'total_requests': len(self.performance_metrics),
                    'error_counts': dict(self.error_tracking)
                },
                
                # System health
                'system': {
                    'current_cpu_percent': self._get_latest_metric('cpu_usage', 'cpu_percent'),
                    'current_memory_percent': self._get_latest_metric('memory_usage', 'memory_percent'),
                    'metrics_collected': len(self.system_metrics['cpu_usage'])
                }
            }
            
            return summary
    
    def _format_uptime(self, seconds):
        """Format uptime in human-readable format"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    def _get_popular_pages(self, limit=5):
        """Get most popular pages by view count"""
        page_counts = {path: len(views) for path, views in self.page_views.items()}
        sorted_pages = sorted(page_counts.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_pages[:limit])
    
    def _get_latest_metric(self, metric_type, field):
        """Get latest value for a metric field"""
        metrics = self.system_metrics.get(metric_type, [])
        if metrics:
            return metrics[-1].get(field, 0)
        return 0
    
    def export_analytics_report(self):
        """Export comprehensive analytics report"""
        try:
            report = {
                'generated_at': datetime.utcnow().isoformat(),
                'report_type': 'production_analytics',
                'summary': self.get_analytics_summary(),
                'detailed_metrics': {
                    'page_views': dict(self.page_views),
                    'generation_metrics': dict(self.generation_metrics),
                    'performance_metrics': self.performance_metrics[-1000:],  # Last 1000
                    'error_tracking': dict(self.error_tracking),
                    'system_metrics': self.system_metrics
                }
            }
            
            # Save report to file
            report_file = f"logs/analytics/analytics_report_{int(time.time())}.json"
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            logging.info(f"Analytics report exported: {report_file}")
            return report_file
            
        except Exception as e:
            logging.error(f"Failed to export analytics report: {e}")
            return None
    
    def cleanup_old_data(self, days_to_keep=7):
        """Clean up old analytics data"""
        try:
            cleanup_count = 0
            cutoff_time = datetime.utcnow() - timedelta(days=days_to_keep)
            
            # Clean page views
            for path in list(self.page_views.keys()):
                original_count = len(self.page_views[path])
                self.page_views[path] = [
                    view for view in self.page_views[path]
                    if datetime.fromisoformat(view['timestamp']) >= cutoff_time
                ]
                cleanup_count += original_count - len(self.page_views[path])
            
            # Clean performance metrics
            original_perf_count = len(self.performance_metrics)
            self.performance_metrics = [
                metric for metric in self.performance_metrics
                if datetime.fromisoformat(metric['timestamp']) >= cutoff_time
            ]
            cleanup_count += original_perf_count - len(self.performance_metrics)
            
            logging.info(f"Cleaned up {cleanup_count} old analytics records")
            return cleanup_count
            
        except Exception as e:
            logging.error(f"Analytics cleanup failed: {e}")
            return 0

# Global analytics instance
analytics = ProductionAnalytics()
