"""
Analytics System for CodeCraft Studio
Real-time analytics and performance monitoring
© 2025 Ervin Remus Radosavlevici
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

class Analytics:
    """Production analytics tracking"""

    def __init__(self):
        self.page_views = defaultdict(list)
        self.generation_metrics = {
            'total_started': 0,
            'total_completed': 0,
            'total_failed': 0,
            'response_times': []
        }
        self.user_metrics = defaultdict(dict)

    def track_page_view(self, path, user_agent="", ip=""):
        """Track page views"""
        self.page_views[path].append({
            'timestamp': datetime.utcnow().isoformat(),
            'user_agent': user_agent,
            'ip': ip
        })

    def track_response_time(self, endpoint, response_time_ms):
        """Track response times"""
        self.generation_metrics['response_times'].append({
            'endpoint': endpoint,
            'time_ms': response_time_ms,
            'timestamp': datetime.utcnow().isoformat()
        })

        # Keep only last 1000 entries
        if len(self.generation_metrics['response_times']) > 1000:
            self.generation_metrics['response_times'] = self.generation_metrics['response_times'][-1000:]

    def get_analytics_summary(self):
        """Get comprehensive analytics summary"""
        return {
            'page_views': {path: len(views) for path, views in self.page_views.items()},
            'generation_metrics': self.generation_metrics,
            'popular_pages': self._get_popular_pages(),
            'performance_stats': self._get_performance_stats(),
            'timestamp': datetime.utcnow().isoformat()
        }

    def _get_popular_pages(self):
        """Get most popular pages"""
        page_counts = [(path, len(views)) for path, views in self.page_views.items()]
        return sorted(page_counts, key=lambda x: x[1], reverse=True)[:10]

    def _get_performance_stats(self):
        """Get performance statistics"""
        if not self.generation_metrics['response_times']:
            return {'average_response_time': 0, 'slow_endpoints': []}

        times = [rt['time_ms'] for rt in self.generation_metrics['response_times']]
        avg_time = sum(times) / len(times)

        # Find slow endpoints (>1000ms)
        slow_endpoints = [rt for rt in self.generation_metrics['response_times'] if rt['time_ms'] > 1000]

        return {
            'average_response_time': round(avg_time, 2),
            'slow_endpoints': len(slow_endpoints)
        }

# Global analytics instance
analytics = Analytics()