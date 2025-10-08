#!/usr/bin/env python3
"""
🛡️ Smart Interview Prep Tool - ULTIMATE GUARDIAN
Python-based auto-restart daemon that monitors and restarts the server
"""

import os
import sys
import time
import signal
import logging
import subprocess
import threading
from datetime import datetime
import psutil

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - GUARDIAN - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('smart_interview_guardian.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SmartInterviewGuardian:
    """Ultimate guardian that keeps the Smart Interview Prep Tool alive FOREVER"""
    
    def __init__(self):
        self.process = None
        self.running = True
        self.restart_count = 0
        self.start_time = datetime.now()
        self.max_restarts_per_hour = 10
        self.restart_times = []
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        logger.info("🛡️ Smart Interview Guardian initialized")
        logger.info("🎯 Mission: Keep Smart Interview Prep Tool alive FOREVER")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"🛑 Received signal {signum}. Shutting down gracefully...")
        self.running = False
        if self.process:
            self.stop_server()
    
    def start_server(self):
        """Start the production server"""
        try:
            logger.info("🚀 Starting Smart Interview Prep Tool production server...")
            
            # Start the server process
            self.process = subprocess.Popen(
                [sys.executable, 'run_production.py'],
                cwd=os.path.dirname(__file__),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            logger.info(f"✅ Server started with PID: {self.process.pid}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start server: {e}")
            return False
    
    def stop_server(self):
        """Stop the server gracefully"""
        if self.process:
            try:
                logger.info("🛑 Stopping server gracefully...")
                
                # Try graceful shutdown first
                self.process.terminate()
                
                # Wait up to 10 seconds for graceful shutdown
                try:
                    self.process.wait(timeout=10)
                    logger.info("✅ Server stopped gracefully")
                except subprocess.TimeoutExpired:
                    # Force kill if graceful shutdown fails
                    logger.warning("⚠️ Graceful shutdown failed, forcing termination...")
                    self.process.kill()
                    self.process.wait()
                    logger.info("✅ Server terminated forcefully")
                
                self.process = None
                
            except Exception as e:
                logger.error(f"❌ Error stopping server: {e}")
    
    def is_server_healthy(self):
        """Check if the server is running and healthy"""
        if not self.process:
            return False
        
        # Check if process is still running
        if self.process.poll() is not None:
            return False
        
        # Additional health checks could go here
        # (e.g., HTTP health check, memory usage, etc.)
        
        return True
    
    def should_restart(self):
        """Check if we should restart (rate limiting)"""
        now = datetime.now()
        
        # Remove restart times older than 1 hour
        self.restart_times = [
            t for t in self.restart_times 
            if (now - t).seconds < 3600
        ]
        
        # Check if we've exceeded restart limit
        if len(self.restart_times) >= self.max_restarts_per_hour:
            logger.error(f"🚨 Too many restarts ({len(self.restart_times)}) in the last hour!")
            logger.error("🛑 Stopping guardian to prevent restart loop")
            return False
        
        return True
    
    def record_restart(self):
        """Record a restart attempt"""
        self.restart_times.append(datetime.now())
        self.restart_count += 1
    
    def monitor_server(self):
        """Monitor server output and log it"""
        if not self.process:
            return
        
        try:
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    # Log server output (remove our own log prefix to avoid duplication)
                    clean_line = line.strip()
                    if clean_line and not clean_line.startswith('202'):  # Skip timestamp lines
                        logger.info(f"SERVER: {clean_line}")
                
                if not self.running:
                    break
                    
        except Exception as e:
            logger.error(f"❌ Error monitoring server output: {e}")
    
    def run_forever(self):
        """Main guardian loop - keeps server alive FOREVER"""
        logger.info("🛡️ Guardian starting eternal watch...")
        logger.info("🌟 Smart Interview Prep Tool will run FOREVER!")
        logger.info("🔄 Auto-restart enabled with rate limiting")
        logger.info("📊 Max restarts per hour: 10")
        logger.info("")
        
        while self.running:
            try:
                # Start server if not running
                if not self.is_server_healthy():
                    if self.process:
                        logger.warning("⚠️ Server died! Preparing to restart...")
                        self.stop_server()
                    
                    # Check restart rate limiting
                    if not self.should_restart():
                        logger.error("🛑 Restart rate limit exceeded. Stopping guardian.")
                        break
                    
                    # Record restart attempt
                    self.record_restart()
                    
                    logger.info(f"🔄 Restart attempt #{self.restart_count}")
                    
                    # Wait a bit before restarting
                    time.sleep(5)
                    
                    # Start the server
                    if self.start_server():
                        # Start monitoring in a separate thread
                        monitor_thread = threading.Thread(
                            target=self.monitor_server,
                            daemon=True
                        )
                        monitor_thread.start()
                        
                        logger.info("✅ Server restarted successfully")
                    else:
                        logger.error("❌ Failed to restart server")
                        time.sleep(30)  # Wait longer on failure
                
                # Sleep for a bit before next check
                time.sleep(5)
                
            except Exception as e:
                logger.error(f"❌ Guardian error: {e}")
                time.sleep(10)
        
        # Cleanup
        logger.info("🛑 Guardian shutting down...")
        self.stop_server()
        
        uptime = datetime.now() - self.start_time
        logger.info(f"📊 Guardian uptime: {uptime}")
        logger.info(f"🔄 Total restarts: {self.restart_count}")
        logger.info("👋 Guardian stopped")

def main():
    """Main entry point"""
    print("🛡️ Smart Interview Prep Tool - ULTIMATE GUARDIAN")
    print("🎯 Keeping your app alive FOREVER!")
    print("🚀 Starting guardian daemon...")
    print("")
    
    try:
        guardian = SmartInterviewGuardian()
        guardian.run_forever()
    except KeyboardInterrupt:
        print("\n👋 Guardian stopped by user")
    except Exception as e:
        print(f"❌ Guardian fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()