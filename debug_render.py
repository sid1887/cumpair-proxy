#!/usr/bin/env python3
"""
Debug script to check Render service details
"""

import socket
import requests

PROXY_HOST = "cumpair-proxy.onrender.com"

print("🔍 Render Service Debug Info\n")
print("="*60)

# 1. DNS Resolution
print("\n1️⃣ DNS Resolution:")
try:
    ip = socket.gethostbyname(PROXY_HOST)
    print(f"   ✅ {PROXY_HOST} resolves to {ip}")
except Exception as e:
    print(f"   ❌ DNS Error: {e}")

# 2. Port checks
print("\n2️⃣ Port Connectivity:")
for port in [80, 443, 8080, 10000]:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((PROXY_HOST, port))
        sock.close()
        if result == 0:
            print(f"   ✅ Port {port:5d} is OPEN")
        else:
            print(f"   ❌ Port {port:5d} is CLOSED")
    except Exception as e:
        print(f"   ❌ Port {port:5d} error: {e}")

# 3. HTTP Direct Access
print("\n3️⃣ Direct HTTP Access:")
try:
    response = requests.get(f"http://{PROXY_HOST}", timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:100]}")
except Exception as e:
    print(f"   Error: {e}")

# 4. HTTPS Direct Access
print("\n4️⃣ Direct HTTPS Access:")
try:
    response = requests.get(f"https://{PROXY_HOST}", timeout=5, verify=False)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:100]}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "="*60 + "\n")
