# Habit Tracker Application

## Overview

This is a Flask-based habit tracking web application that allows users to create and manage daily or weekly habits with associated tasks. The application features a clean, responsive interface built with Bootstrap 5 and uses JSON file storage for data persistence. Users can track their progress through a visual calendar system and manage tasks of different sizes (small, medium, big) within each habit.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask for server-side rendering
- **UI Framework**: Bootstrap 5 for responsive design and component styling
- **Icons**: Feather Icons for consistent iconography
- **Styling**: Custom CSS with CSS variables for theming, Google Fonts (Inter/Poppins) for typography
- **JavaScript**: Vanilla JavaScript for client-side interactions, tooltips, and form feedback

### Backend Architecture
- **Framework**: Flask web framework with Python
- **Application Structure**: Single-file Flask application (app.py) with modular route handling
- **Data Models**: JSON-based data structure defined in models.py for reference
- **Session Management**: Flask sessions with configurable secret key from environment variables
- **Error Handling**: Comprehensive logging and exception handling for data operations

### Data Storage Solution
- **Primary Storage**: JSON file-based persistence (data/habits.json)
- **Data Structure**: Nested JSON with habits containing tasks and completion tracking
- **File Operations**: Atomic read/write operations with directory creation and error recovery
- **ID Generation**: Timestamp-based unique ID generation for habits and tasks

### Key Data Models
- **Habits**: Contains id, name, frequency (daily/weekly), creation timestamp, tasks array, and completions object
- **Tasks**: Nested within habits with id, name, size classification, and creation timestamp  
- **Completions**: Date-keyed tracking of task completion status per day

### Authentication and Authorization
- **Current State**: No authentication system implemented
- **Session Security**: Basic Flask session management with configurable secret key
- **Data Access**: Open access to all functionality without user restrictions

## External Dependencies

### Frontend Dependencies
- **Bootstrap 5**: CSS framework loaded from CDN for UI components and responsive layout
- **Google Fonts**: Web fonts (Inter, Poppins) for enhanced typography
- **Feather Icons**: Icon library loaded from unpkg CDN for consistent iconography

### Backend Dependencies
- **Flask**: Core web framework for Python
- **Python Standard Library**: json, os, logging, datetime modules for core functionality

### Development Dependencies
- **Flask Debug Mode**: Enabled for development with hot reloading
- **Environment Variables**: SESSION_SECRET for session security configuration

### Infrastructure Requirements
- **File System**: Write permissions required for data directory and JSON file storage
- **Port Configuration**: Application runs on configurable port (default 5000)
- **Host Configuration**: Configured for 0.0.0.0 binding for container compatibility