#!/bin/bash
# Start preview server with cloudflare tunnel

PREVIEW_DIR="/root/.openclaw/workspace/output/previews"
PREVIEW_PORT=8765
TUNNEL_LOG="/tmp/preview-tunnel.log"

# Start HTTP server if not running
if ! pgrep -f "python3.*http.server.*${PREVIEW_PORT}" > /dev/null; then
    cd "$PREVIEW_DIR"
    python3 -m http.server ${PREVIEW_PORT} > /dev/null 2>&1 &
    echo "Started HTTP server on port ${PREVIEW_PORT}"
fi

# Start cloudflare tunnel if not running
if ! pgrep -f "cloudflared.*tunnel.*${PREVIEW_PORT}" > /dev/null; then
    cloudflared tunnel --url http://localhost:${PREVIEW_PORT} > "$TUNNEL_LOG" 2>&1 &
    sleep 3
    echo "Started cloudflare tunnel"
fi

# Extract and display tunnel URL
sleep 2
TUNNEL_URL=$(grep -oP 'https://[a-z0-9-]+\.trycloudflare\.com' "$TUNNEL_LOG" | tail -1)

if [ -n "$TUNNEL_URL" ]; then
    echo "$TUNNEL_URL"
    echo "$TUNNEL_URL" > /tmp/preview-tunnel-url.txt
else
    echo "Error: Could not get tunnel URL" >&2
    exit 1
fi
