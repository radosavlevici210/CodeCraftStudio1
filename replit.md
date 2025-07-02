# CodeCraft Studio - AI Music & Video Generator

## Overview

CodeCraft Studio is an AI-powered web application that generates cinematic music, vocal tracks, and synchronized video content from user-provided themes. The system combines advanced AI services with a self-learning agent to create epic orchestral compositions with professional voice synthesis and cinematic visuals.

## System Architecture

### Frontend Architecture
- **Framework**: Flask web application with Jinja2 templating
- **UI Components**: Bootstrap 5 for responsive design with custom CSS styling
- **JavaScript**: Vanilla JavaScript for interactive features and form handling
- **Theme**: Dark theme with gold accents for a cinematic aesthetic

### Backend Architecture
- **Web Framework**: Flask with SQLAlchemy ORM
- **Database**: SQLite (default) with support for PostgreSQL via DATABASE_URL environment variable
- **AI Integration**: OpenAI API for lyrics generation and content enhancement
- **Audio Processing**: gTTS (Google Text-to-Speech) and pydub for voice synthesis and audio manipulation
- **Video Generation**: Custom video generator with matplotlib for visualizations

### Data Storage
- **Primary Database**: SQLAlchemy with three main models:
  - `Generation`: Stores generation requests and results
  - `LearningData`: Stores AI learning data for continuous improvement
  - `SecurityLog`: Tracks security events and system access
- **File Storage**: Static files stored in organized directories (audio, video, downloads)
- **Session Management**: Flask sessions with configurable secret key

## Key Components

### AI Agent (InvictusAIAgent)
- **Self-Learning Capabilities**: Improves performance with each generation
- **Style Management**: Handles voice styles (heroic_male, soprano, choir, whisper) and music styles (epic, pop, dark, gregorian, fantasy, gladiator, emotional)
- **Learning Data**: Tracks and analyzes generation patterns for optimization

### Music Generator
- **Voice Synthesis**: Professional vocal generation with effects (reverb, bass boost, pitch shift)
- **Audio Processing**: Advanced audio manipulation using pydub
- **Style Mapping**: Connects themes to appropriate musical styles

### Video Generator
- **Scene Templates**: Predefined cinematic scenes (epic_battle, sacred_temple, emotional_closeup)
- **Synchronization**: Aligns video content with audio tracks
- **Visualization**: Creates waveform visualizations and cinematic effects

### Security System (RADOS)
- **Event Logging**: Comprehensive security event tracking
- **Content Protection**: Watermarking and theft detection
- **Access Control**: IP tracking and user agent monitoring

## Data Flow

1. **User Input**: Theme, title, voice style, and music style selection
2. **AI Processing**: OpenAI generates lyrics based on theme and preferences
3. **Audio Generation**: Voice synthesis with selected style and effects
4. **Music Creation**: Orchestral music generation matching the theme
5. **Video Synthesis**: Cinematic video synchronized with audio content
6. **Learning Update**: System learns from generation results for improvement
7. **Output Delivery**: Complete package with audio, video, and metadata

## External Dependencies

### AI Services
- **OpenAI API**: GPT-4 for lyrics generation and content enhancement
- **Google Text-to-Speech**: Voice synthesis functionality

### Audio/Video Processing
- **pydub**: Audio manipulation and effects processing
- **matplotlib**: Video visualization and waveform generation
- **numpy**: Mathematical operations for audio processing

### Web Framework
- **Flask**: Core web application framework
- **SQLAlchemy**: Database ORM and management
- **Bootstrap 5**: Frontend UI framework
- **Font Awesome**: Icon library

## Deployment Strategy

### Environment Configuration
- **Database**: Configurable via DATABASE_URL (SQLite default, PostgreSQL support)
- **API Keys**: OpenAI API key via OPENAI_API_KEY environment variable
- **Session Security**: Configurable secret key via SESSION_SECRET

### File Management
- **Static Directories**: Automatic creation of required directories (audio, video, downloads, logs)
- **Asset Organization**: Structured file storage with timestamp-based naming

### Security Considerations
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies
- **Session Management**: Secure session handling with configurable keys
- **Request Logging**: Comprehensive logging of all system interactions

## Recent Changes

### July 02, 2025 - Production Migration and AI Enhancement
- **Production Migration Complete**: Successfully migrated from Replit Agent to production environment with full security and stability
- **OpenAI Integration Active**: Configured OpenAI GPT-4o for real-time lyrics generation and music enhancement
- **Enhanced Content Protection**: Implemented RADOS Quantum Enforcement Policy v2.7 with blessing/curse protection system
- **Performance Optimization**: Resolved all timeout issues and worker crashes for stable production operation
- **Audio Generation Fixed**: Resolved TTS and audio processing issues with FFmpeg integration and fallback systems
- **Security Enhancements**: Added unauthorized access detection and comprehensive content watermarking
- **Real AI Music Composition**: Advanced harmonic progression generation, orchestral layers, and professional mastering chain
- **AI-Powered Video Generation**: OpenAI integration for scene enhancement and intelligent composition
- **YouTube Upload System**: Comprehensive upload automation with AI-generated metadata and scheduling
- **Real-Time Collaboration**: Multi-user workspace with live editing and voice chat support
- **Advanced Audio Mixer**: Professional mixing system with AI-powered decisions and mastering chain
- **Custom Voice Training**: Voice model creation, training simulation, and quality evaluation

### New API Endpoints Added
- `/api/youtube/upload` - Automated YouTube uploads
- `/api/collaboration/create` - Create collaborative sessions
- `/api/collaboration/join` - Join collaborative sessions  
- `/api/collaboration/updates/<session_id>` - Live collaboration updates
- `/api/audio/mix` - Professional audio mixing
- `/api/voice/train` - Custom voice model training
- `/api/voice/synthesize` - Custom voice synthesis
- `/api/voice/evaluate` - Voice quality evaluation

### New Dashboard Pages
- `/collaboration` - Real-time collaboration interface
- `/voice-training` - Custom voice training dashboard
- `/audio-mixer` - Professional mixing interface

## Changelog

- July 02, 2025. Initial setup and advanced features implementation complete

## User Preferences

Preferred communication style: Simple, everyday language.