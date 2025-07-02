"""
Routes for CodeCraft Studio
Handles all web requests and API endpoints
© 2025 Ervin Remus Radosavlevici
"""

from flask import render_template, request, redirect, url_for, flash, send_file, jsonify, session
from app import app, db
from models import Generation, SecurityLog
from ai_agent import InvictusAIAgent
from youtube_uploader import YouTubeUploader
from collaboration_system import collaboration_system
from advanced_audio_mixer import AdvancedAudioMixer
from voice_training_system import VoiceTrainingSystem
from security.rados_security import log_security_event, enforce_rados_protection
import os
import json
import uuid
import logging

# Initialize all systems
ai_agent = InvictusAIAgent()
youtube_uploader = YouTubeUploader()
audio_mixer = AdvancedAudioMixer()
voice_trainer = VoiceTrainingSystem()

@app.route('/')
def index():
    """Main page"""
    try:
        enforce_rados_protection()
        
        # Get recent generations
        recent_generations = Generation.query.filter_by(status='completed').order_by(Generation.created_at.desc()).limit(5).all()
        
        # Get system health
        system_health = ai_agent.monitor_system_health()
        
        # Get statistics
        stats = ai_agent.get_generation_statistics()
        
        return render_template('index.html', 
                             recent_generations=recent_generations,
                             system_health=system_health,
                             stats=stats)
    except Exception as e:
        log_security_event("INDEX_ERROR", str(e), "ERROR")
        flash("An error occurred loading the page", "error")
        return render_template('index.html', 
                             recent_generations=[],
                             system_health={},
                             stats={})

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    """Generation page"""
    try:
        enforce_rados_protection()
        
        if request.method == 'POST':
            # Get form data
            theme = request.form.get('theme', '').strip()
            title = request.form.get('title', '').strip()
            voice_style = request.form.get('voice_style', 'heroic_male')
            music_style = request.form.get('music_style', 'epic')
            
            # Validate input
            if not theme:
                flash("Theme is required", "error")
                return render_template('generate.html')
            
            if len(theme) < 3:
                flash("Theme must be at least 3 characters long", "error")
                return render_template('generate.html')
            
            # Generate content
            try:
                log_security_event("GENERATION_REQUEST", f"Theme: {theme}, Title: {title}")
                
                # Use AI agent to generate complete content
                result = ai_agent.generate_complete_content(theme, title)
                
                flash("Generation completed successfully!", "success")
                return redirect(url_for('results', generation_id=result['id']))
                
            except Exception as e:
                log_security_event("GENERATION_PROCESS_ERROR", str(e), "ERROR")
                flash(f"Generation failed: {str(e)}", "error")
                return render_template('generate.html')
        
        # GET request - show form
        return render_template('generate.html')
        
    except Exception as e:
        log_security_event("GENERATE_PAGE_ERROR", str(e), "ERROR")
        flash("An error occurred", "error")
        return render_template('generate.html')

@app.route('/results/<int:generation_id>')
def results(generation_id):
    """Results page"""
    try:
        enforce_rados_protection()
        
        # Get generation record
        generation = Generation.query.get_or_404(generation_id)
        
        # Parse lyrics data
        lyrics_data = generation.get_lyrics_data()
        
        # Check if files exist
        audio_exists = generation.audio_file and os.path.exists(generation.audio_file)
        video_exists = generation.video_file and os.path.exists(generation.video_file)
        
        return render_template('results.html',
                             generation=generation,
                             lyrics_data=lyrics_data,
                             audio_exists=audio_exists,
                             video_exists=video_exists)
        
    except Exception as e:
        log_security_event("RESULTS_PAGE_ERROR", str(e), "ERROR")
        flash("Could not load results", "error")
        return redirect(url_for('index'))

@app.route('/download/<int:generation_id>/<file_type>')
def download(generation_id, file_type):
    """Download generated files"""
    try:
        enforce_rados_protection()
        
        generation = Generation.query.get_or_404(generation_id)
        
        if file_type == 'audio' and generation.audio_file:
            if os.path.exists(generation.audio_file):
                log_security_event("FILE_DOWNLOAD", f"Audio: {generation.audio_file}")
                return send_file(generation.audio_file, as_attachment=True)
        
        elif file_type == 'video' and generation.video_file:
            if os.path.exists(generation.video_file):
                log_security_event("FILE_DOWNLOAD", f"Video: {generation.video_file}")
                return send_file(generation.video_file, as_attachment=True)
        
        flash("File not found", "error")
        return redirect(url_for('results', generation_id=generation_id))
        
    except Exception as e:
        log_security_event("DOWNLOAD_ERROR", str(e), "ERROR")
        flash("Download failed", "error")
        return redirect(url_for('index'))

