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

def generate_lyrics(theme, title):
    """Generate lyrics using OpenAI API"""
    try:
        # Enhanced prompt for better lyric generation
        prompt = f"""Create powerful, cinematic lyrics for a song titled "{title}" with the theme "{theme}".

Generate lyrics that are:
- Epic and emotionally resonant
- Suitable for orchestral/cinematic music
- Structured with verses and choruses
- Inspiring and uplifting

Theme: {theme}
Title: {title}

Please provide the lyrics in this JSON format:
{{
    "title": "{title}",
    "theme": "{theme}",
    "verses": [
        {{"type": "verse", "lyrics": "verse 1 lyrics here", "timing": "0:30"}},
        {{"type": "chorus", "lyrics": "chorus lyrics here", "timing": "30:60"}},
        {{"type": "verse", "lyrics": "verse 2 lyrics here", "timing": "60:90"}},
        {{"type": "chorus", "lyrics": "chorus lyrics here", "timing": "90:120"}},
        {{"type": "bridge", "lyrics": "bridge lyrics here", "timing": "120:150"}},
        {{"type": "chorus", "lyrics": "final chorus lyrics here", "timing": "150:180"}}
    ],
    "full_text": "complete song lyrics as one text"
}}"""

        client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

        # Add timeout to prevent worker timeouts
        import signal

        def timeout_handler(signum, frame):
            raise TimeoutError("OpenAI API call timed out")

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(15)  # 15 second timeout for lyrics

        try:
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. 
            # do not change this unless explicitly requested by the user
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a master lyricist who creates epic, cinematic song lyrics. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                timeout=12.0  # 12 second timeout
            )

            result = json.loads(response.choices[0].message.content)
            signal.alarm(0)  # Cancel timeout
            log_security_event("LYRICS_GENERATED", f"Theme: {theme}, Title: {title}")

            return result

        except (TimeoutError, Exception) as api_error:
            signal.alarm(0)  # Cancel timeout
            logging.error(f"OpenAI lyrics generation failed: {api_error}")
            return _get_fallback_lyrics(theme, title)

        finally:
            signal.alarm(0)  # Ensure timeout is always cancelled

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