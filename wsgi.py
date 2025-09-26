#!/usr/bin/env python3
"""
Production WSGI entry point for cloud deployment
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from app import app

# Configure for production
app.config['DEBUG'] = False
app.config['ENV'] = 'production'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
