
"""
Production Import Handler
Handles missing dependencies gracefully for production deployment
© 2025 Ervin Remus Radosavlevici
"""

import sys
import logging

def safe_import_audio_libs():
    """Safely import audio libraries with fallbacks"""
    audio_libs = {}
    
    try:
        import soundfile as sf
        audio_libs['soundfile'] = sf
    except ImportError:
        logging.warning("soundfile not available - audio processing limited")
        audio_libs['soundfile'] = None
    
    try:
        import librosa
        audio_libs['librosa'] = librosa
    except ImportError:
        logging.warning("librosa not available - advanced audio features disabled")
        audio_libs['librosa'] = None
    
    try:
        from pydub import AudioSegment
        audio_libs['pydub'] = AudioSegment
    except ImportError:
        logging.warning("pydub not available - basic audio processing disabled")
        audio_libs['pydub'] = None
    
    return audio_libs

def check_production_dependencies():
    """Check and report production dependencies status"""
    required_libs = [
        'flask', 'flask_sqlalchemy', 'openai', 'gunicorn', 
        'numpy', 'gtts', 'requests', 'pillow'
    ]
    
    missing_libs = []
    for lib in required_libs:
        try:
            __import__(lib.replace('_', '.'))
        except ImportError:
            missing_libs.append(lib)
    
    if missing_libs:
        logging.error(f"Missing critical dependencies: {missing_libs}")
        return False
    
    logging.info("All critical dependencies available")
    return True

def safe_import_audio_libs():
    """Safely import audio libraries with fallbacks"""
    audio_libs = {}
    
    # Try to import soundfile
    try:
        import soundfile as sf
        audio_libs['soundfile'] = sf
    except ImportError:
        logging.warning("soundfile not available - audio features limited")
        audio_libs['soundfile'] = None
    
    # Try to import librosa
    try:
        import librosa
        audio_libs['librosa'] = librosa
    except ImportError:
        logging.warning("librosa not available - advanced audio features disabled")
        audio_libs['librosa'] = None
    
    # Try to import pydub
    try:
        from pydub import AudioSegment
        audio_libs['pydub'] = AudioSegment
    except ImportError:
        logging.warning("pydub not available - basic audio processing disabled")
        audio_libs['pydub'] = None
    
    return audio_libs

# Initialize audio libraries safely
AUDIO_LIBS = safe_import_audio_libs())
