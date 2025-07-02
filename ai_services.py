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
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "default_openai_key")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def generate_lyrics(theme, title="Invictus Aeternum"):
    """Generate lyrics based on theme using OpenAI"""
    try:
        log_security_event("LYRICS_GENERATION_START", f"Theme: {theme}, Title: {title}")
        
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
            max_tokens=1500
        )
        
        lyrics_data = json.loads(response.choices[0].message.content)
        log_security_event("LYRICS_GENERATION_SUCCESS", f"Generated lyrics for: {title}")
        
        return lyrics_data
        
    except Exception as e:
        log_security_event("LYRICS_GENERATION_ERROR", str(e), "ERROR")
        # Return fallback lyrics
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
        
        prompt = f"""
        Create a detailed music production prompt for generating {music_style} music with these lyrics:
        
        Lyrics: {lyrics_text}
        Mood: {mood}
        Style: {music_style}
        
        Generate a professional music production description including:
        - Instrumentation details
        - Tempo and rhythm suggestions
        - Vocal arrangement guidance
        - Audio effects recommendations
        - Overall production notes
        
        Return as JSON with detailed production specifications.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional music producer specializing in cinematic and orchestral arrangements."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=800
        )
        
        enhancement_data = json.loads(response.choices[0].message.content)
        log_security_event("MUSIC_ENHANCEMENT_SUCCESS", f"Enhanced prompt for {music_style}")
        
        return enhancement_data
        
    except Exception as e:
        log_security_event("MUSIC_ENHANCEMENT_ERROR", str(e), "ERROR")
        return {
            "instrumentation": f"Full orchestra with {music_style} arrangement",
            "tempo": "Moderate to fast",
            "effects": "Reverb, chorus, orchestral processing",
            "notes": f"Professional {music_style} production"
        }
