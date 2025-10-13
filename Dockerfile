FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends tinyproxy apache2-utils ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Arguments for proxy credentials
ARG PROXY_USER=user
ARG PROXY_PASS=pass

# Create log directory
RUN mkdir -p /var/log/tinyproxy && chown -R nobody:nogroup /var/log/tinyproxy

# Generate hashed password for BasicAuth
RUN htpasswd -cb /etc/tinyproxy/htpasswd "${PROXY_USER}" "${PROXY_PASS}"

# Write a minimal working Tinyproxy config
RUN printf '\
User nobody\n\
Group nogroup\n\
Port 8080\n\
Timeout 600\n\
Logfile "/var/log/tinyproxy/tinyproxy.log"\n\
MaxClients 100\n\
Allow 0.0.0.0/0\n\
BasicAuth %s\n\
' "/etc/tinyproxy/htpasswd" > /etc/tinyproxy/tinyproxy.conf

# Expose port
EXPOSE 8080

# Run Tinyproxy in foreground
CMD ["tinyproxy", "-d"]
