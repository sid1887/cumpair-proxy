#!/usr/bin/env bash
set -e

# Default PORT fallback
export PORT="${PORT:-8080}"

echo "🚀 Starting Tinyproxy on port $PORT"

# Ensure log dir exists
mkdir -p /var/log/tinyproxy /var/run/tinyproxy
chown -R nobody:nogroup /var/log/tinyproxy /var/run/tinyproxy

# Use envsubst to expand ${PORT} into the config
# Export PORT so envsubst can see it
export PORT
envsubst '${PORT}' < /etc/tinyproxy/tinyproxy.conf.template > /etc/tinyproxy/tinyproxy.conf

echo "✅ Configuration generated for port $PORT"
cat /etc/tinyproxy/tinyproxy.conf

# Start tinyproxy in foreground
exec tinyproxy -d
