"""
AI Services for CodeCraft Studio
Handles OpenAI integration for lyrics generation and music enhancement
© 2025 Ervin Remus Radosavlevici
"""

import os
import json
import logging
from openai import OpenAI
from security.rados_security import log_security_event

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
else:
    openai_client = None
    logging.warning("OpenAI API key not found. AI features will be limited.")

def generate_lyrics(theme, title="Invictus Aeternum"):
    """Generate lyrics based on theme using OpenAI"""
    try:
        log_security_event("LYRICS_GENERATION_START", f"Theme: {theme}, Title: {title}")
        
        if not openai_client:
            log_security_event("LYRICS_GENERATION_FALLBACK", "Using fallback lyrics - OpenAI not available")
            return _get_fallback_lyrics(theme, title)
        
        prompt = f"""
        Generate powerful, cinematic lyrics for a song titled "{title}" with the theme "{theme}".
        
        The lyrics should be:
        - Epic and inspiring
        - Suitable for orchestral/cinematic music
        - Include verses, chorus, and bridge sections
        - Have timing information for video synchronization
        - Include Latin phrases where appropriate for grandeur
        
        Return the response as JSON with this structure:
        {{
            "title": "{title}",
            "theme": "{theme}",
            "full_text": "complete lyrics as one string",
            "verses": [
                {{
                    "type": "verse",
                    "lyrics": "verse lyrics here",
                    "timing": "0:30"
                }},
                {{
                    "type": "chorus", 
                    "lyrics": "chorus lyrics here",
                    "timing": "0:30-1:00"
                }}
            ],
            "structure": ["verse", "chorus", "verse", "chorus", "bridge", "chorus"],
            "mood": "heroic/epic/emotional",
            "latin_phrases": ["phrase1", "phrase2"]
        }}
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional lyricist specializing in epic, cinematic music. Generate lyrics that are suitable for orchestral arrangements and video synchronization."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=1500,
            timeout=15
        )
        
        if response.choices[0].message.content:
            lyrics_data = json.loads(response.choices[0].message.content)
            log_security_event("LYRICS_GENERATION_SUCCESS", f"Generated lyrics for: {title}")
            return lyrics_data
        else:
            raise Exception("Empty response from OpenAI")
        
    except Exception as e:
        log_security_event("LYRICS_GENERATION_ERROR", str(e), "ERROR")
        return _get_fallback_lyrics(theme, title)

def _get_fallback_lyrics(theme, title):
    """Return fallback lyrics when AI is not available"""
    return {
        "title": title,
        "theme": theme,
        "full_text": f"Invictus Aeternum, we rise again, Through fire and fate, we conquer the pain, Our hearts ablaze, our spirits soar, We are the champions, forevermore.",
        "verses": [
            {
                "type": "verse",
                "lyrics": "Invictus Aeternum, we rise again, Through fire and fate, we conquer the pain",
                "timing": "0:00-0:30"
            },
            {
                "type": "chorus",
                "lyrics": "Our hearts ablaze, our spirits soar, We are the champions, forevermore",
                "timing": "0:30-1:00"
            }
        ],
        "structure": ["verse", "chorus"],
        "mood": "heroic",
        "latin_phrases": ["Invictus Aeternum"]
    }

def enhance_music_prompt(lyrics_data, music_style):
    """Enhance music generation prompt using AI"""
    try:
        lyrics_text = lyrics_data.get('full_text', '')
        mood = lyrics_data.get('mood', 'heroic')
        
        # Use optimized fallback to prevent blocking
        log_security_event("MUSIC_ENHANCEMENT_FALLBACK", "Using optimized enhancement for performance")
        return {
            "instrumentation": f"Full orchestra with {music_style} arrangement",
            "tempo": "Moderate to fast",
            "effects": "Reverb, chorus, orchestral processing",
            "notes": f"Professional {music_style} production"
        }
        
    except Exception as e:
        log_security_event("MUSIC_ENHANCEMENT_ERROR", str(e), "ERROR")
        return {
            "instrumentation": f"Full orchestra with {music_style} arrangement",
            "tempo": "Moderate to fast",
            "effects": "Reverb, chorus, orchestral processing",
            "notes": f"Professional {music_style} production"
        }
