# 🔐 SECURITY & PRIVACY GUIDE

## ⚠️ IMPORTANT FILES TO KEEP SECRET

This document lists all files that contain sensitive information and should **NEVER** be shared or committed to version control.

### 🚨 CRITICAL SECRET FILES

#### 1. **Environment Variables**
- `.env` - Contains all API keys and secrets
- `.env.local`, `.env.production` - Environment-specific secrets

#### 2. **API Credentials**
- `credentials.json` - Google API service account credentials
- `token.json` - OAuth tokens and refresh tokens
- Any files ending with `_credentials.json`

#### 3. **Database Files**
- `*.db` files - SQLite databases with user data
- `internship_tracker.db` - Contains personal internship information
- `interview_performance.db` - Contains interview performance history

#### 4. **Log Files**
- `*.log` - May contain API keys, user data, or error traces
- `smart_interview_prep_errors.log` - Application error logs

### 🛡️ PROTECTED BY .GITIGNORE

The following file types are automatically ignored:

```
# Sensitive files
.env*
credentials*.json
*.db
*.log

# Cache and temporary files
__pycache__/
*.pyc
*.tmp

# User data
uploads/
user_data/
exports/
```

### 🔑 API KEYS PROTECTION

The application uses these sensitive API keys:

1. **OpenAI API Key** (`OPENAI_API_KEY`)
   - Used for AI-powered interview analysis
   - Keep secret to prevent unauthorized usage charges

2. **Google Gemini API Key** (`GEMINI_API_KEY`)
   - Used for question generation
   - Has daily usage limits

3. **Google OAuth Credentials**
   - `GMAIL_CLIENT_ID` and `GMAIL_CLIENT_SECRET`
   - Used for Gmail integration
   - Required for email scanning features

4. **Google API Key** (`GOOGLE_API_KEY`)
   - Used for various Google services
   - Supports calendar and email features

### 📋 SETUP CHECKLIST

Before sharing or deploying your code:

- [ ] Verify `.env` file is not committed
- [ ] Check that `credentials.json` is not in git
- [ ] Ensure database files are ignored
- [ ] Remove any hardcoded API keys from source code
- [ ] Use environment variables for all secrets
- [ ] Test with `.env.example` file

### 🔒 BEST PRACTICES

#### For Development:
1. Copy `.env.example` to `.env`
2. Fill in your actual API keys in `.env`
3. Never edit `.env.example` with real values
4. Use different API keys for development vs production

#### For Sharing Code:
1. Only share template files (`credentials_template.json`, `.env.example`)
2. Include setup instructions in README
3. Document which API keys are needed
4. Provide links to get API keys

#### For Production:
1. Use environment variables on your hosting platform
2. Enable 2FA on all accounts
3. Regularly rotate API keys
4. Monitor API usage and set billing alerts
5. Use separate production API keys

### 🚨 IF SECRETS ARE EXPOSED

If you accidentally commit sensitive files:

1. **Immediately** rotate all exposed API keys
2. Remove the files from git history:
   ```bash
   git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch credentials.json' --prune-empty --tag-name-filter cat -- --all
   ```
3. Update `.gitignore` to prevent future exposure
4. Force push to remove from remote repository
5. Check billing/usage on all affected services

### 📞 SUPPORT

If you need help with:
- Setting up API keys → See `CREDENTIALS_SETUP.md`
- Environment configuration → See `STEP_BY_STEP_SETUP.md`
- Security concerns → Check this file or contact the maintainer

---

**Remember: Security is everyone's responsibility. When in doubt, don't commit it!** 🔐