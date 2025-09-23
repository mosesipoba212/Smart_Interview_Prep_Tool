
# API Credentials Setup Instructions

## Gmail API Setup
1. Go to Google Cloud Console (https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create credentials (OAuth 2.0 Client ID)
5. Download credentials.json and place in project root

## Google Calendar API Setup  
1. In the same Google Cloud project
2. Enable Google Calendar API
3. Use the same OAuth credentials or create new ones
4. Download calendar_credentials.json and place in project root

## OpenAI API Setup
1. Sign up at https://platform.openai.com/
2. Generate an API key
3. Add the key to your .env file

## Required Files:
- credentials.json (Gmail API)
- calendar_credentials.json (Calendar API)  
- .env (API keys and configuration)

## File Structure:
```
Smart_Interview_Prep_Tool/
├── credentials.json          # Gmail API credentials
├── calendar_credentials.json # Calendar API credentials
├── .env                     # Environment variables
├── main.py                  # Main application
└── ...
```
