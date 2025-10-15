FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install Tinyproxy and dependencies (including gettext-base for envsubst)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tinyproxy \
    ca-certificates \
    curl \
    gettext-base \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories with proper permissions
RUN mkdir -p /var/log/tinyproxy /var/run/tinyproxy && \
    chown -R nobody:nogroup /var/log/tinyproxy /var/run/tinyproxy

# Copy template and entrypoint
COPY tinyproxy.conf.template /etc/tinyproxy/tinyproxy.conf.template
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Expose the proxy port (will be overridden by $PORT at runtime)
EXPOSE 8080

# Health check using $PORT
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f -x http://localhost:${PORT:-8080} http://www.google.com || exit 1

# Start using entrypoint script
CMD ["/usr/local/bin/entrypoint.sh"]
