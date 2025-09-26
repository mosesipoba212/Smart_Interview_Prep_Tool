# Smart Interview Prep Tool - Deployment Guide

## 🚀 Deployment Options

### Option 1: Heroku (Recommended)
1. Create account at https://heroku.com
2. Install Heroku CLI
3. Deploy with our prepared files

### Option 2: Railway  
1. Connect GitHub repo at https://railway.app
2. Auto-deploys from GitHub

### Option 3: Render
1. Connect repo at https://render.com
2. Configure build settings

## 📁 Files Ready for Deployment
- ✅ requirements.txt (all dependencies)
- ✅ Procfile (Heroku config)
- ✅ wsgi.py (production server)
- ✅ app.py (main application)

## 🔑 Environment Variables Needed
- GEMINI_API_KEY (optional, for AI features)
- SECRET_KEY (Flask security)
- Gmail credentials (for email sync)

## 🛠️ Deployment Commands

### For Heroku:
```bash
heroku create your-interview-prep-tool
git push heroku main
heroku open
```

### For Railway/Render:
- Just connect your GitHub repo
- Platform auto-detects Python app
- Deploys automatically

## 📊 What Works After Deployment
✅ Mock interviews
✅ Question banks  
✅ Analytics dashboard
✅ Performance tracking
❓ Gmail sync (requires OAuth setup in production)

## 🔐 Gmail OAuth in Production
- Need to configure OAuth for production domain
- Add production URL to Google Console
- Upload credentials securely

## 📝 Notes
- Free tiers have limitations (sleep after inactivity)
- For heavy usage, consider paid plans
- Database will reset on free tiers (use PostgreSQL addon for persistence)