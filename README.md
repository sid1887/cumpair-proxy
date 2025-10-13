# cumpair-proxy-railway

TinyProxy container configured to listen on port 8080. Deploy to Railway (Docker) for an on-demand HTTP proxy.

## Local build & test

# Linux / macOS
docker build -t cumpair-proxy --build-arg PROXY_USER=youruser --build-arg PROXY_PASS=yourpass .
docker run -p 8080:8080 cumpair-proxy

# Test from another terminal:
curl -x http://youruser:yourpass@localhost:8080 https://api.ipify.org

## Deploy to Railway (web UI)
1. Push this repo to GitHub.
2. Go to https://railway.app → New Project → Deploy from GitHub Repo → select this repo.
3. Railway will detect the Dockerfile. In project settings, set Environment Variables:
   - PROXY_USER (e.g. youruser)
   - PROXY_PASS (e.g. yourpass)
4. Deploy. Railway gives a domain like `yourapp.up.railway.app`.
5. Test (replace domain and creds):
   curl -x http://youruser:yourpass@yourapp.up.railway.app:8080 https://api.ipify.org

## Start/Stop using Railway CLI
Install Railway CLI, login, then:
# Deploy (starts the instance)
railway up

# Remove the most recent deployment (stops and prevents hours from accruing)
railway down
