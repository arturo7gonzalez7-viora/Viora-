#!/bin/bash
# Quick HTML preview server for OpenClaw
# Usage: ./serve-preview.sh <html-file>

HTML_FILE="$1"
PORT="${2:-8888}"

if [ -z "$HTML_FILE" ]; then
    echo "Usage: $0 <html-file> [port]"
    exit 1
fi

if [ ! -f "$HTML_FILE" ]; then
    echo "Error: File not found: $HTML_FILE"
    exit 1
fi

# Copy to output/preview/ with a timestamped name
PREVIEW_DIR="/root/.openclaw/workspace/output/preview"
mkdir -p "$PREVIEW_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BASENAME=$(basename "$HTML_FILE" .html)
PREVIEW_FILE="${PREVIEW_DIR}/${BASENAME}_${TIMESTAMP}.html"
cp "$HTML_FILE" "$PREVIEW_FILE"

# Get the Cloudflare tunnel URL
TUNNEL_URL=$(journalctl -u cloudflared-tunnel --no-pager -n 50 | grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' | tail -1)

if [ -z "$TUNNEL_URL" ]; then
    echo "Error: Cloudflare tunnel URL not found"
    echo "Run: journalctl -u cloudflared-tunnel"
    exit 1
fi

# Construct the preview URL
RELATIVE_PATH="workspace/output/preview/${BASENAME}_${TIMESTAMP}.html"
PREVIEW_URL="${TUNNEL_URL}/${RELATIVE_PATH}"

echo "✅ Preview ready!"
echo "📄 File: $PREVIEW_FILE"
echo "🔗 Preview: $PREVIEW_URL"
echo ""
echo "Note: Cloudflare tunnel must serve static files for this to work."
echo "If the preview doesn't load, you may need to configure the tunnel or use a different serving method."
