#!/bin/bash
# Daily cost cleanup script

# Clean sessions over 7 days old
find ~/.openclaw/agents/main/sessions/ -name "*.jsonl" -mtime +7 -delete

# Run OpenClaw session cleanup
openclaw sessions cleanup

echo "✅ Cleaned old sessions to reduce costs"