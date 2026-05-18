#!/usr/bin/env python3
"""
VIORA DAILY REPORT v3
Action-focused report: what Arturo needs to DO today, not just stats.
Posts to Discord. Falls back to console if no webhook.

Usage: python3 daily-report.py
"""

import requests
from datetime import datetime, timedelta
from pathlib import Path

from config import DISCORD_WEBHOOK, OUTPUT_DIR
from db import get_stats, get_conn


def get_positive_replies():
    """Get leads that replied positively (not bounced/unsub)."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT business_name, email, reply_date
        FROM leads
        WHERE replied IS NOT NULL AND replied != ''
          AND unsubscribed = 0 AND bounced = 0
          AND status NOT IN ('closed', 'not_interested', 'sequence_complete')
        ORDER BY reply_date DESC
        LIMIT 10
    """).fetchall()
    conn.close()
    return rows


def get_todays_linkedin_dms():
    """Get DMs queued today from send_log."""
    conn = get_conn()
    today = datetime.now().strftime("%Y-%m-%d")
    rows = conn.execute("""
        SELECT l.business_name, l.city
        FROM send_log s JOIN leads l ON s.lead_id = l.id
        WHERE s.channel = 'linkedin' AND s.sent_at LIKE ?
        ORDER BY s.id
    """, (f"{today}%",)).fetchall()
    conn.close()
    return rows


def get_streak():
    """Consecutive days the system has been running."""
    conn = get_conn()
    dates = conn.execute(
        "SELECT DISTINCT substr(sent_at, 1, 10) FROM send_log ORDER BY sent_at DESC LIMIT 30"
    ).fetchall()
    conn.close()
    if not dates:
        return 0
    streak = 0
    today = datetime.now().date()
    for row in dates:
        expected = today - timedelta(days=streak)
        if row[0] == expected.strftime("%Y-%m-%d"):
            streak += 1
        else:
            break
    return streak


def build_report():
    """Build the report string. Kept under ~1900 chars for Discord."""
    stats = get_stats()
    replies = get_positive_replies()
    linkedin_dms = get_todays_linkedin_dms()
    streak = get_streak()

    closed = stats.get("total_closed", 0)
    mrr = closed * 350
    pct = min(int((mrr / 20000) * 100), 100) if mrr > 0 else 0
    bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
    clients_needed = max(0, 58 - closed)

    today_str = datetime.now().strftime("%a %b %d")
    lines = [f"**📊 VIORA REPORT — {today_str}** (Day {streak})"]

    # ── POSITIVE REPLIES (top priority) ──
    if replies:
        lines.append("")
        lines.append("**🔥 POSITIVE REPLIES — RESPOND NOW:**")
        for r in replies:
            lines.append(f"• **{r['business_name']}** → {r['email']}")

    # ── TODAY'S ACTION ITEMS ──
    lines.append("")
    lines.append("**📋 YOUR TODO:**")
    if replies:
        lines.append(f"1️⃣ Reply to {len(replies)} lead(s) above (use templates in email-sequences.md)")
    if linkedin_dms:
        lines.append(f"{'2️⃣' if replies else '1️⃣'} Send {len(linkedin_dms)} LinkedIn DMs (posted above or in output/)")
    lines.append(f"{'3️⃣' if replies or linkedin_dms else '1️⃣'} Check calendar for demo calls")

    # ── TODAY'S NUMBERS ──
    lines.append("")
    lines.append(
        f"**📧 Today:** {stats.get('emails_sent_today', 0)} emails sent · "
        f"{stats.get('linkedin_sent_today', 0)} LinkedIn DMs"
    )

    # ── FUNNEL ──
    total = stats.get("total_leads", 0)
    contacted = stats.get("total_email_1", 0)
    replied_n = stats.get("total_replied", 0)
    demos = stats.get("total_demos", 0)
    reply_rate = round(replied_n / contacted * 100, 1) if contacted else 0

    lines.append(
        f"**📊 Funnel:** {total} leads → {contacted} contacted → "
        f"{replied_n} replied ({reply_rate}%) → {demos} demos → {closed} closed"
    )

    # ── MRR TRACKER ──
    lines.append("")
    lines.append(f"**💰 MRR:** ${mrr:,}/mo [{bar}] {pct}% of $20k")
    if clients_needed > 0:
        lines.append(f"Need **{clients_needed}** more clients @ $350/mo")

    # ── INLINE LINKEDIN DMs (compact) ──
    if linkedin_dms and len(linkedin_dms) <= 5:
        lines.append("")
        lines.append("**💼 LinkedIn DMs today:**")
        for i, dm in enumerate(linkedin_dms, 1):
            lines.append(f"{i}. {dm['business_name']} ({dm['city']})")
    elif linkedin_dms:
        lines.append(f"\n**💼 {len(linkedin_dms)} LinkedIn DMs** queued — check Discord or output/ folder")

    return "\n".join(lines)


def send_to_discord(report):
    """Post report to Discord webhook."""
    try:
        resp = requests.post(DISCORD_WEBHOOK, json={"content": report}, timeout=10)
        if resp.status_code in (200, 204):
            print("✅ Report sent to Discord")
        else:
            print(f"⚠️  Discord {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        print(f"❌ Discord failed: {e}")


def main():
    report = build_report()

    # Always print to console
    print(report)
    print()

    # Send to Discord if webhook exists
    if DISCORD_WEBHOOK:
        send_to_discord(report)
    else:
        print("⚠️  Set DISCORD_WEBHOOK in .env for Discord reports")


if __name__ == "__main__":
    main()
