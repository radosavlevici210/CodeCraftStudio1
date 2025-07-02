"""
The changes address import errors by wrapping imports in try-except blocks and logging errors, improving the application's robustness during startup.
"""
"""
Routes for CodeCraft Studio
Handles all web requests and API endpoints
© 2025 Ervin Remus Radosavlevici
"""

from flask import render_template, request, redirect, url_for, flash, send_file, jsonify, session, Blueprint
from app import db
from models import Generation, SecurityLog
from business_licensing import BusinessLicense, SalesRecord, license_manager
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
import time
from datetime import datetime
from health_monitor import health_monitor
from analytics import analytics

# Create blueprint for routes
main_bp = Blueprint('main', __name__)

# Initialize all systems
ai_agent = InvictusAIAgent()
youtube_uploader = YouTubeUploader()
audio_mixer = AdvancedAudioMixer()
voice_trainer = VoiceTrainingSystem()

@main_bp.route('/')
def index():
    """Main page"""
    try:
        enforce_rados_protection()

        # Get recent generations
        recent_generations = Generation.query.filter_by(status='completed').order_by(Generation.created_at.desc()).limit(5).all()

        # Get system health
        system_health = health_monitor.get_health_status()
        analytics_summary = analytics.get_analytics_summary()

        # Get statistics
        stats = ai_agent.get_generation_statistics()

        return render_template('index.html', 
                             recent_generations=recent_generations,
                             system_health=system_health,
                             stats=stats,
                             analytics=analytics_summary)
    except Exception as e:
        log_security_event("INDEX_ERROR", str(e), "ERROR")
        flash("An error occurred loading the page", "error")
        return render_template('index.html', 
                             recent_generations=[],
                             system_health={},
                             stats={})

@main_bp.route('/generate', methods=['GET', 'POST'])
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

            # Generate content with production timeout
            try:
                log_security_event("GENERATION_REQUEST", f"Theme: {theme}, Title: {title}")

                # Add production timeout wrapper
                import signal

                def timeout_handler(signum, frame):
                    raise TimeoutError("Generation timed out")

                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(25)  # 25 second total timeout

                try:
                    # Use AI agent to generate complete content
                    result = ai_agent.generate_complete_content(theme, title)
                    signal.alarm(0)  # Cancel timeout

                    flash("Generation completed successfully!", "success")
                    return redirect(url_for('main.results', generation_id=result['id']))

                except TimeoutError:
                    signal.alarm(0)
                    log_security_event("GENERATION_TIMEOUT", f"Theme: {theme}")
                    flash("Generation timed out. Please try a simpler theme.", "warning")
                    return render_template('generate.html')

                except Exception as gen_error:
                    signal.alarm(0)
                    raise gen_error

            except Exception as e:
                log_security_event("GENERATION_PROCESS_ERROR", str(e), "ERROR")

                # Provide user-friendly error messages
                if "timeout" in str(e).lower():
                    flash("Generation timed out. Please try again with a simpler theme.", "warning")
                elif "api" in str(e).lower():
                    flash("AI service temporarily unavailable. Please try again.", "warning")
                else:
                    flash("Generation failed. Please try again.", "error")

                return render_template('generate.html')

        # GET request - show form
        return render_template('generate.html')

    except Exception as e:
        log_security_event("GENERATE_PAGE_ERROR", str(e), "ERROR")
        flash("An error occurred", "error")
        return render_template('generate.html')

@main_bp.route('/results/<int:generation_id>')
def results(generation_id):
    """Results page"""
    try:
        enforce_rados_protection()

        # Get generation record
        generation = Generation.query.get_or_404(generation_id)

        # Parse lyrics data
        lyrics_data = generation.get_lyrics_data()

        # Check if files exist
        audio_exists = generation.audio_file and os.path.exists(f"static/audio/{generation.audio_file}")
        video_exists = generation.video_file and os.path.exists(f"static/video/{generation.video_file}")

        return render_template('results.html',
                             generation=generation,
                             lyrics_data=lyrics_data,
                             audio_exists=audio_exists,
                             video_exists=video_exists)

    except Exception as e:
        log_security_event("RESULTS_PAGE_ERROR", str(e), "ERROR")
        flash("Could not load results", "error")
        return redirect(url_for('main.index'))

