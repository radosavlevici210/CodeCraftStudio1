"""
YouTube Upload Service for CodeCraft Studio
Handles automated YouTube uploads with AI-generated metadata
© 2025 Ervin Remus Radosavlevici
"""

import os
import time
import json
import logging
from datetime import datetime
from security.rados_security import log_security_event, watermark_content
from ai_services import generate_lyrics, enhance_music_prompt
from openai import OpenAI

class YouTubeUploader:
    """Professional YouTube upload and management system"""
    
    def __init__(self):
        api_key = os.environ.get('OPENAI_API_KEY')
        if api_key:
            self.openai_client = OpenAI(api_key=api_key)
        else:
            self.openai_client = None
            logging.warning("OpenAI API key not found. AI features will be limited.")
        
        # YouTube upload configurations
        self.upload_configs = {
            'epic': {
                'category': 'Music',
                'tags': ['epic music', 'cinematic', 'orchestral', 'dramatic', 'film score'],
                'privacy': 'public'
            },
            'emotional': {
                'category': 'Music',
                'tags': ['emotional music', 'beautiful', 'touching', 'cinematic', 'soundtrack'],
                'privacy': 'public'
            },
            'dark': {
                'category': 'Music',
                'tags': ['dark music', 'atmospheric', 'mysterious', 'cinematic', 'ambient'],
                'privacy': 'public'
            },
            'fantasy': {
                'category': 'Music',
                'tags': ['fantasy music', 'magical', 'ethereal', 'adventure', 'medieval'],
                'privacy': 'public'
            },
            'gladiator': {
                'category': 'Music',
                'tags': ['gladiator music', 'roman', 'battle', 'epic', 'heroic'],
                'privacy': 'public'
            },
            'gregorian': {
                'category': 'Music',
                'tags': ['gregorian chant', 'sacred music', 'spiritual', 'medieval', 'religious'],
                'privacy': 'public'
            },
            'pop': {
                'category': 'Music',
                'tags': ['pop music', 'modern', 'contemporary', 'vocals', 'commercial'],
                'privacy': 'public'
            }
        }
        
        # Ensure upload directory exists
        os.makedirs('static/uploads', exist_ok=True)
        os.makedirs('logs/youtube', exist_ok=True)
    
    def prepare_upload_package(self, generation_data):
        """Prepare complete upload package for YouTube"""
        try:
            log_security_event("YOUTUBE_PACKAGE_START", f"Preparing package for generation {generation_data.get('id')}")
            
            print("📦 Preparing YouTube upload package...")
            
            # Generate AI-powered metadata
            metadata = self.generate_ai_metadata(generation_data)
            
            # Create upload package
            package = {
                'video_file': generation_data.get('video_file'),
                'audio_file': generation_data.get('audio_file'),
                'metadata': metadata,
                'thumbnail': self.generate_custom_thumbnail(generation_data),
                'upload_config': self.get_upload_config(generation_data.get('music_style', 'epic')),
                'generation_id': generation_data.get('id'),
                'created_at': datetime.utcnow().isoformat()
            }
            
            # Save package for processing
            package_file = f"static/uploads/package_{generation_data.get('id')}_{int(time.time())}.json"
            with open(package_file, 'w') as f:
                json.dump(package, f, indent=2)
            
            log_security_event("YOUTUBE_PACKAGE_SUCCESS", f"Package created: {package_file}")
            print(f"✅ YouTube package prepared: {package_file}")
            
            return package
            
        except Exception as e:
            log_security_event("YOUTUBE_PACKAGE_ERROR", str(e), "ERROR")
            raise e
    
    def generate_ai_metadata(self, generation_data):
        """Generate AI-powered YouTube metadata"""
        try:
            print("🤖 Generating AI-powered YouTube metadata...")
            
            theme = generation_data.get('theme', 'Epic Journey')
            title = generation_data.get('title', 'Invictus Aeternum')
            music_style = generation_data.get('music_style', 'epic')
            lyrics_data = generation_data.get('lyrics_data', {})
            
            if not self.openai_client:
                log_security_event("YOUTUBE_METADATA_FALLBACK", "Using fallback metadata - OpenAI not available")
                ai_metadata = self._get_fallback_metadata(title, theme, music_style)
            else:
                # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. 
                # do not change this unless explicitly requested by the user
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional YouTube content strategist and SEO expert. "
                                       "Create compelling YouTube metadata for AI-generated music videos. "
                                       "Focus on discovery, engagement, and professional presentation. "
                                       "Respond with JSON containing: title, description, tags, and seo_keywords."
                        },
                        {
                            "role": "user",
                            "content": f"Create YouTube metadata for this AI-generated music: "
                                       f"Title: {title}, Theme: {theme}, Style: {music_style}, "
                                       f"Lyrics preview: {str(lyrics_data)[:200]}..."
                        }
                    ],
                    response_format={"type": "json_object"}
                )
                
                if response.choices[0].message.content:
                    ai_metadata = json.loads(response.choices[0].message.content)
                else:
                    ai_metadata = self._get_fallback_metadata(title, theme, music_style)
            
            # Enhance with studio branding
            enhanced_metadata = {
                'title': f"{ai_metadata.get('title', title)} | CodeCraft Studio",
                'description': self.create_professional_description(ai_metadata, generation_data),
                'tags': ai_metadata.get('tags', []) + ['AI Music', 'CodeCraft Studio', 'Generated Music'],
                'seo_keywords': ai_metadata.get('seo_keywords', []),
                'category': 'Music',
                'language': 'en',
                'ai_generated': True
            }
            
            return enhanced_metadata
            
        except Exception as e:
            logging.warning(f"AI metadata generation failed: {e}")
            return self.create_fallback_metadata(generation_data)
    
    def create_professional_description(self, ai_metadata, generation_data):
        """Create professional YouTube description"""
        base_description = ai_metadata.get('description', 'AI-generated cinematic music')
        
        description = f"""{base_description}

🎵 Generated by CodeCraft Studio - AI Music & Video Generator
🤖 Powered by advanced AI composition and cinematic video generation
🎼 Style: {generation_data.get('music_style', 'Epic').title()}
🎭 Theme: {generation_data.get('theme', 'Epic Journey')}

✨ Features:
• AI-powered orchestral composition
• Professional voice synthesis with effects
• Cinematic video with synchronized visuals
• Dynamic scene transitions and color grading
• High-quality audio mastering (320kbps)

🔧 Technology Stack:
• OpenAI GPT-4 for lyrics generation
• Advanced audio processing with pydub
• Professional video composition
• Machine learning for style optimization

📅 Generated: {datetime.utcnow().strftime('%B %d, %Y')}
🏢 © 2025 Ervin Remus Radosavlevici
🛡️ Protected by RADOS Quantum Enforcement Policy v2.7

#AIMusic #CinematicMusic #GeneratedMusic #CodeCraftStudio #EpicMusic #AIComposition
"""
        return description
    
    def create_fallback_metadata(self, generation_data):
        """Create fallback metadata when AI is unavailable"""
        title = generation_data.get('title', 'Invictus Aeternum')
        theme = generation_data.get('theme', 'Epic Journey')
        style = generation_data.get('music_style', 'epic')
        
        return {
            'title': f"{title} - {theme} | CodeCraft Studio",
            'description': f"AI-generated {style} music with cinematic video. "
                          f"Theme: {theme}. Generated by CodeCraft Studio.",
            'tags': ['AI Music', 'Generated Music', 'CodeCraft Studio', style, 'Cinematic'],
            'category': 'Music',
            'language': 'en',
            'ai_generated': True
        }
    
    def generate_custom_thumbnail(self, generation_data):
        """Generate custom thumbnail for YouTube video"""
        try:
            print("🎨 Generating custom YouTube thumbnail...")
            
            theme = generation_data.get('theme', 'Epic Journey')
            style = generation_data.get('music_style', 'epic')
            
            if not self.openai_client:
                log_security_event("THUMBNAIL_GENERATION_FALLBACK", "Using fallback thumbnail - OpenAI not available")
                return self._get_fallback_thumbnail(theme, style)
            
            # Generate thumbnail using DALL-E
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=f"YouTube thumbnail for {style} music video: {theme}, "
                       f"professional design, bold text overlay, cinematic style, "
                       f"high contrast, eye-catching composition, 1280x720 aspect ratio",
                size="1024x1024",
                quality="hd"
            )
            
            if response.data and len(response.data) > 0:
                thumbnail_data = {
                    'url': response.data[0].url,
                    'style': style,
                    'theme': theme,
                    'generated_at': datetime.utcnow().isoformat()
                }
                return thumbnail_data
            else:
                return self._get_fallback_thumbnail(theme, style)
            
        except Exception as e:
            logging.warning(f"Custom thumbnail generation failed: {e}")
            return self.create_default_thumbnail(generation_data)
    
    def create_default_thumbnail(self, generation_data):
        """Create default thumbnail data"""
        return {
            'url': None,
            'style': generation_data.get('music_style', 'epic'),
            'theme': generation_data.get('theme', 'Epic Journey'),
            'default': True,
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def get_upload_config(self, music_style):
        """Get upload configuration for music style"""
        return self.upload_configs.get(music_style, self.upload_configs['epic'])
    
    def simulate_youtube_upload(self, package):
        """Simulate YouTube upload process (placeholder for real API integration)"""
        try:
            print("📤 Simulating YouTube upload process...")
            
            # Simulate upload steps
            steps = [
                "Authenticating with YouTube API",
                "Uploading video file",
                "Processing video",
                "Setting metadata",
                "Applying thumbnail",
                "Publishing video"
            ]
            
            for i, step in enumerate(steps):
                print(f"   {i+1}/6: {step}...")
                time.sleep(1)  # Simulate processing time
            
            # Create simulated upload result
            upload_result = {
                'video_id': f"sim_{int(time.time())}_{package['generation_id']}",
                'url': f"https://youtube.com/watch?v=sim_{package['generation_id']}",
                'status': 'uploaded',
                'visibility': package['upload_config']['privacy'],
                'uploaded_at': datetime.utcnow().isoformat(),
                'metadata': package['metadata'],
                'thumbnail': package['thumbnail']
            }
            
            # Save upload log
            log_file = f"logs/youtube/upload_{package['generation_id']}_{int(time.time())}.json"
            with open(log_file, 'w') as f:
                json.dump(upload_result, f, indent=2)
            
            log_security_event("YOUTUBE_UPLOAD_SUCCESS", f"Simulated upload: {upload_result['video_id']}")
            print(f"✅ YouTube upload completed: {upload_result['url']}")
            
            return upload_result
            
        except Exception as e:
            log_security_event("YOUTUBE_UPLOAD_ERROR", str(e), "ERROR")
            raise e
    
    def get_upload_analytics(self, video_id):
        """Get upload analytics and performance data"""
        try:
            # Simulate analytics data
            analytics = {
                'video_id': video_id,
                'views': 0,
                'likes': 0,
                'comments': 0,
                'shares': 0,
                'watch_time': '0:00',
                'engagement_rate': 0.0,
                'discovery_source': 'search',
                'audience_retention': 0.85,
                'last_updated': datetime.utcnow().isoformat()
            }
            
            return analytics
            
        except Exception as e:
            logging.error(f"Analytics retrieval failed: {e}")
            return None
    
    def schedule_upload(self, package, schedule_time):
        """Schedule YouTube upload for later"""
        try:
            print(f"📅 Scheduling upload for {schedule_time}")
            
            schedule_data = {
                'package': package,
                'scheduled_time': schedule_time,
                'status': 'scheduled',
                'created_at': datetime.utcnow().isoformat()
            }
            
            schedule_file = f"static/uploads/scheduled_{package['generation_id']}_{int(time.time())}.json"
            with open(schedule_file, 'w') as f:
                json.dump(schedule_data, f, indent=2)
            
            log_security_event("YOUTUBE_SCHEDULED", f"Upload scheduled: {schedule_file}")
            return schedule_data
            
        except Exception as e:
            log_security_event("YOUTUBE_SCHEDULE_ERROR", str(e), "ERROR")
            raise e
    
    def _get_fallback_metadata(self, title, theme, style):
        """Generate fallback metadata when AI is not available"""
        return {
            'title': f'{title} - {theme} | CodeCraft Studio',
            'description': f'AI-generated {style} music with cinematic video. Theme: {theme}. '
                          f'Created with CodeCraft Studio\'s advanced AI music generation system. '
                          f'Professional orchestral composition with synchronized visuals.',
            'tags': ['AI Music', 'Generated Music', 'CodeCraft Studio', style, 'Cinematic', 
                    'Orchestral', 'Epic Music', theme.replace(' ', '')],
            'seo_keywords': [f'{style} music', 'AI generated', 'cinematic', 'orchestral'],
            'category': 'Music',
            'language': 'en',
            'ai_generated': True
        }
    
    def _get_fallback_thumbnail(self, theme, style):
        """Generate fallback thumbnail data when AI is not available"""
        return {
            'url': None,
            'type': 'fallback',
            'description': f'CodeCraft Studio - {theme} ({style})',
            'dimensions': '1280x720',
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def batch_upload(self, packages):
        """Handle batch upload of multiple videos"""
        try:
            print(f"📦 Processing batch upload of {len(packages)} videos...")
            
            results = []
            for i, package in enumerate(packages):
                print(f"   Processing {i+1}/{len(packages)}: {package.get('metadata', {}).get('title', 'Unknown')}")
                
                try:
                    result = self.simulate_youtube_upload(package)
                    results.append(result)
                    time.sleep(2)  # Rate limiting
                    
                except Exception as upload_error:
                    logging.error(f"Batch upload item {i} failed: {upload_error}")
                    continue
            
            batch_result = {
                'total_packages': len(packages),
                'successful_uploads': len(results),
                'failed_uploads': len(packages) - len(results),
                'upload_results': results,
                'completed_at': datetime.utcnow().isoformat()
            }
            
            log_security_event("YOUTUBE_BATCH_COMPLETE", f"Batch upload completed: {len(results)}/{len(packages)}")
            return batch_result
            
        except Exception as e:
            log_security_event("YOUTUBE_BATCH_ERROR", str(e), "ERROR")
            raise e