# Smart Interview Prep Tool

# 🎯 Smart Interview Prep Tool

A comprehensive web application designed to help job seekers excel in their interview preparation with AI-powered features, real-time Gmail integration, and detailed analytics.

## ✨ Features

### 🤖 **AI-Powered Mock Interviews**
- Interactive interview simulations with real-time feedback
- Multiple interview types: Technical, Behavioral, System Design
- Difficulty levels from beginner to advanced
- Personalized scoring and improvement suggestions

### 📧 **Gmail Integration**
- Real-time email scanning for job applications and interview invites
- Automatic extraction of company names, interview dates, and times
- Smart email classification (applications, rejections, offers, interviews)

### 📊 **Advanced Analytics Dashboard**
- Application success rate tracking
- Interview performance metrics
- Company-wise application statistics
- Monthly application trends with visual charts

### 📚 **Comprehensive Resources**
- Industry-specific question banks
- Company-specific interview guides
- Performance tracking over time
- Preparation checklists and study materials

### 🔧 **Additional Tools**
- Professional networking guidance
- Resume analysis capabilities
- Interview scheduling integration
- Progress tracking and goal setting

## 🚀 **Live Demo**
**[Try the live application](https://web-production-d3f66.up.railway.app)**

## 🛠️ **Tech Stack**
- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy
- **APIs**: Gmail API, Google OAuth 2.0
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Deployment**: Railway Platform
- **AI Integration**: OpenAI GPT (optional)

## 🎯 **Use Cases**
- **Job Seekers**: Practice interviews and track application progress
- **Students**: Prepare for internship and graduate job interviews
- **Career Coaches**: Tool for helping clients improve interview skills
- **Recruiters**: Understanding candidate preparation needs

## 📈 **Key Benefits**
- **Data-Driven Insights**: Track your application success patterns
- **Real-Time Updates**: Automatic sync with your actual job search emails
- **Personalized Practice**: AI-powered mock interviews tailored to your needs
- **Progress Monitoring**: Visual analytics to measure improvement over time

## 🔐 **Privacy & Security**
- Local SQLite database (your data stays private)
- Secure OAuth 2.0 Gmail integration
- No personal data stored on external servers
- Optional AI features (can work offline)

---

*Built with ❤️ to help job seekers succeed in their interview journey*

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
