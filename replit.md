# AI TaskMaster

## Overview

AI TaskMaster is a comprehensive Streamlit application that combines event management functionality with AI-powered challenges using Azure OpenAI. The application serves as a learning platform for AI integration, featuring both practical event management capabilities and educational AI exercises.

## System Architecture

### Frontend Architecture
- **Streamlit Web Application**: Main interface with multi-page navigation
- **Page-based routing**: Separate pages for event management and AI challenges
- **Custom CSS styling**: Dark mode support with responsive design
- **Client-side AI integration**: Direct Azure OpenAI client integration

### Backend Architecture
- **FastAPI REST API**: Asynchronous backend service running on port 8000
- **SQLAlchemy ORM**: Database abstraction layer for data operations
- **Pydantic schemas**: Request/response validation and serialization
- **CORS middleware**: Cross-origin resource sharing for frontend-backend communication

### Data Storage Solutions
- **SQLite database**: Local file-based database (`events.db`)
- **Events table**: Stores event management data with CRUD operations
- **Hosts table**: Manages event host information with unique constraints
- **Auto-generated schemas**: Database tables created automatically on startup

### Authentication and Authorization Mechanisms
- **Azure OpenAI authentication**: API key-based authentication with environment variables
- **No user authentication**: Current implementation is single-user focused
- **API security**: Basic CORS configuration for development environment

## Key Components

### Event Management System
- **Full CRUD operations**: Create, Read, Update, Delete events
- **Real-time backend communication**: Async requests to FastAPI endpoints
- **Form validation**: Input validation for event creation and updates
- **Status management**: Event status tracking (open, fully booked, completed)

### AI Challenge Framework
- **Multi-challenge structure**: Four distinct AI learning challenges
- **Azure OpenAI integration**: Direct API calls with error handling
- **Prompt engineering**: Templates for different AI interaction patterns
- **Token management**: Usage tracking and optimization features

### Utilities and Helpers
- **AI Client wrapper**: Centralized Azure OpenAI client management
- **Prompt templates**: Reusable system prompts for different use cases
- **CSS styling**: Custom dark mode implementation
- **Error handling**: Comprehensive error management across components

## Data Flow

1. **Application startup**: Streamlit loads and initializes AI client
2. **Backend initialization**: FastAPI starts automatically via threading
3. **Database setup**: SQLAlchemy creates tables if they don't exist
4. **User interaction**: Frontend communicates with backend via REST API
5. **AI processing**: Direct calls to Azure OpenAI with response handling
6. **Data persistence**: Events stored in local SQLite database

## External Dependencies

### AI Services
- **Azure OpenAI**: Primary AI service for chat completions
- **tiktoken**: Token counting and optimization
- **OpenAI Python SDK**: Official client library

### Web Framework
- **Streamlit**: Main web application framework
- **FastAPI**: Backend API framework
- **Uvicorn**: ASGI server for FastAPI

### Database and ORM
- **SQLAlchemy**: Database ORM and abstraction
- **SQLite**: Embedded database engine
- **Pydantic**: Data validation and serialization

### Additional Libraries
- **pandas**: Data manipulation for event display
- **requests**: HTTP client for backend communication
- **python-multipart**: File upload support

## Deployment Strategy

### Development Environment
- **Replit configuration**: Optimized for Replit deployment
- **Port configuration**: Streamlit on 5000, FastAPI on 8000
- **Auto-scaling deployment**: Configured for automatic scaling
- **Environment variables**: Azure OpenAI credentials via environment

### Production Considerations
- **Database migration**: Would require PostgreSQL for production
- **Authentication layer**: User management system needed
- **HTTPS configuration**: SSL/TLS termination required
- **Resource optimization**: Token usage monitoring and rate limiting

## Recent Changes

### June 18, 2025 - Azure OpenAI o3-mini Integration and Bug Fixes
- **API Parameter Updates**: Modified all AI completion calls to use `max_completion_tokens` instead of `max_tokens` for o3-mini model compatibility
- **Temperature Parameter Removal**: Removed temperature parameters as they are not supported by o3-mini model
- **Retry Mechanism Implementation**: Added robust 3-attempt retry system with exponential backoff (1s, 2s, 4s) for all Azure OpenAI API calls to handle empty responses
- **Token Limit Optimization**: Significantly increased token limits across all challenges:
  - Challenge 1: Feature prioritization (1200 tokens), Roadmap creation (1000 tokens), User stories (1100 tokens)
  - Challenge 2: Expert analysis (800 tokens), Conservative parameter (300 tokens), Extended parameter (700 tokens)
  - Challenge 3: Prompt comparison responses (800 tokens each)
  - Challenge 4: RAG responses (1000 tokens)
- **Product Context Integration**: Enhanced Challenge 1 workflow where selected product concept persists across all tasks (prioritization, roadmap, user stories)
- **PDF Processing Enhancement**: Added PyPDF2 integration for proper PDF document processing in Challenge 4 RAG implementation
- **Parameter Tuning Fixes**: Enhanced Challenge 2 parameter experiment with better error handling and response validation
- **Database Corruption Fix**: Resolved SQLite database corruption issue by recreating the database file
- **Form Validation Improvement**: Enhanced event management form validation to handle null values properly
- **Dark Mode Enhancement**: Improved sidebar text visibility in dark mode with comprehensive CSS styling
- **Technical Documentation**: Added detailed technical explanations in sidebar expandable sections for both event management architecture and AI challenges learning outcomes

### Technical Improvements Made:
- **Event Management**: Fixed CRUD operations, enhanced form validation, improved error handling
- **AI Challenges**: Resolved API compatibility issues, improved response handling, enhanced user experience
- **UI/UX**: Better dark mode support, clearer technical documentation, improved text visibility
- **Document Processing**: Enhanced RAG functionality with multi-format support (PDF, TXT, MD)
- **Documentation**: Comprehensive README section with local setup instructions, troubleshooting guide, and learning objectives

## Changelog
- June 18, 2025. Initial setup and comprehensive feature implementation

## User Preferences

Preferred communication style: Simple, everyday language.
Technical detail level: Comprehensive technical explanations with architecture details.