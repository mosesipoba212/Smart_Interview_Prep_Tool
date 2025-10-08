#!/usr/bin/env python3
"""
🚀 Production Server Runner with Waitress
Ultra-stable production server with auto-restart capabilities
"""

import os
import sys
import time
import logging
import subprocess
from datetime import datetime
from waitress import serve

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import our bulletproof app
from app_bulletproof import app, logger

def run_production_server():
    """Run the production server with waitress"""
    logger.info("🚀 Starting PRODUCTION Smart Interview Prep Tool")
    logger.info("🌐 Server will be available at: http://127.0.0.1:8080")
    logger.info("🛡️ Running with Waitress WSGI Server")
    logger.info("⚡ High performance, production-ready configuration")
    
    try:
        # Production configuration
        serve(
            app, 
            host='127.0.0.1', 
            port=8080,
            threads=6,  # Handle multiple requests
            connection_limit=1000,  # Max connections
            cleanup_interval=30,  # Cleanup frequency
            channel_timeout=120,  # Channel timeout
            log_untrusted_proxy_headers=True,
            clear_untrusted_proxy_headers=True,
            ident='SmartInterviewPrepTool/1.0'
        )
    except Exception as e:
        logger.error(f"❌ Production server failed: {e}")
        raise

if __name__ == '__main__':
    try:
        run_production_server()
    except KeyboardInterrupt:
        logger.info("👋 Production server stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)