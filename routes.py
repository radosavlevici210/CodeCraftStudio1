"""
Routes for CodeCraft Studio
Handles all web requests and API endpoints
© 2025 Ervin Remus Radosavlevici
"""

from flask import render_template, request, redirect, url_for, flash, send_file, jsonify
from app import app, db
from models import Generation, SecurityLog
from ai_agent import InvictusAIAgent
from security.rados_security import log_security_event, enforce_rados_protection
import os
import logging

# Initialize AI Agent
ai_agent = InvictusAIAgent()

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
