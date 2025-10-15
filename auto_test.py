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
    {"scheme": "http", "port": "8080", "name": "HTTP proxy on 8080 (direct internal)"},
    {"scheme": "http", "port": None, "name": "HTTP proxy (default port)"},
    {"scheme": "https", "port": None, "name": "HTTPS proxy (default port)"},
    {"scheme": "http", "port": "443", "name": "HTTP proxy on 443 (Render default)"},
    {"scheme": "https", "port": "443", "name": "HTTPS proxy on 443 (TLS terminated)"},
    {"scheme": "http", "port": "80", "name": "HTTP proxy on 80"},
]

def test_config(config):
    """Test a specific proxy configuration"""
    scheme = config["scheme"]
    port = config["port"]
    name = config["name"]
    
    if port:
        proxy_url = f"{scheme}://{PROXY_HOST}:{port}"
    else:
        proxy_url = f"{scheme}://{PROXY_HOST}"
    
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
        'errors': [],
        'http_status': None,
        'https_status': None
    }
    
    # Test HTTP
    try:
        print("  [1/2] Testing HTTP request...", end=" ")
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
        results['http_status'] = response.status_code
        response.raise_for_status()
        results['http_works'] = True
        print(f"✅ PASS (Status: {response.status_code})")
    except requests.exceptions.SSLError as e:
        results['errors'].append(f"HTTP SSL: {str(e)[:80]}")
        print(f"❌ FAIL (SSLError - try different scheme)")
    except requests.exceptions.HTTPError as e:
        results['http_status'] = e.response.status_code if hasattr(e, 'response') else None
        results['errors'].append(f"HTTP {results['http_status']}: {str(e)[:80]}")
        print(f"❌ FAIL (HTTP {results['http_status']})")
    except Exception as e:
        error_msg = str(e)[:80]
        results['errors'].append(f"HTTP: {error_msg}")
        print(f"❌ FAIL ({type(e).__name__})")
    
    # Test HTTPS
    try:
        print("  [2/2] Testing HTTPS request...", end=" ")
        response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
        results['https_status'] = response.status_code
        response.raise_for_status()
        results['https_works'] = True
        print(f"✅ PASS (Status: {response.status_code})")
    except requests.exceptions.SSLError as e:
        results['errors'].append(f"HTTPS SSL: {str(e)[:80]}")
        print(f"❌ FAIL (SSLError - try different scheme)")
    except requests.exceptions.HTTPError as e:
        results['https_status'] = e.response.status_code if hasattr(e, 'response') else None
        results['errors'].append(f"HTTPS {results['https_status']}: {str(e)[:80]}")
        print(f"❌ FAIL (HTTP {results['https_status']})")
    except Exception as e:
        error_msg = str(e)[:80]
        results['errors'].append(f"HTTPS: {error_msg}")
        print(f"❌ FAIL ({type(e).__name__})")
    
    return results

def main():
    print(f"\n{'#'*70}")
    print(f"# 🤖 AUTOMATED PROXY CONFIGURATION TEST SUITE")
    print(f"# Testing {len(TEST_CONFIGS)} different configurations")
    print(f"# Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*70}")
    
    # Disable SSL warnings for testing
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
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
            working_configs.append(result)
        elif result['https_works']:
            status = "⚠️  HTTPS ONLY"
            working_configs.append(result)
        else:
            status = "❌ BOTH FAIL"
        
        print(f"{i}. {status:15} - {result['config']}")
        print(f"   URL: {result['proxy_url']}")
        if result['http_status']:
            print(f"   HTTP Status: {result['http_status']}")
        if result['https_status']:
            print(f"   HTTPS Status: {result['https_status']}")
        if result['errors']:
            for error in result['errors'][:2]:  # Show first 2 errors
                print(f"   Error: {error}")
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
        
        # Extract scheme and port
        scheme = best['proxy_url'].split('://')[0]
        if ':' in best['proxy_url'].split('://')[1]:
            port = best['proxy_url'].split(':')[-1]
        else:
            port = "443" if scheme == "https" else "80"
        
        print(f"\n📝 Update your test_proxy.py with:")
        print(f'   PROXY_SCHEME = "{scheme}"')
        print(f'   PROXY_PORT = "{port}"')
        
        print(f"\n🔧 Or set environment variables:")
        print(f'   export PROXY_SCHEME="{scheme}"')
        print(f'   export PROXY_PORT="{port}"')
    else:
        print("❌ No working configurations found.")
        print("\n🔧 Troubleshooting steps:")
        print("   1. Check Render logs: https://dashboard.render.com")
        print("   2. Verify tinyproxy started successfully (check for 'Port 10000')")
        print("   3. Common errors:")
        print("      - 400 Bad Request: Proxy config issue or wrong scheme")
        print("      - 403 Forbidden: Access control issue")
        print("      - Connection errors: Service not running or wrong port")
        print("\n   4. Try manual curl test:")
        print(f"      curl -v -x http://{PROXY_HOST} http://httpbin.org/ip")
    
    print(f"\n{'='*70}\n")
    
    return 0 if working_configs else 1

if __name__ == "__main__":
    sys.exit(main())
