#!/usr/bin/env python3
"""
Automated Proxy Test Suite
Tests multiple configurations to find the working one
"""

import requests
import sys
import time
from datetime import datetime

PROXY_HOST = "cumpair-proxy.onrender.com"

# Different configurations to test
TEST_CONFIGS = [
    {"scheme": "http", "port": "443", "name": "HTTP proxy on 443 (Render default)"},
    {"scheme": "https", "port": "443", "name": "HTTPS proxy on 443 (TLS terminated)"},
    {"scheme": "http", "port": "8080", "name": "HTTP proxy on 8080 (direct)"},
    {"scheme": "http", "port": "80", "name": "HTTP proxy on 80"},
]

def test_config(config):
    """Test a specific proxy configuration"""
    scheme = config["scheme"]
    port = config["port"]
    name = config["name"]
    
    proxy_url = f"{scheme}://{PROXY_HOST}:{port}"
    proxies = {'http': proxy_url, 'https': proxy_url}
    
    print(f"\n{'='*70}")
    print(f"🔍 Testing: {name}")
    print(f"   Proxy URL: {proxy_url}")
    print(f"{'='*70}")
    
    results = {
        'config': name,
        'proxy_url': proxy_url,
        'http_works': False,
        'https_works': False,
        'errors': []
    }
    
    # Test HTTP
    try:
        print("  [1/2] Testing HTTP request...", end=" ")
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10)
        response.raise_for_status()
        results['http_works'] = True
        print("✅ PASS")
    except Exception as e:
        error_msg = str(e)[:100]
        results['errors'].append(f"HTTP: {error_msg}")
        print(f"❌ FAIL ({type(e).__name__})")
    
    # Test HTTPS
    try:
        print("  [2/2] Testing HTTPS request...", end=" ")
        response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
        response.raise_for_status()
        results['https_works'] = True
        print("✅ PASS")
    except Exception as e:
        error_msg = str(e)[:100]
        results['errors'].append(f"HTTPS: {error_msg}")
        print(f"❌ FAIL ({type(e).__name__})")
    
    return results

def main():
    print(f"\n{'#'*70}")
    print(f"# 🤖 AUTOMATED PROXY CONFIGURATION TEST SUITE")
    print(f"# Testing {len(TEST_CONFIGS)} different configurations")
    print(f"# Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*70}")
    
    all_results = []
    
    for i, config in enumerate(TEST_CONFIGS, 1):
        print(f"\n[Test {i}/{len(TEST_CONFIGS)}]")
        results = test_config(config)
        all_results.append(results)
        time.sleep(1)  # Brief pause between tests
    
    # Summary Report
    print(f"\n\n{'='*70}")
    print(f"📊 FINAL RESULTS SUMMARY")
    print(f"{'='*70}\n")
    
    working_configs = []
    
    for i, result in enumerate(all_results, 1):
        status = ""
        if result['http_works'] and result['https_works']:
            status = "✅ BOTH WORK"
            working_configs.append(result)
        elif result['http_works']:
            status = "⚠️  HTTP ONLY"
        elif result['https_works']:
            status = "⚠️  HTTPS ONLY"
        else:
            status = "❌ BOTH FAIL"
        
        print(f"{i}. {status:15} - {result['config']}")
        print(f"   URL: {result['proxy_url']}")
        if result['errors']:
            for error in result['errors'][:1]:  # Show first error only
                print(f"   Error: {error[:80]}...")
        print()
    
    # Recommendations
    print(f"{'='*70}")
    print(f"💡 RECOMMENDATIONS")
    print(f"{'='*70}\n")
    
    if working_configs:
        print(f"✅ Found {len(working_configs)} working configuration(s)!\n")
        best = working_configs[0]
        print(f"🎯 BEST CONFIG TO USE:")
        print(f"   {best['config']}")
        print(f"   Proxy URL: {best['proxy_url']}")
        print(f"\n📝 Update your test_proxy.py with:")
        print(f'   PROXY_SCHEME = "{best["proxy_url"].split("://")[0]}"')
        print(f'   PROXY_PORT = "{best["proxy_url"].split(":")[-1]}"')
    else:
        print("❌ No working configurations found.")
        print("\n🔧 Troubleshooting steps:")
        print("   1. Check if your Render deployment is running")
        print("   2. Check Render logs for errors")
        print("   3. Verify the service URL is correct")
        print("   4. Wait 2-3 minutes after deployment before testing")
    
    print(f"\n{'='*70}\n")
    
    return 0 if working_configs else 1

if __name__ == "__main__":
    sys.exit(main())
