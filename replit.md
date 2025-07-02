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

## Changelog

- July 02, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.