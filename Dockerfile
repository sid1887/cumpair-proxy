FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends tinyproxy ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/log/tinyproxy && chown -R nobody:nogroup /var/log/tinyproxy

# Minimal working config
RUN printf '\
User nobody\n\
Group nogroup\n\
Port 8080\n\
Timeout 600\n\
Logfile "/var/log/tinyproxy/tinyproxy.log"\n\
MaxClients 100\n\
Allow 0.0.0.0/0\n\
' > /etc/tinyproxy/tinyproxy.conf

EXPOSE 8080

CMD ["tinyproxy", "-d"]