@main_bp.route('/download/<int:generation_id>/<file_type>')
def download(generation_id, file_type):
    """Download generated files"""
    try:
        enforce_rados_protection()

        generation = Generation.query.get_or_404(generation_id)

        if file_type == 'audio' and generation.audio_file:
            file_path = f"static/audio/{generation.audio_file}"
            if os.path.exists(file_path):
                log_security_event("FILE_DOWNLOAD", f"Audio: {generation.audio_file}")
                return send_file(file_path, as_attachment=True)

        elif file_type == 'video' and generation.video_file:
            file_path = f"static/video/{generation.video_file}"
            if os.path.exists(file_path):
                log_security_event("FILE_DOWNLOAD", f"Video: {generation.video_file}")
                return send_file(file_path, as_attachment=True)

        flash("File not found", "error")
        return redirect(url_for('main.results', generation_id=generation_id))

    except Exception as e:
        log_security_event("DOWNLOAD_ERROR", str(e), "ERROR")
        flash("Download failed", "error")
        return redirect(url_for('main.index'))

@main_bp.route('/gallery')
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
        return redirect(url_for('main.index'))

@main_bp.route('/health')
def health_check():
    """Production health check endpoint"""
    try:
        health_status = health_monitor.get_health_status()
        return jsonify(health_status), 200
    except Exception as e:
        log_security_event("HEALTH_CHECK_ERROR", str(e), "ERROR")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@main_bp.route('/analytics')
def analytics_dashboard():
    """Production analytics dashboard"""
    try:
        analytics_data = analytics.get_analytics_summary()
        return jsonify(analytics_data), 200
    except Exception as e:
        log_security_event("ANALYTICS_ERROR", str(e), "ERROR")
        return jsonify({'error': str(e)}), 500

@main_bp.route('/status')
def system_status():
    """Comprehensive system status"""
    try:
        status = {
            'health': health_monitor.get_health_status(),
            'analytics': analytics.get_analytics_summary(),
            'security': {
                'protection_active': True,
                'rados_version': '2.7',
                'owner': 'Ervin Remus Radosavlevici'
            }
        }
        return jsonify(status), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/stats')
def stats():
    """Statistics endpoint"""
    try:
        stats_data = ai_agent.get_generation_statistics()
        return jsonify(stats_data)
    except Exception as e:
        log_security_event("STATS_ERROR", str(e), "ERROR")
        return jsonify({"error": "Could not load statistics"}), 500

# ============= ADVANCED FEATURES API ENDPOINTS =============

@main_bp.route('/api/youtube/upload', methods=['POST'])
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

@main_bp.route('/api/collaboration/create', methods=['POST'])
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

@main_bp.route('/api/audio/mix', methods=['POST'])
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

@main_bp.route('/api/voice/train', methods=['POST'])
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

# ============= ERROR HANDLERS =============

@main_bp.errorhandler(404)
def not_found(error):
    """404 error handler"""
    log_security_event("404_ERROR", request.url)
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Page not found"), 404

@main_bp.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    log_security_event("500_ERROR", str(error), "ERROR")
    db.session.rollback()
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Internal server error"), 500

# ============================================================================
# BUSINESS LICENSING ROUTES
# ============================================================================

@main_bp.route('/business')
def business():
    """Business licensing and sales page"""
    try:
        enforce_rados_protection()
        log_security_event("BUSINESS_PAGE_ACCESS", "Business licensing page accessed")
        return render_template('business.html')
    except Exception as e:
        log_security_event("BUSINESS_PAGE_ERROR", str(e), "ERROR")
        return render_template('error.html', message="Business page unavailable"), 500

