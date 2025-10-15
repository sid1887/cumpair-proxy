#!/usr/bin/env python3
"""
Wait for deployment and auto-test
"""

import subprocess
import time
import sys

def check_service():
    """Quick check if service is responding"""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(("cumpair-proxy.onrender.com", 443))
        sock.close()
        return result == 0
    except:
        return False

def main():
    print("⏳ Waiting for deployment to be ready...")
    print("   This will check every 10 seconds for up to 5 minutes\n")
    
    max_attempts = 30  # 5 minutes
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        print(f"[Attempt {attempt}/{max_attempts}] Checking service...", end=" ")
        
        if check_service():
            print("✅ Service is responding!")
            print("\n" + "="*50)
            print("Starting automated tests...\n")
            time.sleep(2)
            
            # Run auto_test.py
            result = subprocess.run([sys.executable, "auto_test.py"])
            return result.returncode
        else:
            print("⏳ Not ready yet")
            time.sleep(10)
    
    print("\n❌ Service did not respond after 5 minutes")
    print("   Please check Render deployment logs")
    return 1

if __name__ == "__main__":
    sys.exit(main())
