#!/usr/bin/env python3
"""
Google Integration Setup Helper
Automated setup assistant for Gmail and Calendar integration
"""

import os
import json
import webbrowser
from pathlib import Path

def check_credentials_file():
    """Check if credentials.json exists"""
    cred_file = Path("credentials.json")
    if cred_file.exists():
        print("✅ credentials.json found!")
        return True
    else:
        print("❌ credentials.json not found!")
        return False

def validate_credentials_format():
    """Validate credentials.json format"""
    try:
        with open("credentials.json", 'r') as f:
            creds = json.load(f)
        
        if "installed" in creds:
            client_info = creds["installed"]
            required_fields = ["client_id", "client_secret", "auth_uri", "token_uri"]
            
            missing_fields = [field for field in required_fields if field not in client_info]
            
            if missing_fields:
                print(f"❌ Missing fields in credentials.json: {missing_fields}")
                return False
            else:
                print("✅ credentials.json format is valid!")
                return True
        else:
            print("❌ Invalid credentials.json format - 'installed' section not found")
            return False
            
    except json.JSONDecodeError:
        print("❌ credentials.json is not valid JSON")
        return False
    except FileNotFoundError:
        print("❌ credentials.json file not found")
        return False

def check_environment_variables():
    """Check if required environment variables are set"""
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found!")
        
        with open(".env", 'r') as f:
            env_content = f.read()
            
        for var in required_vars:
            if var not in env_content:
                missing_vars.append(var)
    else:
        print("❌ .env file not found!")
        missing_vars = required_vars
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return False
    else:
        print("✅ Environment variables configured!")
        return True

def create_gitignore():
    """Create/update .gitignore file"""
    gitignore_content = """
# Google Credentials - KEEP SECURE
credentials.json
token.json

# Environment Variables
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    
    with open(".gitignore", 'w') as f:
        f.write(gitignore_content.strip())
    
    print("✅ .gitignore created/updated!")

def open_google_cloud_console():
    """Open Google Cloud Console in browser"""
    print("🌐 Opening Google Cloud Console...")
    webbrowser.open("https://console.cloud.google.com/")

def open_gmail_api_page():
    """Open Gmail API library page"""
    print("📧 Opening Gmail API page...")
    webbrowser.open("https://console.cloud.google.com/apis/library/gmail.googleapis.com")

def open_calendar_api_page():
    """Open Calendar API library page"""
    print("📅 Opening Calendar API page...")
    webbrowser.open("https://console.cloud.google.com/apis/library/calendar-json.googleapis.com")

def create_sample_env():
    """Create sample .env file"""
    env_content = """# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Google API Configuration (Optional - credentials.json is the primary method)
GOOGLE_CLIENT_ID=your_client_id_from_credentials.json
GOOGLE_CLIENT_SECRET=your_client_secret_from_credentials.json
GOOGLE_REDIRECT_URI=http://localhost:8080/callback

# Application Configuration
DEBUG=True
FLASK_ENV=development
"""
    
    if not Path(".env").exists():
        with open(".env", 'w') as f:
            f.write(env_content)
        print("✅ Sample .env file created!")
    else:
        print("ℹ️  .env file already exists")

def main():
    """Main setup function"""
    print("🚀 Google Integration Setup Helper")
    print("=" * 50)
    
    # Check current status
    print("\n📋 Checking current setup status...")
    
    creds_exist = check_credentials_file()
    env_vars_ok = check_environment_variables()
    
    if creds_exist:
        creds_valid = validate_credentials_format()
    else:
        creds_valid = False
    
    # Setup recommendations
    print("\n🔧 Setup Recommendations:")
    
    if not creds_exist or not creds_valid:
        print("\n1. Set up Google Cloud credentials:")
        print("   a. Create Google Cloud Project")
        print("   b. Enable Gmail and Calendar APIs")
        print("   c. Create OAuth2 credentials")
        print("   d. Download credentials.json to project root")
        
        print("\n   Would you like to open the setup pages? (y/n): ", end="")
        response = input().strip().lower()
        
        if response == 'y':
            open_google_cloud_console()
            print("\n   Open Gmail API page? (y/n): ", end="")
            if input().strip().lower() == 'y':
                open_gmail_api_page()
            
            print("\n   Open Calendar API page? (y/n): ", end="")
            if input().strip().lower() == 'y':
                open_calendar_api_page()
    
    if not env_vars_ok:
        print("\n2. Configure environment variables:")
        print("   Create .env file with your OpenAI API key")
        
        print("\n   Create sample .env file? (y/n): ", end="")
        response = input().strip().lower()
        
        if response == 'y':
            create_sample_env()
    
    # Create .gitignore
    print("\n3. Security setup:")
    create_gitignore()
    
    # Final status
    print("\n" + "=" * 50)
    print("📊 Setup Status Summary:")
    print(f"   Credentials file: {'✅' if creds_exist and creds_valid else '❌'}")
    print(f"   Environment vars: {'✅' if env_vars_ok else '❌'}")
    print(f"   Security (.gitignore): ✅")
    
    if creds_exist and creds_valid and env_vars_ok:
        print("\n🎉 Setup complete! You can now run the application:")
        print("   python main.py")
    else:
        print("\n⚠️  Setup incomplete. Please follow the steps above.")
        print("📖 For detailed instructions, see: GOOGLE_SETUP_GUIDE.md")

if __name__ == "__main__":
    main()