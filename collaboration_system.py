"""
Real-Time Collaboration System for CodeCraft Studio
Handles multi-user collaboration, live editing, and shared workspace management
© 2025 Ervin Remus Radosavlevici
"""

import os
import time
import json
import uuid
import logging
from datetime import datetime, timedelta
from threading import Thread, Lock
from security.rados_security import log_security_event, watermark_content
from app import db
from models import Generation, LearningData

class CollaborationSystem:
    """Advanced real-time collaboration and workspace management"""
    
    def __init__(self):
        self.active_sessions = {}
        self.shared_workspaces = {}
        self.live_updates = {}
        self.session_lock = Lock()
        
        # Collaboration features configuration
        self.features = {
            'live_editing': True,
            'voice_chat': True,
            'screen_sharing': True,
            'version_control': True,
            'real_time_sync': True,
            'collaborative_mixing': True,
            'shared_ai_learning': True
        }
        
        # User roles and permissions
        self.user_roles = {
            'owner': {
                'can_edit': True,
                'can_delete': True,
                'can_share': True,
                'can_export': True,
                'can_manage_users': True,
                'can_access_ai': True
            },
            'collaborator': {
                'can_edit': True,
                'can_delete': False,
                'can_share': True,
                'can_export': True,
                'can_manage_users': False,
                'can_access_ai': True
            },
            'viewer': {
                'can_edit': False,
                'can_delete': False,
                'can_share': False,
                'can_export': False,
                'can_manage_users': False,
                'can_access_ai': False
            }
        }
        
        # Ensure collaboration directories exist
        os.makedirs('static/collaboration', exist_ok=True)
        os.makedirs('logs/collaboration', exist_ok=True)
        
        # Start background cleanup task
        self.cleanup_thread = Thread(target=self._cleanup_expired_sessions, daemon=True)
        self.cleanup_thread.start()
    
    def create_collaborative_session(self, generation_id, user_id, user_name):
        """Create a new collaborative session"""
        try:
            session_id = str(uuid.uuid4())
            
            with self.session_lock:
                self.active_sessions[session_id] = {
                    'id': session_id,
                    'generation_id': generation_id,
                    'owner_id': user_id,
                    'owner_name': user_name,
                    'participants': [{'id': user_id, 'name': user_name, 'role': 'owner'}],
                    'created_at': datetime.utcnow(),
                    'last_activity': datetime.utcnow(),
                    'workspace_data': self._initialize_workspace(generation_id),
                    'live_changes': [],
                    'version_history': [],
                    'chat_messages': [],
                    'active_tools': {},
                    'locked_sections': {}
                }
            
            log_security_event("COLLABORATION_SESSION_CREATED", f"Session: {session_id}")
            print(f"🤝 Collaborative session created: {session_id}")
            
            return session_id
            
        except Exception as e:
            log_security_event("COLLABORATION_SESSION_ERROR", str(e), "ERROR")
            raise e
    
    def join_collaborative_session(self, session_id, user_id, user_name, invite_code=None):
        """Join an existing collaborative session"""
        try:
            with self.session_lock:
                if session_id not in self.active_sessions:
                    raise ValueError("Session not found or expired")
                
                session = self.active_sessions[session_id]
                
                # Check if user is already in session
                existing_user = next((p for p in session['participants'] if p['id'] == user_id), None)
                if existing_user:
                    existing_user['last_seen'] = datetime.utcnow()
                    return session_id
                
                # Add new participant
                session['participants'].append({
                    'id': user_id,
                    'name': user_name,
                    'role': 'collaborator',
                    'joined_at': datetime.utcnow(),
                    'last_seen': datetime.utcnow(),
                    'permissions': self.user_roles['collaborator']
                })
                
                session['last_activity'] = datetime.utcnow()
                
                # Notify other participants
                self._broadcast_user_joined(session_id, user_name)
            
            log_security_event("COLLABORATION_USER_JOINED", f"User {user_name} joined session {session_id}")
            print(f"👋 {user_name} joined collaborative session")
            
            return session_id
            
        except Exception as e:
            log_security_event("COLLABORATION_JOIN_ERROR", str(e), "ERROR")
            raise e
    
    def _initialize_workspace(self, generation_id):
        """Initialize collaborative workspace data"""
        try:
            # Load generation data
            generation = Generation.query.get(generation_id)
            if not generation:
                return {}
            
            workspace = {
                'generation_data': {
                    'title': generation.title,
                    'theme': generation.theme,
                    'voice_style': generation.voice_style,
                    'music_style': generation.music_style,
                    'lyrics_data': generation.get_lyrics_data(),
                    'status': generation.status
                },
                'editing_state': {
                    'current_section': 'lyrics',
                    'cursor_positions': {},
                    'selected_ranges': {},
                    'active_tools': []
                },
                'audio_mixing': {
                    'tracks': [],
                    'effects': [],
                    'mix_settings': {},
                    'timeline_position': 0
                },
                'video_editing': {
                    'scenes': [],
                    'transitions': [],
                    'timeline': [],
                    'preview_position': 0
                }
            }
            
            return workspace
            
        except Exception as e:
            logging.error(f"Workspace initialization failed: {e}")
            return {}
    
    def update_workspace_live(self, session_id, user_id, update_data):
        """Handle live workspace updates"""
        try:
            with self.session_lock:
                if session_id not in self.active_sessions:
                    raise ValueError("Session not found")
                
                session = self.active_sessions[session_id]
                
                # Validate user permissions
                user = next((p for p in session['participants'] if p['id'] == user_id), None)
                if not user or not user.get('permissions', {}).get('can_edit', False):
                    raise PermissionError("User does not have edit permissions")
                
                # Apply update to workspace
                self._apply_workspace_update(session['workspace_data'], update_data)
                
                # Record the change
                change_record = {
                    'id': str(uuid.uuid4()),
                    'user_id': user_id,
                    'user_name': user['name'],
                    'timestamp': datetime.utcnow().isoformat(),
                    'type': update_data.get('type', 'edit'),
                    'section': update_data.get('section', 'unknown'),
                    'data': update_data,
                    'version': len(session['live_changes']) + 1
                }
                
                session['live_changes'].append(change_record)
                session['last_activity'] = datetime.utcnow()
                
                # Broadcast to other participants
                self._broadcast_live_update(session_id, change_record, user_id)
            
            log_security_event("COLLABORATION_UPDATE", f"Session {session_id} updated by {user_id}")
            return change_record['id']
            
        except Exception as e:
            log_security_event("COLLABORATION_UPDATE_ERROR", str(e), "ERROR")
            raise e
    
    def _apply_workspace_update(self, workspace_data, update_data):
        """Apply update to workspace data"""
        update_type = update_data.get('type')
        section = update_data.get('section')
        data = update_data.get('data', {})
        
        if update_type == 'lyrics_edit':
            workspace_data['generation_data']['lyrics_data'].update(data)
        elif update_type == 'style_change':
            if 'voice_style' in data:
                workspace_data['generation_data']['voice_style'] = data['voice_style']
            if 'music_style' in data:
                workspace_data['generation_data']['music_style'] = data['music_style']
        elif update_type == 'audio_mix':
            workspace_data['audio_mixing'].update(data)
        elif update_type == 'video_edit':
            workspace_data['video_editing'].update(data)
        elif update_type == 'timeline_position':
            if section == 'audio':
                workspace_data['audio_mixing']['timeline_position'] = data.get('position', 0)
            elif section == 'video':
                workspace_data['video_editing']['preview_position'] = data.get('position', 0)
    
    def _broadcast_live_update(self, session_id, change_record, sender_user_id):
        """Broadcast live update to all session participants"""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                return
            
            # Store update for real-time delivery
            if session_id not in self.live_updates:
                self.live_updates[session_id] = []
            
            self.live_updates[session_id].append({
                'change': change_record,
                'sender': sender_user_id,
                'broadcast_time': datetime.utcnow().isoformat()
            })
            
            # Keep only recent updates (last 100)
            if len(self.live_updates[session_id]) > 100:
                self.live_updates[session_id] = self.live_updates[session_id][-100:]
            
        except Exception as e:
            logging.error(f"Broadcast failed: {e}")
    
    def _broadcast_user_joined(self, session_id, user_name):
        """Broadcast user joined notification"""
        try:
            join_notification = {
                'type': 'user_joined',
                'user_name': user_name,
                'timestamp': datetime.utcnow().isoformat(),
                'message': f"{user_name} joined the collaboration"
            }
            
            if session_id not in self.live_updates:
                self.live_updates[session_id] = []
            
            self.live_updates[session_id].append({
                'notification': join_notification,
                'broadcast_time': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            logging.error(f"User joined broadcast failed: {e}")
    
    def get_live_updates(self, session_id, user_id, last_update_id=None):
        """Get live updates for a session"""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                return []
            
            # Verify user is in session
            user = next((p for p in session['participants'] if p['id'] == user_id), None)
            if not user:
                raise PermissionError("User not in session")
            
            # Update user's last seen
            user['last_seen'] = datetime.utcnow()
            
            # Get updates
            updates = self.live_updates.get(session_id, [])
            
            # Filter updates based on last_update_id if provided
            if last_update_id:
                # Implementation would filter based on update ID
                pass
            
            return updates[-20:]  # Return last 20 updates
            
        except Exception as e:
            logging.error(f"Get live updates failed: {e}")
            return []
    
    def create_shared_workspace(self, workspace_name, creator_id, creator_name):
        """Create a shared workspace for multiple projects"""
        try:
            workspace_id = str(uuid.uuid4())
            
            self.shared_workspaces[workspace_id] = {
                'id': workspace_id,
                'name': workspace_name,
                'creator_id': creator_id,
                'creator_name': creator_name,
                'created_at': datetime.utcnow(),
                'members': [{'id': creator_id, 'name': creator_name, 'role': 'owner'}],
                'projects': [],
                'shared_resources': {
                    'samples': [],
                    'templates': [],
                    'presets': []
                },
                'activity_log': []
            }
            
            log_security_event("SHARED_WORKSPACE_CREATED", f"Workspace: {workspace_id}")
            return workspace_id
            
        except Exception as e:
            log_security_event("SHARED_WORKSPACE_ERROR", str(e), "ERROR")
            raise e
    
    def enable_voice_chat(self, session_id, user_id):
        """Enable voice chat for collaboration session"""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                raise ValueError("Session not found")
            
            # Simulate voice chat setup
            voice_chat_config = {
                'enabled': True,
                'quality': 'high',
                'noise_suppression': True,
                'echo_cancellation': True,
                'auto_gain_control': True,
                'room_id': f"voice_{session_id}",
                'participants': []
            }
            
            session['voice_chat'] = voice_chat_config
            
            log_security_event("VOICE_CHAT_ENABLED", f"Session: {session_id}")
            return voice_chat_config
            
        except Exception as e:
            log_security_event("VOICE_CHAT_ERROR", str(e), "ERROR")
            raise e
    
    def save_collaboration_version(self, session_id, user_id, version_name, description=""):
        """Save a version snapshot of the collaboration"""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                raise ValueError("Session not found")
            
            version = {
                'id': str(uuid.uuid4()),
                'name': version_name,
                'description': description,
                'created_by': user_id,
                'created_at': datetime.utcnow().isoformat(),
                'workspace_snapshot': json.dumps(session['workspace_data']),
                'participants_snapshot': session['participants'].copy(),
                'change_count': len(session['live_changes'])
            }
            
            session['version_history'].append(version)
            
            # Save to file system
            version_file = f"static/collaboration/version_{session_id}_{version['id']}.json"
            with open(version_file, 'w') as f:
                json.dump(version, f, indent=2)
            
            log_security_event("COLLABORATION_VERSION_SAVED", f"Version: {version['id']}")
            return version['id']
            
        except Exception as e:
            log_security_event("COLLABORATION_VERSION_ERROR", str(e), "ERROR")
            raise e
    
    def get_session_analytics(self, session_id):
        """Get analytics for collaboration session"""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                return None
            
            analytics = {
                'session_id': session_id,
                'duration': (datetime.utcnow() - session['created_at']).total_seconds(),
                'participants_count': len(session['participants']),
                'changes_count': len(session['live_changes']),
                'versions_count': len(session.get('version_history', [])),
                'activity_level': self._calculate_activity_level(session),
                'collaboration_score': self._calculate_collaboration_score(session),
                'last_activity': session['last_activity'].isoformat()
            }
            
            return analytics
            
        except Exception as e:
            logging.error(f"Session analytics failed: {e}")
            return None
    
    def _calculate_activity_level(self, session):
        """Calculate activity level for session"""
        recent_changes = [
            c for c in session['live_changes']
            if datetime.fromisoformat(c['timestamp']) > datetime.utcnow() - timedelta(minutes=30)
        ]
        
        if len(recent_changes) > 20:
            return 'high'
        elif len(recent_changes) > 5:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_collaboration_score(self, session):
        """Calculate collaboration effectiveness score"""
        try:
            participants_count = len(session['participants'])
            changes_count = len(session['live_changes'])
            duration_hours = (datetime.utcnow() - session['created_at']).total_seconds() / 3600
            
            # Simple scoring algorithm
            if duration_hours > 0:
                changes_per_hour = changes_count / duration_hours
                collaboration_factor = min(participants_count / 2, 2)  # Cap at 2x
                score = (changes_per_hour * collaboration_factor) / 10
                return min(score, 10)  # Cap at 10
            
            return 0
            
        except:
            return 0
    
    def _cleanup_expired_sessions(self):
        """Background task to cleanup expired sessions"""
        while True:
            try:
                time.sleep(300)  # Check every 5 minutes
                
                with self.session_lock:
                    expired_sessions = []
                    cutoff_time = datetime.utcnow() - timedelta(hours=24)
                    
                    for session_id, session in self.active_sessions.items():
                        if session['last_activity'] < cutoff_time:
                            expired_sessions.append(session_id)
                    
                    for session_id in expired_sessions:
                        self._archive_session(session_id)
                        del self.active_sessions[session_id]
                        if session_id in self.live_updates:
                            del self.live_updates[session_id]
                
                if expired_sessions:
                    log_security_event("COLLABORATION_CLEANUP", f"Cleaned up {len(expired_sessions)} expired sessions")
                
            except Exception as e:
                logging.error(f"Session cleanup failed: {e}")
    
    def _archive_session(self, session_id):
        """Archive session data before cleanup"""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                return
            
            archive_data = {
                'session': session,
                'live_updates': self.live_updates.get(session_id, []),
                'archived_at': datetime.utcnow().isoformat()
            }
            
            archive_file = f"logs/collaboration/archived_{session_id}_{int(time.time())}.json"
            with open(archive_file, 'w') as f:
                json.dump(archive_data, f, indent=2, default=str)
                
        except Exception as e:
            logging.error(f"Session archiving failed: {e}")

# Global collaboration system instance
collaboration_system = CollaborationSystem()