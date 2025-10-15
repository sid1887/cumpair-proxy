#!/bin/bash

echo "🚀 Quick Proxy Test Script"
echo "=========================="
echo ""

# Test 1: HTTP on 443
echo "Test 1: HTTP proxy on port 443"
curl -s -o /dev/null -w "Status: %{http_code}\n" -x http://cumpair-proxy.onrender.com:443 http://httpbin.org/ip
echo ""

# Test 2: HTTPS on 443
echo "Test 2: HTTPS proxy on port 443"
curl -s -o /dev/null -w "Status: %{http_code}\n" -x http://cumpair-proxy.onrender.com:443 https://httpbin.org/ip
echo ""

# Test 3: Check if service is reachable
echo "Test 3: Checking if service is reachable"
nc -zv cumpair-proxy.onrender.com 443 2>&1 | grep -q succeeded && echo "✅ Port 443 is open" || echo "❌ Port 443 is closed"
echo ""

echo "Done! Run 'python auto_test.py' for detailed results."
