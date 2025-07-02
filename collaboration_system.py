"""
Collaboration System for CodeCraft Studio
Real-time collaboration features
© 2025 Ervin Remus Radosavlevici
"""

import json
import uuid
from datetime import datetime
from collections import defaultdict

class CollaborationSystem:
    """Real-time collaboration management"""

    def __init__(self):
        self.active_sessions = {}
        self.session_history = []
        self.user_connections = defaultdict(list)

    def create_collaborative_session(self, generation_id, user_id, user_name):
        """Create new collaborative session"""
        session_id = str(uuid.uuid4())

        session_data = {
            'id': session_id,
            'generation_id': generation_id,
            'created_by': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'participants': [{
                'id': user_id,
                'name': user_name,
                'joined_at': datetime.utcnow().isoformat(),
                'role': 'owner'
            }],
            'status': 'active',
            'updates': []
        }

        self.active_sessions[session_id] = session_data
        return session_id

    def join_collaborative_session(self, session_id, user_id, user_name):
        """Join existing collaborative session"""
        if session_id not in self.active_sessions:
            raise ValueError("Session not found")

        session = self.active_sessions[session_id]

        # Check if user already in session
        existing_participant = next((p for p in session['participants'] if p['id'] == user_id), None)

        if not existing_participant:
            session['participants'].append({
                'id': user_id,
                'name': user_name,
                'joined_at': datetime.utcnow().isoformat(),
                'role': 'collaborator'
            })

        return session_id

    def get_live_updates(self, session_id, user_id, last_update_id=None):
        """Get live updates for session"""
        if session_id not in self.active_sessions:
            return []

        session = self.active_sessions[session_id]
        updates = session.get('updates', [])

        if last_update_id:
            # Return updates after last_update_id
            try:
                last_index = next(i for i, update in enumerate(updates) if update['id'] == last_update_id)
                return updates[last_index + 1:]
            except StopIteration:
                return updates

        return updates[-10:]  # Return last 10 updates

    def get_session_analytics(self, session_id):
        """Get session analytics"""
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}

        session = self.active_sessions[session_id]

        return {
            'session_id': session_id,
            'participants_count': len(session['participants']),
            'duration_minutes': self._calculate_session_duration(session),
            'updates_count': len(session.get('updates', [])),
            'status': session['status']
        }

    def _calculate_session_duration(self, session):
        """Calculate session duration in minutes"""
        start_time = datetime.fromisoformat(session['created_at'])
        current_time = datetime.utcnow()
        duration = current_time - start_time
        return int(duration.total_seconds() / 60)

# Global collaboration system instance
collaboration_system = CollaborationSystem()