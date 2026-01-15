#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
for f in .cf_pid .server_pid; do
  if [[ -f "$f" ]]; then
    pid=$(cat "$f" || true)
    if [[ -n "$pid" ]] && ps -p "$pid" >/dev/null 2>&1; then
      kill "$pid" || true
      echo "Stopped $f (PID $pid)"
    fi
    rm -f "$f"
  fi
done
