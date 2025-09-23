# Smart Interview Prep Tool

A comprehensive interview preparation application with Gmail integration, AI-powered question generation, Google Calendar scheduling, and performance tracking.

## Features

- 🔍 **Auto Email Parsing**: Automatically detects and parses recruiter emails
- 🤖 **AI Question Generation**: Creates tailored question sets based on interview type
- 📅 **Calendar Integration**: Auto-schedules prep blocks in Google Calendar
- 📊 **Performance Tracking**: Tracks performance across multiple interviews
- 🎯 **Interview Type Detection**: Automatically identifies interview types (technical, behavioral, etc.)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

1. Set up Gmail API credentials
2. Configure Google Calendar API
3. Add AI service API keys
4. Run the application

## Usage

```bash
python main.py
```

## Project Structure

```
├── src/
│   ├── email_parser/       # Gmail integration and email parsing
│   ├── ai_engine/          # AI question generation
│   ├── calendar_integration/ # Google Calendar API
│   ├── performance_tracker/ # Performance analytics
│   └── interview_detector/  # Interview type detection
├── config/                 # Configuration files
├── tests/                  # Unit tests
└── data/                   # Data storage
```

## API Keys Required

- Gmail API credentials
- Google Calendar API credentials
- OpenAI API key (or alternative AI service)

## License

MIT License
