#!/bin/bash
# ============================================================
# JARVIS AUTOMATE v3 — Daily Viora Outreach Engine
# Runs: 8am Mon-Fri via cron (14:00 UTC for Denver 8am MDT)
# 
# Pipeline:
#   1. Check replies from yesterday (detect bounces, unsubscribes, positive replies)
#   2. Scrape fresh leads (auto-rotates industry/city daily)
#   3. Find emails for leads missing them
#   4. Send cold emails (respects warmup + daily limit)
#   5. Generate LinkedIn DM queue
#   6. Send daily report to Discord
# ============================================================

set -euo pipefail

SCRIPT_DIR="/root/.openclaw/workspace/scripts/viora-outreach"
LOG_DIR="$SCRIPT_DIR/logs"
TODAY=$(date +%Y-%m-%d)
LOG="$LOG_DIR/automate_$TODAY.log"
mkdir -p "$LOG_DIR" "$SCRIPT_DIR/output"

# Load env vars
[ -f "$SCRIPT_DIR/.env" ] && set -a && source "$SCRIPT_DIR/.env" && set +a

# Ensure we're in the right directory (for relative imports)
cd "$SCRIPT_DIR"

banner() {
  echo "" | tee -a "$LOG"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG"
  echo "  $1" | tee -a "$LOG"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG"
}

banner "🤖 JARVIS AUTOMATE v3 — $TODAY $(date +%H:%M)"

# ── STEP 0: Check for replies (bounces, unsubscribes, positive) ──
banner "📬 STEP 0/5: Checking for replies"
python3 "$SCRIPT_DIR/reply-checker.py" 2>&1 | tee -a "$LOG" || true

# ── STEP 1: Scrape fresh leads (auto-rotate) ────────────────────
banner "📍 STEP 1/5: Scraping fresh leads (auto-rotate)"
if [ -n "${GOOGLE_MAPS_KEY:-}" ]; then
  python3 "$SCRIPT_DIR/lead-scraper.py" --rotate --limit 50 2>&1 | tee -a "$LOG" || true
else
  echo "⚠️  GOOGLE_MAPS_KEY not set — skipping scrape" | tee -a "$LOG"
fi

# ── STEP 2: Find emails for new leads ────────────────────────────
banner "🔍 STEP 2/5: Finding emails"
if [ -n "${HUNTER_API_KEY:-}" ]; then
  python3 "$SCRIPT_DIR/find-emails.py" --limit 50 2>&1 | tee -a "$LOG" || true
else
  echo "⚠️  Using pattern guessing (set HUNTER_API_KEY for better results)" | tee -a "$LOG"
  python3 "$SCRIPT_DIR/find-emails.py" --limit 50 --guess-only 2>&1 | tee -a "$LOG" || true
fi

# ── STEP 3: Send cold emails ─────────────────────────────────────
banner "📧 STEP 3/5: Sending cold emails"
# DISABLED: email-sender.py (too many bounces) 2>&1 | tee -a "$LOG" || true

# ── STEP 4: Generate LinkedIn DM queue ───────────────────────────
banner "💼 STEP 4/5: Generating LinkedIn DM queue"
python3 "$SCRIPT_DIR/linkedin-queue.py" 2>&1 | tee -a "$LOG" || true

# ── STEP 5: Daily report ─────────────────────────────────────────
banner "📊 STEP 5/5: Daily report"
python3 "$SCRIPT_DIR/daily-report.py" 2>&1 | tee -a "$LOG" || true

# ── DONE ──────────────────────────────────────────────────────────
banner "✅ JARVIS AUTOMATE v3 COMPLETE — $(date)"
echo "" | tee -a "$LOG"
echo "Your only jobs today:" | tee -a "$LOG"
echo "  1. Check email for replies (especially positive ones!)" | tee -a "$LOG"
echo "  2. Send LinkedIn DMs from: $SCRIPT_DIR/output/" | tee -a "$LOG"
echo "  3. Show up to demo calls and close" | tee -a "$LOG"
echo "" | tee -a "$LOG"
echo "📄 Full log: $LOG" | tee -a "$LOG"