@app.route('/gallery')
def gallery():
    """Gallery of all generations"""
    try:
        enforce_rados_protection()
        
        page = request.args.get('page', 1, type=int)
        per_page = 12
        
        generations = Generation.query.filter_by(status='completed').order_by(
            Generation.created_at.desc()
        ).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('gallery.html', generations=generations)
        
    except Exception as e:
        log_security_event("GALLERY_ERROR", str(e), "ERROR")
        flash("Could not load gallery", "error")
        return redirect(url_for('index'))

@app.route('/health')
def health():
    """System health endpoint"""
    try:
        health_data = ai_agent.monitor_system_health()
        return jsonify(health_data)
    except Exception as e:
        log_security_event("HEALTH_CHECK_ERROR", str(e), "ERROR")
        return jsonify({"error": "Health check failed"}), 500

@app.route('/stats')
def stats():
    """Statistics endpoint"""
    try:
        stats_data = ai_agent.get_generation_statistics()
        return jsonify(stats_data)
    except Exception as e:
        log_security_event("STATS_ERROR", str(e), "ERROR")
        return jsonify({"error": "Could not load statistics"}), 500

# ============= ADVANCED FEATURES API ENDPOINTS =============

@app.route('/api/youtube/upload', methods=['POST'])
def youtube_upload():
    """YouTube upload API endpoint"""
    try:
        enforce_rados_protection()
        
        generation_id = request.json.get('generation_id')
        if not generation_id:
            return jsonify({"error": "Generation ID required"}), 400
        
        generation = Generation.query.get(generation_id)
        if not generation:
            return jsonify({"error": "Generation not found"}), 404
        
        # Prepare upload package
        generation_data = {
            'id': generation.id,
            'title': generation.title,
            'theme': generation.theme,
            'music_style': generation.music_style,
            'voice_style': generation.voice_style,
            'lyrics_data': generation.get_lyrics_data(),
            'audio_file': generation.audio_file,
            'video_file': generation.video_file
        }
        
        package = youtube_uploader.prepare_upload_package(generation_data)
        result = youtube_uploader.simulate_youtube_upload(package)
        
        log_security_event("YOUTUBE_UPLOAD_REQUEST", f"Generation: {generation_id}")
        return jsonify(result)
        
    except Exception as e:
        log_security_event("YOUTUBE_UPLOAD_ERROR", str(e), "ERROR")
        return jsonify({"error": str(e)}), 500

@app.route('/api/collaboration/create', methods=['POST'])
def create_collaboration():
    """Create collaborative session"""
    try:
        enforce_rados_protection()
        
        generation_id = request.json.get('generation_id')
        user_name = request.json.get('user_name', 'Anonymous')
        
        if not generation_id:
            return jsonify({"error": "Generation ID required"}), 400
        
        # Create user session if not exists
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())
        
        user_id = session['user_id']
        
        session_id = collaboration_system.create_collaborative_session(
            generation_id, user_id, user_name
        )
        
        log_security_event("COLLABORATION_CREATED", f"Session: {session_id}")
        return jsonify({
            "session_id": session_id,
            "user_id": user_id,
            "status": "created"
        })
        
    except Exception as e:
        log_security_event("COLLABORATION_CREATE_ERROR", str(e), "ERROR")
        return jsonify({"error": str(e)}), 500

@app.route('/api/collaboration/join', methods=['POST'])
def join_collaboration():
    """Join collaborative session"""
    try:
        enforce_rados_protection()
        
        session_id = request.json.get('session_id')
        user_name = request.json.get('user_name', 'Anonymous')
        
        if not session_id:
            return jsonify({"error": "Session ID required"}), 400
        
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())
        
        user_id = session['user_id']
        
        collaboration_system.join_collaborative_session(session_id, user_id, user_name)
        
        log_security_event("COLLABORATION_JOINED", f"Session: {session_id}")
        return jsonify({
            "session_id": session_id,
            "user_id": user_id,
            "status": "joined"
        })
        
    except Exception as e:
        log_security_event("COLLABORATION_JOIN_ERROR", str(e), "ERROR")
        return jsonify({"error": str(e)}), 500

