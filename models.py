from app import db
from datetime import datetime
import json

class Generation(db.Model):
    """Model for storing generation results"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    theme = db.Column(db.String(100), nullable=False)
    voice_style = db.Column(db.String(50), nullable=False)
    music_style = db.Column(db.String(50), nullable=False)
    lyrics_data = db.Column(db.Text)  # JSON string
    audio_file = db.Column(db.String(200))
    video_file = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def get_lyrics_data(self):
        """Get lyrics data as dictionary"""
        if self.lyrics_data:
            return json.loads(self.lyrics_data)
        return {}
    
    def set_lyrics_data(self, data):
        """Set lyrics data from dictionary"""
        self.lyrics_data = json.dumps(data)

class LearningData(db.Model):
    """Model for storing AI learning data"""
    id = db.Column(db.Integer, primary_key=True)
    data_type = db.Column(db.String(50), nullable=False)
    data_content = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class SecurityLog(db.Model):
    """Model for security event logging"""
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)
    event_data = db.Column(db.Text)
    severity = db.Column(db.String(20), default='INFO')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
