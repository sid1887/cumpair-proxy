# 🚀 Cumpair Proxy Server

Production-ready Tinyproxy server deployed on Render with full HTTP/HTTPS support.

## 📡 Live Endpoint

**Proxy URL:** `http://cumpair-proxy.onrender.com:8080`

**Credentials:**
- Username: `sidraj`
- Password: `sidraj@1887`

## ✨ Features

- ✅ **HTTP & HTTPS Support** - Full tunneling via CONNECT method
- ✅ **Authentication** - Basic Auth protection
- ✅ **High Performance** - Optimized for 200 concurrent connections
- ✅ **No Via Headers** - Avoids 400 errors on strict servers
- ✅ **Multiple HTTPS Ports** - Supports 443, 563, 873, 8443, 9443
- ✅ **Health Checks** - Built-in monitoring
- ✅ **Logging** - Comprehensive request logging

## 🧪 Testing

### Using cURL

```bash
# Test HTTP
curl -x http://sidraj:sidraj@1887@cumpair-proxy.onrender.com:8080 http://httpbin.org/ip

# Test HTTPS
curl -x http://sidraj:sidraj@1887@cumpair-proxy.onrender.com:8080 https://httpbin.org/ip

# Test with headers
curl -x http://sidraj:sidraj@1887@cumpair-proxy.onrender.com:8080 -I https://www.google.com
```

### Using Python

```python
import requests

proxies = {
    'http': 'http://sidraj:sidraj@1887@cumpair-proxy.onrender.com:8080',
    'https': 'http://sidraj:sidraj@1887@cumpair-proxy.onrender.com:8080'
}

# Test HTTP
response = requests.get('http://httpbin.org/ip', proxies=proxies)
print(f"HTTP: {response.text}")

# Test HTTPS
response = requests.get('https://httpbin.org/ip', proxies=proxies)
print(f"HTTPS: {response.text}")
```

### Using Node.js

```javascript
const axios = require('axios');
const HttpsProxyAgent = require('https-proxy-agent');

const proxy = 'http://sidraj:sidraj@1887@cumpair-proxy.onrender.com:8080';
const agent = new HttpsProxyAgent(proxy);

axios.get('https://httpbin.org/ip', { httpsAgent: agent })
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

## 🚀 Local Testing

```bash
# Build the Docker image
docker build -t cumpair-proxy --build-arg PROXY_USER=sidraj --build-arg PROXY_PASS=sidraj@1887 .

# Run locally
docker run -p 8080:8080 cumpair-proxy

# Test locally
curl -x http://sidraj:sidraj@1887@localhost:8080 https://api.ipify.org
```

## 🔧 Configuration Details

- **Max Connections:** 200 concurrent clients
- **Timeout:** 10 minutes per connection
- **Supported Ports:** 443, 563, 873, 8443, 9443
- **Log Level:** Info
- **Via Header:** Disabled (for better compatibility)

## 📊 Monitoring

Check logs on Render dashboard for:
- Connection attempts
- Authentication failures
- CONNECT requests
- Error messages

## ⚠️ Important Notes

- This proxy is for **personal/development use only**
- Render free tier may have limitations
- Keep credentials secure
- Monitor usage to avoid abuse