@app.route('/api/collaboration/updates/<session_id>')
def get_collaboration_updates(session_id):
    """Get live collaboration updates"""
    try:
        enforce_rados_protection()
        
        if 'user_id' not in session:
            return jsonify({"error": "User not authenticated"}), 401
        
        user_id = session['user_id']
        last_update_id = request.args.get('last_update_id')
        
        updates = collaboration_system.get_live_updates(session_id, user_id, last_update_id)
        
        return jsonify({"updates": updates})
        
    except Exception as e:
        log_security_event("COLLABORATION_UPDATES_ERROR", str(e), "ERROR")
        return jsonify({"error": str(e)}), 500

@app.route('/api/audio/mix', methods=['POST'])
def create_audio_mix():
    """Create professional audio mix"""
    try:
        enforce_rados_protection()
        
        audio_tracks = request.json.get('tracks', [])
        mixing_style = request.json.get('style', 'cinematic_epic')
        
        if not audio_tracks:
            return jsonify({"error": "Audio tracks required"}), 400
        
        mix_result = audio_mixer.create_professional_mix(audio_tracks, mixing_style)
        
        log_security_event("AUDIO_MIX_CREATED", f"Style: {mixing_style}")
        return jsonify(mix_result)
        
    except Exception as e:
        log_security_event("AUDIO_MIX_ERROR", str(e), "ERROR")
        return jsonify({"error": str(e)}), 500

@app.route('/api/voice/train', methods=['POST'])
def train_custom_voice():
    """Train custom voice model"""
    try:
        enforce_rados_protection()
        
        voice_name = request.json.get('voice_name')
        training_samples = request.json.get('training_samples', [])
        target_characteristics = request.json.get('target_characteristics', {})
        
        if not voice_name or not training_samples:
            return jsonify({"error": "Voice name and training samples required"}), 400
        
        model_package = voice_trainer.create_custom_voice_model(
            voice_name, training_samples, target_characteristics
        )
        
        log_security_event("VOICE_TRAINING_COMPLETED", f"Voice: {voice_name}")
        return jsonify(model_package)
        
    except Exception as e:
        log_security_event("VOICE_TRAINING_ERROR", str(e), "ERROR")
        return jsonify({"error": str(e)}), 500

@app.route('/api/voice/synthesize', methods=['POST'])
def synthesize_custom_voice():
    """Synthesize speech with custom voice"""
    try:
        enforce_rados_protection()
        
        text = request.json.get('text')
        voice_model_id = request.json.get('voice_model_id')
        emotion = request.json.get('emotion', 'neutral')
        
        if not text or not voice_model_id:
            return jsonify({"error": "Text and voice model ID required"}), 400
        
        audio_file = voice_trainer.synthesize_with_custom_voice(text, voice_model_id, emotion)
        
        log_security_event("CUSTOM_VOICE_SYNTHESIS", f"Model: {voice_model_id}")
        return jsonify({
            "audio_file": audio_file,
            "voice_model_id": voice_model_id,
            "emotion": emotion
        })
        
    except Exception as e:
        log_security_event("CUSTOM_VOICE_SYNTHESIS_ERROR", str(e), "ERROR")
        return jsonify({"error": str(e)}), 500

@app.route('/api/voice/evaluate', methods=['POST'])
def evaluate_voice_quality():
    """Evaluate custom voice quality"""
    try:
        enforce_rados_protection()
        
        voice_model_id = request.json.get('voice_model_id')
        test_texts = request.json.get('test_texts', [
            "This is a test of the voice quality evaluation system.",
            "The quick brown fox jumps over the lazy dog.",
            "Artificial intelligence is transforming the world of audio synthesis."
        ])
        
        if not voice_model_id:
            return jsonify({"error": "Voice model ID required"}), 400
        
        evaluation_results = voice_trainer.evaluate_voice_quality(voice_model_id, test_texts)
        
        log_security_event("VOICE_QUALITY_EVALUATION", f"Model: {voice_model_id}")
        return jsonify(evaluation_results)
        
    except Exception as e:
        log_security_event("VOICE_EVALUATION_ERROR", str(e), "ERROR")
        return jsonify({"error": str(e)}), 500

