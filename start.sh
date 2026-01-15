#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Kill previous
for f in .server_pid .cf_pid; do
  if [[ -f "$f" ]]; then
    pid=$(cat "$f" || true)
    if [[ -n "${pid}" ]] && ps -p "$pid" >/dev/null 2>&1; then
      kill "$pid" || true
      sleep 0.3
    fi
    rm -f "$f"
  fi
done
# Load BASIC AUTH from .auth (format: user:pass)
BASIC_AUTH_USER="${BASIC_AUTH_USER:-}"
BASIC_AUTH_PASS="${BASIC_AUTH_PASS:-}"
if [[ -f .auth ]]; then
  IFS=':' read -r BASIC_AUTH_USER BASIC_AUTH_PASS < .auth || true
fi
export BASIC_AUTH_USER BASIC_AUTH_PASS
# Start dev server
nohup env BASIC_AUTH_USER="$BASIC_AUTH_USER" BASIC_AUTH_PASS="$BASIC_AUTH_PASS" python3 devserver.py > /tmp/proppy_server.log 2>&1 &
echo $! > .server_pid
sleep 0.5
# Start tunnel
log=/tmp/proppy_cloudflared.log
rm -f "$log"
nohup cloudflared tunnel --url http://127.0.0.1:8000 --no-autoupdate >"$log" 2>&1 &
echo $! > .cf_pid
# Wait for URL
url=""
for i in $(seq 1 80); do
  if [[ -s "$log" ]]; then
    url=$(grep -Eo 'https?://[A-Za-z0-9.-]+\.trycloudflare\.com' "$log" | head -n 1 || true)
    if [[ -n "$url" ]]; then
      break
    fi
  fi
  sleep 0.5
done
echo "Local:  http://127.0.0.1:8000"
if [[ -n "$BASIC_AUTH_USER$BASIC_AUTH_PASS" ]]; then
  echo "Auth:   Basic auth enabled (use credentials from .auth)"
fi
if [[ -n "$url" ]]; then
  echo "$url" > .cf_url
  echo "Public: $url"
else
  echo "Public: (pending) — check /tmp/proppy_cloudflared.log"
fi
