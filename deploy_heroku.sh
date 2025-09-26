#!/bin/bash
# Deploy to Heroku script

echo "🚀 Deploying Smart Interview Prep Tool to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install from https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Login to Heroku (if not already)
echo "🔑 Please login to Heroku if prompted..."
heroku auth:whoami || heroku login

# Create Heroku app (replace 'your-interview-prep-tool' with your preferred name)
echo "📱 Creating Heroku app..."
read -p "Enter your app name (or press enter for auto-generated): " APP_NAME

if [ -z "$APP_NAME" ]; then
    heroku create
else
    heroku create $APP_NAME
fi

# Set environment variables
echo "🔐 Setting environment variables..."
heroku config:set SECRET_KEY="smart-interview-prep-production-$(date +%s)"

# Optional: Set Gemini API key if you have one
read -p "Enter GEMINI_API_KEY (optional, press enter to skip): " GEMINI_KEY
if [ ! -z "$GEMINI_KEY" ]; then
    heroku config:set GEMINI_API_KEY="$GEMINI_KEY"
fi

# Deploy to Heroku
echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Deploy to Heroku - Smart Interview Prep Tool"
git push heroku main

# Open the app
echo "✅ Deployment complete!"
heroku open

echo "🎉 Your Smart Interview Prep Tool is now live!"
echo "📊 Note: Gmail sync will need OAuth configuration for production use"