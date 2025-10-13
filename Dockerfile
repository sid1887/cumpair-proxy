# TinyProxy on Ubuntu 22.04 - listens on port 8080
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install tinyproxy + apache2-utils (htpasswd) and ca-certificates
RUN apt-get update \
 && apt-get install -y --no-install-recommends tinyproxy apache2-utils ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# default build args (override at build or set env in Railway)
ARG PROXY_USER=user
ARG PROXY_PASS=pass

# Create a tinyproxy config that listens on 8080 and uses BasicAuth
RUN mkdir -p /var/log/tinyproxy

RUN printf 'User nobody\nGroup nogroup\nPort 8080\nTimeout 600\nDefaultErrorFile \"/usr/share/tinyproxy/default.html\"\nLogfile \"/var/log/tinyproxy/tinyproxy.log\"\nPidFile \"/run/tinyproxy/tinyproxy.pid\"\nMaxClients 100\nMinSpareServers 5\nMaxSpareServers 20\nStartServers 10\nAllow 0.0.0.0/0\nBasicAuth %s %s\n' "${PROXY_USER}" "${PROXY_PASS}" > /etc/tinyproxy/tinyproxy.conf

EXPOSE 8080

CMD ["tinyproxy", "-d"]
