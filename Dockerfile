FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install Tinyproxy and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tinyproxy \
    apache2-utils \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Proxy credentials
ARG PROXY_USER=sidraj
ARG PROXY_PASS=sidraj1887

# Create necessary directories with proper permissions
RUN mkdir -p /var/log/tinyproxy /var/run/tinyproxy && \
    chown -R nobody:nogroup /var/log/tinyproxy /var/run/tinyproxy

# Create optimized Tinyproxy configuration
RUN cat > /etc/tinyproxy/tinyproxy.conf <<'EOF'
# User and Group
User nobody
Group nogroup

# Port to listen on
Port 8080

# Bind to all interfaces
Bind 0.0.0.0

# Timeout for connections (10 minutes)
Timeout 600

# Logging
LogFile "/var/log/tinyproxy/tinyproxy.log"
LogLevel Info

# PID file
PidFile "/var/run/tinyproxy/tinyproxy.pid"

# Performance tuning - Maximum number of clients
MaxClients 200

# Maximum requests per child process
MaxRequestsPerChild 10000

# Minimum and maximum spare servers
MinSpareServers 5
MaxSpareServers 20

# Start servers
StartServers 10

# Allow connections from anywhere
Allow 0.0.0.0/0

# Disable Via header to avoid 400 errors on HTTPS
DisableViaHeader Yes

# Enable CONNECT method for HTTPS tunneling
ConnectPort 443
ConnectPort 563
ConnectPort 8443

# Disable filtering
FilterDefaultDeny No

EOF

# Remove htpasswd creation since we're not using BasicAuth
# BasicAuth causes issues with CONNECT method in Tinyproxy

# Note: Without BasicAuth, the proxy is open. For production, consider:
# 1. Use IP whitelisting in Render
# 2. Use a reverse proxy with authentication (nginx)
# 3. Use VPN or private network

# Expose the proxy port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f -x http://localhost:8080 http://www.google.com || exit 1

# Start Tinyproxy in foreground with debug mode
CMD ["tinyproxy", "-d"]
