FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install Tinyproxy and utils
RUN apt-get update && \
    apt-get install -y --no-install-recommends tinyproxy apache2-utils ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Proxy credentials
ARG PROXY_USER=user
ARG PROXY_PASS=pass

# Prepare log directory
RUN mkdir -p /var/log/tinyproxy && chown -R nobody:nogroup /var/log/tinyproxy

# Tinyproxy config with CONNECT allowed for HTTPS
RUN printf '\
User nobody\n\
Group nogroup\n\
Port 8080\n\
Timeout 600\n\
Logfile "/var/log/tinyproxy/tinyproxy.log"\n\
MaxClients 100\n\
MinSpareServers 5\n\
MaxSpareServers 20\n\
StartServers 10\n\
Allow 0.0.0.0/0\n\
BasicAuth %s %s\n\
ConnectPort 443\n\
ConnectPort 8443\n\
' "${PROXY_USER}" "${PROXY_PASS}" > /etc/tinyproxy/tinyproxy.conf

EXPOSE 8080

CMD ["tinyproxy", "-d"]