@app.route('/api/youtube/analytics/<video_id>')
def get_youtube_analytics(video_id):
    """Get YouTube video analytics"""
    try:
        enforce_rados_protection()
        
        analytics = youtube_uploader.get_upload_analytics(video_id)
        
        return jsonify(analytics)
        
    except Exception as e:
        log_security_event("YOUTUBE_ANALYTICS_ERROR", str(e), "ERROR")
        return jsonify({"error": str(e)}), 500

@app.route('/api/collaboration/analytics/<session_id>')
def get_collaboration_analytics(session_id):
    """Get collaboration session analytics"""
    try:
        enforce_rados_protection()
        
        analytics = collaboration_system.get_session_analytics(session_id)
        
        return jsonify(analytics)
        
    except Exception as e:
        log_security_event("COLLABORATION_ANALYTICS_ERROR", str(e), "ERROR")
        return jsonify({"error": str(e)}), 500

# ============= ADVANCED FEATURES WEB PAGES =============

@app.route('/collaboration')
def collaboration_page():
    """Collaboration dashboard page"""
    try:
        enforce_rados_protection()
        
        # Get user's active sessions
        user_id = session.get('user_id')
        active_sessions = []
        
        if user_id:
            # Get active collaboration sessions for user
            for session_id, session_data in collaboration_system.active_sessions.items():
                if any(p['id'] == user_id for p in session_data['participants']):
                    active_sessions.append({
                        'id': session_id,
                        'generation_id': session_data['generation_id'],
                        'participants': len(session_data['participants']),
                        'created_at': session_data['created_at']
                    })
        
        return render_template('collaboration.html', active_sessions=active_sessions)
        
    except Exception as e:
        log_security_event("COLLABORATION_PAGE_ERROR", str(e), "ERROR")
        flash("Could not load collaboration page", "error")
        return redirect(url_for('index'))

@app.route('/voice-training')
def voice_training_page():
    """Voice training dashboard page"""
    try:
        enforce_rados_protection()
        
        # Get available voice models
        voice_models = []
        models_dir = 'static/voice_models'
        
        if os.path.exists(models_dir):
            for filename in os.listdir(models_dir):
                if filename.endswith('.json'):
                    try:
                        with open(os.path.join(models_dir, filename), 'r') as f:
                            model_data = json.load(f)
                            voice_models.append({
                                'name': model_data.get('voice_name', 'Unknown'),
                                'id': model_data.get('model_id', filename),
                                'quality': model_data.get('model_info', {}).get('quality_score', 0),
                                'created_at': model_data.get('created_at', '')
                            })
                    except:
                        continue
        
        return render_template('voice_training.html', voice_models=voice_models)
        
    except Exception as e:
        log_security_event("VOICE_TRAINING_PAGE_ERROR", str(e), "ERROR")
        flash("Could not load voice training page", "error")
        return redirect(url_for('index'))

@app.route('/audio-mixer')
def audio_mixer_page():
    """Audio mixer dashboard page"""
    try:
        enforce_rados_protection()
        
        # Get recent mixes
        recent_mixes = []
        mixing_dir = 'static/mixing'
        
        if os.path.exists(mixing_dir):
            for filename in os.listdir(mixing_dir):
                if filename.startswith('session_') and filename.endswith('.json'):
                    try:
                        with open(os.path.join(mixing_dir, filename), 'r') as f:
                            session_data = json.load(f)
                            recent_mixes.append({
                                'id': session_data.get('id', 'Unknown'),
                                'style': session_data.get('style', 'Unknown'),
                                'tracks': len(session_data.get('tracks', [])),
                                'created_at': session_data.get('created_at', '')
                            })
                    except:
                        continue
        
        return render_template('audio_mixer.html', 
                             recent_mixes=recent_mixes,
                             mixing_presets=list(audio_mixer.mixing_presets.keys()))
        
    except Exception as e:
        log_security_event("AUDIO_MIXER_PAGE_ERROR", str(e), "ERROR")
        flash("Could not load audio mixer page", "error")
        return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    log_security_event("404_ERROR", request.url)
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    log_security_event("500_ERROR", str(error), "ERROR")
    db.session.rollback()
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Internal server error"), 500

# Context processor for global template variables
@app.context_processor
def inject_global_vars():
    """Inject global variables into templates"""
    return {
        'app_name': 'CodeCraft Studio',
        'app_version': '1.0',
        'copyright': '© 2025 Ervin Remus Radosavlevici',
        'license': 'Radosavlevici Game License v1.0'
    }
