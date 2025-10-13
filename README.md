# cumpair-proxy (Render)

TinyProxy container (HTTP proxy) listening on port 8080 — ready for Render deployment.

## Local test
docker build -t cumpair-proxy --build-arg PROXY_USER=youruser --build-arg PROXY_PASS=yourpass .
docker run -p 8080:8080 cumpair-proxy
curl -x http://youruser:yourpass@localhost:8080 https://api.ipify.org

## Deploy to Render
1. Push repo to GitHub.
2. Sign in to https://render.com and create a new Web Service (Docker).
3. Connect the GitHub repo and select the branch.
4. Set Environment Variables:
   - PROXY_USER=youruser
   - PROXY_PASS=yourpass
5. Set the port to 8080 if prompted.
6. Deploy and test:
   curl -x http://youruser:yourpass@<your-service-host>:8080 https://api.ipify.org
