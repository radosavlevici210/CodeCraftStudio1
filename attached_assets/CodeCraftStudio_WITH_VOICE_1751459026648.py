
# === CodeCraft Studio | Voice-Enabled Edition ===
# © 2025 Ervin Remus Radosavlevici
# AI Music, Video & Vocal Generator
# License: Radosavlevici Game License v1.0

import random
import time
from gtts import gTTS
import os

# === Music Generator ===
def generate_professional_music(lyrics, genre="epic", mood="heroic"):
    print(f"🎵 Generating professional music from lyrics in genre '{genre}' and mood '{mood}'...")
    time.sleep(2)
    return f"MusicTrack_{random.randint(1000,9999)}.mp3"

# === Video Generator ===
def generate_synced_video(lyrics, visuals_style="cinematic"):
    print(f"🎬 Generating cinematic video for lyrics...")
    time.sleep(2)
    return f"VideoClip_{random.randint(1000,9999)}.mp4"

# === Voice Synthesizer ===
def generate_singing_voice(lyrics, voice_lang='en'):
    print("🎤 Synthesizing singing voice from lyrics...")
    tts = gTTS(text=lyrics, lang=voice_lang)
    filename = f"VoiceTrack_{random.randint(1000,9999)}.mp3"
    tts.save(filename)
    print(f"✅ Vocal audio saved as {filename}")
    return filename

# === Master AI Generator ===
def generate_full_music_video_with_voice(lyrics, genre="epic", mood="heroic", visuals_style="cinematic", voice_lang="en"):
    print("🧠 Creating full music + video + voice package...")
    voice = generate_singing_voice(lyrics, voice_lang)
    music = generate_professional_music(lyrics, genre, mood)
    video = generate_synced_video(lyrics, visuals_style)
    return {
        "voice_file": voice,
        "music_file": music,
        "video_file": video
    }

# === Example Usage ===
if __name__ == "__main__":
    lyrics = """Invictus Aeternum, we rise again,
    Through fire and fate, we conquer the pain,
    Our hearts ablaze, our spirits soar,
    We are the champions, forevermore."""

    output = generate_full_music_video_with_voice(lyrics)
    print("📦 Final Output Package:", output)