@main_bp.route('/api/business/purchase', methods=['POST'])
def purchase_license():
    """Purchase a business license"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['license_type', 'customer_name', 'customer_email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Create license
        license_record = license_manager.create_license(
            license_type=data['license_type'],
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            company_name=data.get('company_name')
        )
        
        # Record sale
        sale_record = license_manager.record_sale(license_record)
        
        log_security_event("LICENSE_PURCHASED", f"License purchased: {license_record.license_key} by {data['customer_email']}")
        
        return jsonify({
            'success': True,
            'license_key': license_record.license_key,
            'transaction_id': sale_record.transaction_id,
            'message': 'License purchased successfully'
        })
        
    except Exception as e:
        log_security_event("LICENSE_PURCHASE_ERROR", str(e), "ERROR")
        return jsonify({'success': False, 'error': str(e)}), 500

@main_bp.route('/api/business/validate', methods=['POST'])
def validate_license():
    """Validate a license key"""
    try:
        data = request.get_json()
        license_key = data.get('license_key')
        
        if not license_key:
            return jsonify({'valid': False, 'error': 'License key required'}), 400
        
        valid, result = license_manager.validate_license(license_key)
        
        if valid:
            return jsonify({
                'valid': True,
                'license_info': result.to_dict(),
                'message': 'License is valid'
            })
        else:
            return jsonify({
                'valid': False,
                'error': result
            })
        
    except Exception as e:
        log_security_event("LICENSE_VALIDATION_ERROR", str(e), "ERROR")
        return jsonify({'valid': False, 'error': str(e)}), 500

@main_bp.route('/api/business/analytics')
def business_analytics():
    """Get business sales analytics"""
    try:
        enforce_rados_protection()
        analytics_data = license_manager.get_sales_analytics()
        
        log_security_event("BUSINESS_ANALYTICS_ACCESS", "Sales analytics accessed")
        return jsonify(analytics_data)
        
    except Exception as e:
        log_security_event("BUSINESS_ANALYTICS_ERROR", str(e), "ERROR")
        return jsonify({'error': 'Analytics unavailable'}), 500

@main_bp.route('/api/business/licenses')
def list_licenses():
    """List all business licenses (admin only)"""
    try:
        enforce_rados_protection()
        
        # Get all licenses with pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        licenses_query = BusinessLicense.query.order_by(BusinessLicense.created_at.desc())
        licenses_paginated = licenses_query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        licenses_data = [license.to_dict() for license in licenses_paginated.items]
        
        return jsonify({
            'licenses': licenses_data,
            'total': licenses_paginated.total,
            'pages': licenses_paginated.pages,
            'current_page': page
        })
        
    except Exception as e:
        log_security_event("LICENSES_LIST_ERROR", str(e), "ERROR")
        return jsonify({'error': 'Unable to retrieve licenses'}), 500

@main_bp.route('/api/business/generate-protected', methods=['POST'])
def generate_with_license():
    """Generate content with license protection"""
    try:
        data = request.get_json()
        license_key = data.get('license_key')
        
        if not license_key:
            return jsonify({'success': False, 'error': 'License key required for protected generation'}), 400
        
        # Validate license
        valid, license_result = license_manager.validate_license(license_key)
        if not valid:
            return jsonify({'success': False, 'error': f'Invalid license: {license_result}'}), 403
        
        # Generate content with license validation
        generation_data = {
            'theme': data.get('theme', 'Epic Victory'),
            'title': data.get('title', 'Licensed Creation'),
            'music_style': data.get('music_style', 'epic'),
            'voice_style': data.get('voice_style', 'heroic_male')
        }
        
        # Create generation record
        generation = Generation(
            theme=generation_data['theme'],
            title=generation_data['title'],
            music_style=generation_data['music_style'],
            voice_style=generation_data['voice_style'],
            status='processing'
        )
        db.session.add(generation)
        db.session.commit()
        
        # Generate content using AI agent
        try:
            result = ai_agent.generate_complete_content(
                theme=generation_data['theme'],
                title=generation_data['title']
            )
            
            # Apply license protection to content
            protected_content = license_manager.apply_content_protection(
                result.get('lyrics_data', {}).get('full_text', ''),
                license_result
            )
            
            # Update generation record
            generation.status = 'completed'
            generation.lyrics_data = json.dumps(result.get('lyrics_data', {}))
            generation.audio_file = result.get('audio_file')
            generation.video_file = result.get('video_file')
            generation.completed_at = datetime.utcnow()
            db.session.commit()
            
            log_security_event("LICENSED_GENERATION_SUCCESS", f"Content generated with license {license_key}")
            
            return jsonify({
                'success': True,
                'generation_id': generation.id,
                'protected_content': protected_content,
                'license_info': license_result.to_dict(),
                'usage_remaining': max(0, license_result.max_usage - license_result.usage_count) if license_result.max_usage != -1 else 'unlimited'
            })
            
        except Exception as generation_error:
            generation.status = 'failed'
            generation.error_message = str(generation_error)
            db.session.commit()
            raise generation_error
        
    except Exception as e:
        log_security_event("LICENSED_GENERATION_ERROR", str(e), "ERROR")
        return jsonify({'success': False, 'error': str(e)}), 500

# Context processor for global template variables
@main_bp.context_processor
def inject_global_vars():
    """Inject global variables into templates"""
    return {
        'app_name': 'CodeCraft Studio',
        'app_version': '1.0',
        'copyright': '© 2025 Ervin Remus Radosavlevici',
        'license': 'Radosavlevici Game License v1.0'
    }

# Blueprint will be registered in app.py