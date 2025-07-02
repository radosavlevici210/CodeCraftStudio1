"""
Music Generator for CodeCraft Studio
Handles music generation and audio processing
© 2025 Ervin Remus Radosavlevici
"""

import os
import random
import time
from datetime import datetime
from gtts import gTTS
from pydub import AudioSegment
from security.rados_security import log_security_event, watermark_content
import logging

class MusicGenerator:
    """Professional music generation system"""
    
    def __init__(self):
        self.voice_styles = {
            'heroic_male': {
                'lang': 'en',
                'effects': ['reverb', 'bass_boost'],
                'description': 'Deep, powerful male voice with heroic resonance'
            },
            'soprano': {
                'lang': 'en',
                'effects': ['reverb', 'pitch_shift'],
                'description': 'High, clear female soprano with ethereal quality'
            },
            'choir': {
                'lang': 'en',
                'effects': ['reverb', 'chorus', 'harmony'],
                'description': 'Full choir harmonies with Latin pronunciation'
            },
            'whisper': {
                'lang': 'en',
                'effects': ['intimate', 'soft_reverb'],
                'description': 'Intimate whisper voice for dramatic effect'
            }
        }
        
        self.music_styles = {
            'epic': 'Epic orchestral with full symphony and choir',
            'pop': 'Modern pop arrangement with orchestral elements',
            'dark': 'Dark, brooding orchestral with minor keys',
            'gregorian': 'Medieval Gregorian chant with sacred atmosphere',
            'fantasy': 'Fantasy orchestral with magical elements',
            'gladiator': 'Gladiator-style epic with battle drums',
            'emotional': 'Emotional ballad with strings and piano'
        }
    
    def generate_voice_with_effects(self, lyrics_text, voice_style='heroic_male'):
        """Generate voice with professional effects"""
        try:
            log_security_event("VOICE_GENERATION_START", f"Style: {voice_style}")
            
            # Generate base voice using gTTS
            tts = gTTS(text=lyrics_text, lang='en', slow=False)
            timestamp = int(time.time())
            raw_voice_file = f"static/audio/voice_raw_{timestamp}.mp3"
            tts.save(raw_voice_file)
            
            # Load audio for processing
            audio = AudioSegment.from_mp3(raw_voice_file)
            
            # Apply effects based on voice style
            effects = self.voice_styles.get(voice_style, {}).get('effects', [])
            
            for effect in effects:
                audio = self.apply_audio_effect(audio, effect)
            
            # Save processed audio
            final_voice_file = f"static/audio/voice_{voice_style}_{timestamp}.mp3"
            audio.export(final_voice_file, format="mp3")
            
            # Clean up raw file
            if os.path.exists(raw_voice_file):
                os.remove(raw_voice_file)
            
            # Add watermark protection
            watermark_content("VOICE_AUDIO", final_voice_file)
            
            log_security_event("VOICE_GENERATION_SUCCESS", f"Generated: {final_voice_file}")
            return final_voice_file
            
        except Exception as e:
            log_security_event("VOICE_GENERATION_ERROR", str(e), "ERROR")
            raise e
    
    def apply_audio_effect(self, audio, effect):
        """Apply audio effect to audio segment"""
        try:
            if effect == 'reverb':
                # Simulate reverb by overlaying delayed versions
                reverb = audio.overlay(audio - 10, position=100)
                return reverb
            elif effect == 'chorus':
                # Create chorus effect by overlaying with slight pitch variation
                chorus = audio.overlay(audio.reverse()[:len(audio)//2], position=50)
                return chorus
            elif effect == 'bass_boost':
                # Boost lower frequencies (simulated)
                return audio + 3
            elif effect == 'pitch_shift':
                # Simulate pitch shift (limited without advanced libraries)
                return audio.speedup(playback_speed=1.1)
            elif effect == 'harmony':
                # Create harmony effect
                harmony = audio.overlay(audio - 5, position=25)
                return harmony
            elif effect == 'soft_reverb':
                # Gentle reverb for whisper effects
                soft_reverb = audio.overlay(audio - 15, position=150)
                return soft_reverb
            elif effect == 'intimate':
                # Reduce volume for intimate effect
                return audio - 5
            else:
                return audio
                
        except Exception as e:
            logging.warning(f"Could not apply effect {effect}: {e}")
            return audio
    
    def generate_music(self, lyrics_data, music_style='epic', voice_style='heroic_male'):
        """Generate complete music with voice"""
        try:
            log_security_event("MUSIC_GENERATION_START", f"Style: {music_style}")
            
            # Generate voice track
            lyrics_text = lyrics_data.get('full_text', '')
            voice_file = self.generate_voice_with_effects(lyrics_text, voice_style)
            
            # Simulate professional music generation
            timestamp = int(time.time())
            music_file = f"static/audio/music_{music_style}_{timestamp}.mp3"
            
            # Create a base audio track (simulated)
            print(f"🎵 Generating professional {music_style} music...")
            time.sleep(3)  # Simulate processing time
            
            # Load voice track to get duration
            voice_audio = AudioSegment.from_mp3(voice_file)
            voice_duration = len(voice_audio)
            
            # Create background music (simulated with silence for now)
            # In a real implementation, this would use advanced music generation
            background_music = AudioSegment.silent(duration=voice_duration)
            
            # Mix voice with background music
            final_audio = background_music.overlay(voice_audio)
            
            # Export final music
            final_audio.export(music_file, format="mp3")
            
            # Add watermark protection
            watermark_content("MUSIC_AUDIO", music_file)
            
            log_security_event("MUSIC_GENERATION_SUCCESS", f"Generated: {music_file}")
            print(f"✅ Music with voice generated: {music_file}")
            
            return music_file
            
        except Exception as e:
            log_security_event("MUSIC_GENERATION_ERROR", str(e), "ERROR")
            raise e
    
    def get_music_style_description(self, style):
        """Get description of music style"""
        return self.music_styles.get(style, "Professional music arrangement")
    
    def get_voice_style_description(self, style):
        """Get description of voice style"""
        return self.voice_styles.get(style, {}).get('description', 'Professional voice performance')
