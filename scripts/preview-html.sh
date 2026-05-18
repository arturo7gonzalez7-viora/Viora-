#!/bin/bash
# Auto-generate preview URL for HTML files
# Usage: ./preview-html.sh <html-file>

set -e

HTML_FILE="$1"
PREVIEW_DIR="/root/.openclaw/workspace/output/previews"
PREVIEW_PORT=8765

if [ -z "$HTML_FILE" ]; then
    echo "Usage: $0 <html-file>" >&2
    exit 1
fi

if [ ! -f "$HTML_FILE" ]; then
    echo "Error: File not found: $HTML_FILE" >&2
    exit 1
fi

# Generate unique ID
PREVIEW_ID=$(date +%Y%m%d_%H%M%S)_$(head -c 4 /dev/urandom | xxd -p)
PREVIEW_NAME="preview_${PREVIEW_ID}.html"
PREVIEW_PATH="${PREVIEW_DIR}/${PREVIEW_NAME}"

# Copy file to previews
cp "$HTML_FILE" "$PREVIEW_PATH"

# Ensure preview server is running
if ! pgrep -f "python3.*http.server.*${PREVIEW_PORT}" > /dev/null; then
    cd "$PREVIEW_DIR"
    nohup python3 -m http.server ${PREVIEW_PORT} > /tmp/preview-server.log 2>&1 &
    sleep 1
fi

# Get server IP
SERVER_IP="31.97.7.46"
PREVIEW_URL="http://${SERVER_IP}:${PREVIEW_PORT}/${PREVIEW_NAME}"

echo "$PREVIEW_URL"
