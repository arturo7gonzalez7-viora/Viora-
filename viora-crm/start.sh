#!/bin/bash
# Viora CRM — Start Script
cd "$(dirname "$0")"

echo "🚀 Starting Viora CRM on port 5555..."
echo "   Dashboard: http://localhost:5555"
echo "   DB: /root/.openclaw/workspace/scripts/viora-outreach/viora.db"

python3 app.py
