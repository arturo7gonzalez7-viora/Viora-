#!/bin/bash
# ============================================================
# VIORA OUTREACH MACHINE — SETUP
# Run once: bash setup.sh
# ============================================================

SCRIPT_DIR="/root/.openclaw/workspace/scripts/viora-outreach"
cd "$SCRIPT_DIR"

echo ""
echo "🚀 VIORA OUTREACH MACHINE SETUP"
echo "================================"
echo ""

# Install Python dependencies
echo "📦 Installing dependencies..."
python3 -m pip install --quiet --break-system-packages \
  google-auth google-auth-oauthlib google-auth-httplib2 \
  google-api-python-client gspread requests python-dotenv 2>&1 | grep -v WARNING || true
echo "✅ Dependencies installed"
echo ""

# Create directory structure
mkdir -p "$SCRIPT_DIR/logs" "$SCRIPT_DIR/output"
echo "✅ Directories created"
echo ""

# Initialize SQLite DB
python3 -c "from db import init_db; init_db(); print('✅ Database initialized (viora.db)')"
echo ""

# Create .env if it doesn't exist
ENV_FILE="$SCRIPT_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
cat > "$ENV_FILE" << 'ENVEOF'
# VIORA OUTREACH MACHINE — Fill these in
# See ARTURO-ACTION-LIST.md for step-by-step instructions

# Gmail address for sending
GMAIL_ADDRESS=arturo.vioraai@gmail.com

# Google Maps API key (console.cloud.google.com — free)
GOOGLE_MAPS_KEY=

# Hunter.io API key (hunter.io — 25 free/month, $49/mo for 500)
HUNTER_API_KEY=

# Google Sheet ID (optional — from your sheet URL)
GOOGLE_SHEET_ID=

# Discord webhook for daily reports (Discord → channel settings → Integrations → Webhooks)
DISCORD_WEBHOOK=

# Your booking link
BOOKING_URL=https://calendar.app.google/pHa5h8Faxr2Qz2LL6

# Email warmup: ramps automatically. Override max here (default: 40)
# MAX_EMAILS_PER_DAY=40
ENVEOF
echo "✅ .env template created → FILL THIS IN before running"
else
  echo "✅ .env already exists"
fi
echo ""

# Set up cron (8am Denver time = 14:00 UTC during MDT, 15:00 UTC during MST)
echo "⏰ Setting up cron job (8am Mon-Fri Denver time)..."
CRON_CMD="0 14 * * 1-5 cd $SCRIPT_DIR && bash jarvis-automate.sh >> $SCRIPT_DIR/logs/cron.log 2>&1"

(crontab -l 2>/dev/null | grep -q "jarvis-automate") && \
  echo "✅ Cron already configured" || \
  { (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab - && echo "✅ Cron job set (8am Mon-Fri Denver)"; }
echo ""

# Done
echo "================================"
echo "✅ SETUP COMPLETE"
echo ""
echo "📋 NEXT: Open and fill in your .env file:"
echo "   $ENV_FILE"
echo ""
echo "Then test with:"
echo "   python3 email-sender.py --dry-run"
echo ""
echo "Then launch:"
echo "   bash jarvis-automate.sh"
echo "================================"
echo ""
