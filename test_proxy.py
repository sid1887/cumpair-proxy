#!/usr/bin/env python3
"""
Test script for Cumpair Proxy Server
Tests both HTTP and HTTPS connectivity
"""

import requests
import sys
import os
from datetime import datetime
from urllib.parse import quote

# Proxy configuration
# Read from environment variables (matching Render's setup) or use defaults
PROXY_USER = os.getenv('PROXY_USER', 'sidraj')
PROXY_PASS = os.getenv('PROXY_PASS', 'sidraj1887')
PROXY_HOST = "cumpair-proxy.onrender.com"
PROXY_PORT = "8080"

# URL-encode the password to handle special characters like @
PROXY_PASS_ENCODED = quote(PROXY_PASS)

PROXY_URL = f"http://{PROXY_USER}:{PROXY_PASS_ENCODED}@{PROXY_HOST}:{PROXY_PORT}"

proxies = {
    'http': PROXY_URL,
    'https': PROXY_URL
}

def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def test_http():
    """Test HTTP connection through proxy"""
    print_header("Testing HTTP Connection")
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=30)
        response.raise_for_status()
        print(f"✅ HTTP Test PASSED")
        print(f"Response: {response.text}")
        return True
    except Exception as e:
        print(f"❌ HTTP Test FAILED: {str(e)}")
        return False

def test_https():
    """Test HTTPS connection through proxy"""
    print_header("Testing HTTPS Connection")
    try:
        response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=30)
        response.raise_for_status()
        print(f"✅ HTTPS Test PASSED")
        print(f"Response: {response.text}")
        return True
    except Exception as e:
        print(f"❌ HTTPS Test FAILED: {str(e)}")
        return False

def test_google():
    """Test connection to Google (HTTPS)"""
    print_header("Testing Google (HTTPS)")
    try:
        response = requests.get('https://www.google.com', proxies=proxies, timeout=30)
        response.raise_for_status()
        print(f"✅ Google Test PASSED")
        print(f"Status Code: {response.status_code}")
        print(f"Response Length: {len(response.text)} bytes")
        return True
    except Exception as e:
        print(f"❌ Google Test FAILED: {str(e)}")
        return False

def test_api_ipify():
    """Test API endpoint (HTTPS)"""
    print_header("Testing API Endpoint (ipify)")
    try:
        response = requests.get('https://api.ipify.org?format=json', proxies=proxies, timeout=30)
        response.raise_for_status()
        print(f"✅ API Test PASSED")
        print(f"Response: {response.text}")
        return True
    except Exception as e:
        print(f"❌ API Test FAILED: {str(e)}")
        return False

def main():
    """Run all tests"""
    print(f"\n🚀 Cumpair Proxy Server Test Suite")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Proxy: http://{PROXY_USER}:****@{PROXY_HOST}:{PROXY_PORT}")
    print(f"Using credentials from: {'Environment Variables' if os.getenv('PROXY_USER') else 'Defaults'}")
    
    results = []
    
    # Run all tests
    results.append(("HTTP", test_http()))
    results.append(("HTTPS", test_https()))
    results.append(("Google", test_google()))
    results.append(("API", test_api_ipify()))
    
    # Summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    print(f"\n{'='*60}")
    print(f"Total: {passed}/{total} tests passed")
    print(f"{'='*60}\n")
    
    # Exit code
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()
