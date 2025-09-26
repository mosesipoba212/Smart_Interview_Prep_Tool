# 🚀 How to Deploy Your Smart Interview Prep Tool

## 📋 Prerequisites
1. ✅ Git installed and configured
2. ✅ Your code pushed to GitHub repository
3. ✅ Heroku account created (free)

## 🎯 Deployment Steps

### Option 1: Heroku (Recommended)

#### Step 1: Install Heroku CLI
Download from: https://devcenter.heroku.com/articles/heroku-cli

#### Step 2: Login to Heroku
```bash
heroku login
```

#### Step 3: Create Heroku App
```bash
heroku create your-interview-prep-tool
```
Replace `your-interview-prep-tool` with your preferred name.

#### Step 4: Set Environment Variables
```bash
heroku config:set SECRET_KEY="your-secret-key-here"
# Optional: Add Gemini API key if you have one
heroku config:set GEMINI_API_KEY="your-gemini-key"
```

#### Step 5: Deploy
```bash
git add .
git commit -m "Deploy to production"
git push heroku main
```

#### Step 6: Open Your App
```bash
heroku open
```

### Option 2: Railway (Alternative)

1. Go to https://railway.app
2. Connect your GitHub account
3. Import your repository
4. Railway auto-detects and deploys
5. Your app is live!

### Option 3: Render (Alternative)

1. Go to https://render.com
2. Connect GitHub repository
3. Choose "Web Service"
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`
5. Deploy!

## 🔐 Important Notes

### What Works Immediately:
✅ Mock interviews
✅ Question banks
✅ Analytics dashboard (with manual data)
✅ Performance tracking
✅ All static features

### What Needs Setup:
❓ Gmail sync (requires OAuth configuration)
❓ Real-time email processing

### For Gmail OAuth in Production:
1. Update Google Console with production URL
2. Add production domain to authorized origins
3. Upload credentials securely as environment variables

## 💰 Pricing
- **Heroku**: Free tier (sleeps after 30min inactivity)
- **Railway**: $5/month for hobby projects
- **Render**: Free tier available

## 🎉 Your App Will Be Live At:
`https://your-app-name.herokuapp.com`

## 🛠️ Quick Deploy (Windows)
Run: `.\deploy_heroku.ps1`

## 🛠️ Quick Deploy (Mac/Linux)  
Run: `bash deploy_heroku.sh`