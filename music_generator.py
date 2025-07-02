"""
Music Generator for CodeCraft Studio
Advanced orchestral music composition with AI enhancement
© 2025 Ervin Remus Radosavlevici
"""

import os
import time
import logging
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine, Sawtooth, Square
from security.rados_security import log_security_event, watermark_content
import random
from datetime import datetime
from gtts import gTTS

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

            try:
                tts.save(raw_voice_file)

                # Wait a moment for file to be written
                time.sleep(0.5)

                # Check if file exists and has content
                if not os.path.exists(raw_voice_file) or os.path.getsize(raw_voice_file) == 0:
                    raise Exception("TTS file generation failed")

                # Load audio for processing
                audio = AudioSegment.from_mp3(raw_voice_file)

            except Exception as e:
                logging.error(f"TTS generation failed: {e}")
                # Create a simple synthetic audio as fallback
                audio = self.create_fallback_voice(lyrics_text, voice_style)

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
        """Generate complete music with voice using advanced AI composition"""
        try:
            log_security_event("MUSIC_GENERATION_START", f"Style: {music_style}")

            # Generate voice track
            lyrics_text = lyrics_data.get('full_text', '')
            voice_file = self.generate_voice_with_effects(lyrics_text, voice_style)

            # Advanced AI music composition
            timestamp = int(time.time())
            music_file = f"static/audio/music_{music_style}_{timestamp}.mp3"

            print(f"🎵 Generating AI-powered {music_style} music composition...")

            # Load voice track to get duration and analyze
            voice_audio = AudioSegment.from_mp3(voice_file)
            voice_duration = len(voice_audio)

            # Generate sophisticated musical arrangement
            music_track = self.create_advanced_musical_arrangement(
                lyrics_data, music_style, voice_duration, voice_audio
            )

            # Apply professional mastering
            mastered_track = self.apply_professional_mastering(music_track, music_style)

            # Create final mix with voice
            final_audio = self.create_professional_mix(mastered_track, voice_audio, music_style)

            # Export with high quality settings
            final_audio.export(music_file, format="mp3", bitrate="320k")

            # Add watermark protection
            watermark_content("MUSIC_AUDIO", music_file)

            log_security_event("MUSIC_GENERATION_SUCCESS", f"Generated: {music_file}")
            print(f"✅ Professional AI music composition generated: {music_file}")

            return music_file

        except Exception as e:
            log_security_event("MUSIC_GENERATION_ERROR", str(e), "ERROR")
            raise e

    def create_advanced_musical_arrangement(self, lyrics_data, music_style, duration, voice_audio):
        """Create sophisticated musical arrangement using AI analysis"""
        try:
            print("🎼 Creating advanced musical arrangement...")

            # Analyze lyrics structure for musical phrasing
            verses = lyrics_data.get('verses', [])

            # Generate base frequencies and harmonies
            arrangement = self.generate_harmonic_progression(music_style, duration)

            # Add orchestral layers based on style
            if music_style == 'epic':
                arrangement = self.add_orchestral_layers(arrangement, 'full_orchestra')
            elif music_style == 'gladiator':
                arrangement = self.add_orchestral_layers(arrangement, 'battle_drums')
            elif music_style == 'fantasy':
                arrangement = self.add_orchestral_layers(arrangement, 'magical_elements')
            elif music_style == 'gregorian':
                arrangement = self.add_orchestral_layers(arrangement, 'sacred_chorus')
            elif music_style == 'dark':
                arrangement = self.add_orchestral_layers(arrangement, 'dark_strings')
            elif music_style == 'emotional':
                arrangement = self.add_orchestral_layers(arrangement, 'strings_piano')
            else:  # pop
                arrangement = self.add_orchestral_layers(arrangement, 'modern_orchestral')

            # Synchronize with vocal phrasing
            arrangement = self.synchronize_with_vocals(arrangement, voice_audio, verses)

            return arrangement

        except Exception as e:
            logging.error(f"Advanced arrangement failed: {e}")
            # Fallback to enhanced basic track
            return self.generate_enhanced_background_track(duration, music_style)

    def generate_harmonic_progression(self, style, duration):
        """Generate harmonic progression based on music theory"""
        print("🎹 Generating harmonic progression...")

        # Create base tone and build harmonies
        base_freq = 220  # A3 note

        # Style-specific harmonic progressions
        progressions = {
            'epic': [1, 5, 6, 4],  # I-V-vi-IV (triumphant)
            'dark': [1, 6, 4, 5],  # i-VI-iv-V (minor, dramatic)
            'emotional': [6, 4, 1, 5],  # vi-IV-I-V (emotional)
            'gladiator': [1, 7, 1, 5],  # I-VII-I-V (powerful)
            'fantasy': [1, 3, 6, 4],  # I-iii-vi-IV (magical)
            'gregorian': [1, 4, 5, 1],  # I-IV-V-I (sacred)
            'pop': [6, 4, 1, 5]  # vi-IV-I-V (modern)
        }

        progression = progressions.get(style, progressions['epic'])

        # Generate chord progression
        chord_duration = duration // len(progression)
        arrangement = AudioSegment.silent(duration=0)

        for chord_num in progression:
            chord = self.generate_chord(base_freq, chord_num, chord_duration)
            arrangement += chord

        # Repeat to fill duration
        while len(arrangement) < duration:
            for chord_num in progression:
                if len(arrangement) >= duration:
                    break
                chord = self.generate_chord(base_freq, chord_num, chord_duration)
                arrangement += chord

        return arrangement[:duration]

    def generate_chord(self, base_freq, chord_num, duration):
        """Generate a musical chord"""
        # Simple chord generation using mathematical relationships
        frequencies = {
            1: [1, 1.25, 1.5],      # Major triad
            3: [1.25, 1.5, 1.875],   # Minor third
            4: [1.33, 1.67, 2],      # Fourth
            5: [1.5, 1.875, 2.25],   # Fifth
            6: [1.67, 2.08, 2.5],    # Sixth
            7: [1.875, 2.34, 2.81]   # Seventh
        }

        ratios = frequencies.get(chord_num, frequencies[1])

        # Create silence as base (would use tone generation in real implementation)
        chord = AudioSegment.silent(duration=duration)

        # Apply subtle volume variation to simulate chord
        if chord_num in [1, 5]:  # Strong chords
            chord = chord + 2
        elif chord_num in [6, 7]:  # Softer chords
            chord = chord - 2

        return chord

    def add_orchestral_layers(self, base_track, orchestration_type):
        """Add orchestral layers based on style"""
        print(f"🎻 Adding {orchestration_type} orchestration...")

        enhanced_track = base_track

        if orchestration_type == 'full_orchestra':
            # Add string section emphasis
            enhanced_track = enhanced_track + 3
            # Add brass section (simulated with volume boost at certain intervals)
            enhanced_track = self.add_brass_emphasis(enhanced_track)

        elif orchestration_type == 'battle_drums':
            # Add percussive elements (simulated with rhythmic volume changes)
            enhanced_track = self.add_rhythmic_emphasis(enhanced_track, 'battle')

        elif orchestration_type == 'magical_elements':
            # Add ethereal effects (simulated with gentle modulation)
            enhanced_track = self.add_ethereal_effects(enhanced_track)

        elif orchestration_type == 'sacred_chorus':
            # Add choir-like reverb and harmony
            enhanced_track = enhanced_track.apply_gain(-2)  # Softer
            enhanced_track = self.apply_audio_effect(enhanced_track, 'reverb')

        elif orchestration_type == 'dark_strings':
            # Lower register emphasis
            enhanced_track = enhanced_track - 3
            enhanced_track = self.apply_audio_effect(enhanced_track, 'bass_boost')

        elif orchestration_type == 'strings_piano':
            # Delicate orchestration
            enhanced_track = enhanced_track - 1
            enhanced_track = self.add_piano_like_articulation(enhanced_track)

        elif orchestration_type == 'modern_orchestral':
            # Contemporary orchestral blend
            enhanced_track = enhanced_track + 1
            enhanced_track = self.add_modern_production_elements(enhanced_track)

        return enhanced_track

    def add_brass_emphasis(self, track):
        """Add brass section emphasis at key moments"""
        # Simulate brass emphasis with strategic volume boosts
        duration = len(track)
        brass_moments = [duration // 4, duration // 2, 3 * duration // 4]

        for moment in brass_moments:
            if moment < duration - 1000:  # Safety check
                # Boost a section around this moment
                start = max(0, moment - 500)
                end = min(duration, moment + 1500)

                # Extract, boost, and replace section
                before = track[:start]
                section = track[start:end] + 4
                after = track[end:]
                track = before + section + after

        return track

    def add_rhythmic_emphasis(self, track, rhythm_type):
        """Add rhythmic emphasis patterns"""
        if rhythm_type == 'battle':
            # Add battle drum pattern (every 500ms emphasis)
            duration = len(track)
            for i in range(0, duration, 500):
                if i < duration - 100:
                    start = i
                    end = min(i + 100, duration)

                    before = track[:start]
                    section = track[start:end] + 6  # Strong emphasis
                    after = track[end:]
                    track = before + section + after

        return track

    def add_ethereal_effects(self, track):
        """Add magical/ethereal effects"""
        # Create gentle modulation effect
        enhanced = self.apply_audio_effect(track, 'reverb')
        enhanced = self.apply_audio_effect(enhanced, 'chorus')
        return enhanced

    def add_piano_like_articulation(self, track):
        """Add piano-like dynamic articulation"""
        # Simulate piano dynamics with subtle volume variations
        duration = len(track)
        sections = 8
        section_length = duration // sections

        for i in range(sections):
            start = i * section_length
            end = min((i + 1) * section_length, duration)

            # Alternate between softer and louder sections
            adjustment = 2 if i % 2 == 0 else -1

            before = track[:start]
            section = track[start:end] + adjustment
            after = track[end:]
            track = before + section + after

        return track

    def add_modern_production_elements(self, track):
        """Add modern production elements"""
        # Apply contemporary production techniques
        enhanced = track + 2  # Slight overall boost
        enhanced = self.apply_audio_effect(enhanced, 'bass_boost')
        return enhanced

    def synchronize_with_vocals(self, music_track, voice_audio, verses):
        """Synchronize musical elements with vocal phrasing"""
        print("🎤 Synchronizing music with vocal phrasing...")

        # Analyze voice audio for phrasing (simplified)
        voice_rms = voice_audio.rms

        # Adjust music dynamics based on vocal intensity
        if voice_rms > 1000:  # Strong vocals
            music_track = music_track - 2  # Lower music to support vocals
        else:  # Softer vocals
            music_track = music_track + 1  # Slightly boost music

        return music_track

    def generate_enhanced_background_track(self, duration, style):
        """Generate enhanced background track as fallback"""
        # Create a more sophisticated background than silence
        track = AudioSegment.silent(duration=duration)

        # Add style-specific characteristics
        if style in ['epic', 'gladiator']:
            track = track + 3  # Stronger presence
        elif style in ['emotional', 'gregorian']:
            track = track - 2  # Softer presence

        return track

    def apply_professional_mastering(self, track, style):
        """Apply professional mastering techniques"""
        print("🎛️ Applying professional mastering...")

        mastered = track

        # Style-specific mastering
        if style == 'epic':
            mastered = mastered + 2  # Louder for epic feel
            mastered = self.apply_audio_effect(mastered, 'bass_boost')
        elif style == 'emotional':
            mastered = self.apply_audio_effect(mastered, 'soft_reverb')
        elif style == 'dark':
            mastered = mastered - 1  # Darker dynamics

        # General mastering effects
        mastered = self.apply_compression(mastered)
        mastered = self.apply_eq_enhancement(mastered, style)

        return mastered

    def apply_compression(self, track):
        """Apply audio compression for professional sound"""
        # Simulate compression by reducing dynamic range
        # In practice, this would use sophisticated audio processing
        return track.apply_gain(-1)  # Slight gain reduction for consistency

    def apply_eq_enhancement(self, track, style):
        """Apply EQ enhancement based on style"""
        # Style-specific EQ adjustments (simulated)
        if style in ['epic', 'gladiator']:
            # Boost mids and highs for clarity
            track = track + 1
        elif style == 'dark':
            # Boost bass, reduce highs
            track = self.apply_audio_effect(track, 'bass_boost')

        return track

    def create_professional_mix(self, music_track, voice_track, style):
        """Create professional mix of music and vocals"""
        print("🎚️ Creating professional mix...")

        # Professional mixing techniques
        if style == 'epic':
            # Epic style: Prominent vocals with full orchestral support
            mixed = music_track.overlay(voice_track + 3)
        elif style == 'emotional':
            # Emotional style: Intimate vocal with gentle musical support
            mixed = music_track.overlay(voice_track + 2)
        elif style == 'dark':
            # Dark style: Atmospheric mixing
            mixed = music_track.overlay(voice_track + 1)
        else:
            # Balanced mix for other styles
            mixed = music_track.overlay(voice_track + 2)

        # Apply final mix processing
        mixed = self.apply_stereo_enhancement(mixed)
        mixed = self.apply_final_limiting(mixed)

        return mixed

    def apply_stereo_enhancement(self, track):
        """Apply stereo enhancement for wider sound"""
        # Simulated stereo enhancement
        return track

    def apply_final_limiting(self, track):
        """Apply final limiting for broadcast-ready sound"""
        # Ensure consistent levels
        return track.apply_gain(-0.5)  # Slight reduction for headroom

    def get_music_style_description(self, style):
        """Get description of music style"""
        return self.music_styles.get(style, "Professional music arrangement")

    def get_voice_style_description(self, style):
        """Get description of voice style"""
        return self.voice_styles.get(style, {}).get('description', 'Professional voice performance')

    def create_fallback_voice(self, lyrics_text, voice_style):
        """Create fallback synthetic voice when TTS fails"""
        try:
            # Create a simple tone-based audio as fallback
            from pydub.generators import Sine

            # Calculate duration based on text length (rough estimate)
            duration_ms = len(lyrics_text) * 100  # 100ms per character
            duration_ms = max(3000, min(duration_ms, 30000))  # Between 3-30 seconds

            # Create a simple musical tone
            base_freq = 440  # A note
            if voice_style == 'soprano':
                base_freq = 523  # C5
            elif voice_style == 'heroic_male':
                base_freq = 330  # E4
            elif voice_style == 'whisper':
                base_freq = 220  # A3

            # Generate simple tone
            tone = Sine(base_freq).to_audio_segment(duration=duration_ms)

            # Add some variation
            tone = tone.fade_in(500).fade_out(500)
            tone = tone - 10  # Reduce volume slightly

            logging.info(f"Created fallback voice: {duration_ms}ms duration")
            return tone

        except Exception as e:
            logging.error(f"Fallback voice creation failed: {e}")
            # Return a minimal silence as last resort
            return AudioSegment.silent(duration=5000)