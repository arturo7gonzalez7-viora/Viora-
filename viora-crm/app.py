#!/usr/bin/env python3
"""Viora CRM — Flask backend for Arturo's daily outreach dashboard."""

import os
import sys
import sqlite3
import json
import pickle
import re
import urllib.request
from datetime import datetime, date, timedelta
from flask import Flask, jsonify, request, render_template

try:
    import requests as req_lib
    from bs4 import BeautifulSoup
    HAS_SCRAPING = True
except ImportError:
    HAS_SCRAPING = False

app = Flask(__name__, static_folder='static', static_url_path='/static')
DB_PATH = "/root/.openclaw/workspace/scripts/viora-outreach/viora.db"
ENV_PATH = "/root/.openclaw/workspace/scripts/viora-outreach/.env"
BOOKING_URL = "https://calendar.app.google/V5Facsr8nXZQRrdQ8"
GMAIL_TOKEN_PATH = "/root/.openclaw/workspace/scripts/viora-outreach/gmail_token.pickle"

# Tier pricing
SETUP_FEES = {"starter": 1550, "growth": 2575, "scale": 3600}
MONTHLY_FEES = {"starter": 360, "growth": 770, "scale": 1544}

def load_env():
    env = {}
    try:
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return env

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def dict_row(row):
    return dict(row) if row else None

def dict_rows(rows):
    return [dict(r) for r in rows]

def ensure_clients_table():
    """Create clients table if it doesn't exist."""
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER,
            business_name TEXT NOT NULL,
            owner_name TEXT,
            email TEXT,
            phone TEXT,
            industry TEXT,
            city TEXT,
            monthly_value REAL DEFAULT 500,
            setup_fee REAL DEFAULT 0,
            setup_fee_date TEXT,
            start_date TEXT,
            next_checkin TEXT,
            notes TEXT,
            active INTEGER DEFAULT 1,
            created_at TEXT,
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        )
    """)
    db.commit()
    db.close()

ensure_clients_table()

def ensure_instagram_column():
    """Add instagram_sent column to leads table if missing."""
    db = get_db()
    cols = [r[1] for r in db.execute('PRAGMA table_info(leads)').fetchall()]
    if 'instagram_sent' not in cols:
        db.execute('ALTER TABLE leads ADD COLUMN instagram_sent TEXT')
        db.commit()
    db.close()

ensure_instagram_column()

def ensure_invoices_table():
    """Create invoices table if it doesn't exist."""
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            client_name TEXT,
            client_email TEXT,
            amount REAL,
            description TEXT,
            type TEXT,
            status TEXT DEFAULT 'pending',
            payment_link TEXT,
            stripe_payment_id TEXT,
            created_at TEXT,
            paid_at TEXT,
            due_date TEXT
        )
    """)
    db.commit()
    db.close()

ensure_invoices_table()

def ensure_audit_reports_table():
    """Create audit_reports table if it doesn't exist."""
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS audit_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_name TEXT,
            website TEXT,
            industry TEXT,
            scraped_data TEXT,
            recommendations TEXT,
            total_roi_estimate REAL,
            created_at TEXT,
            lead_id INTEGER
        )
    """)
    db.commit()
    db.close()

ensure_audit_reports_table()

def get_stripe_key():
    """Load Stripe secret key from .env file."""
    env = load_env()
    return env.get("STRIPE_SECRET_KEY", "").strip()

def send_email_via_gmail(to_email, subject, body_html):
    """Send email using Gmail API with saved credentials."""
    try:
        from googleapiclient.discovery import build
        from google.auth.transport.requests import Request
        import base64
        from email.mime.text import MIMEText

        if not os.path.exists(GMAIL_TOKEN_PATH):
            return False, "Gmail token not found"

        with open(GMAIL_TOKEN_PATH, 'rb') as f:
            creds = pickle.load(f)

        if hasattr(creds, 'expired') and creds.expired and hasattr(creds, 'refresh_token'):
            creds.refresh(Request())

        service = build('gmail', 'v1', credentials=creds)
        msg = MIMEText(body_html, 'html')
        msg['to'] = to_email
        msg['subject'] = subject
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        service.users().messages().send(userId='me', body={'raw': raw}).execute()
        return True, "Sent"
    except Exception as e:
        return False, str(e)

# ─── Pages ───────────────────────────────────────────────────────────────

@app.route("/")
def index():
    env = load_env()
    return render_template("index.html",
                           booking_url=BOOKING_URL,
                           max_emails=int(env.get("MAX_EMAILS_PER_DAY", 40)))

@app.route("/playbook")
def playbook():
    return render_template("playbook.html")

# ─── API: Today's Mission ────────────────────────────────────────────────

@app.route("/api/mission")
def mission():
    db = get_db()
    today = date.today().isoformat()
    week_start = (date.today() - timedelta(days=date.today().weekday())).isoformat()

    hot = dict_rows(db.execute("""
        SELECT id, business_name, city, email, phone, owner_name, industry, notes
        FROM leads WHERE status = 'interested' AND unsubscribed = 0 AND bounced = 0
        ORDER BY reply_date DESC LIMIT 20
    """).fetchall())

    three_days_ago = (date.today() - timedelta(days=3)).isoformat()
    followups = dict_rows(db.execute("""
        SELECT id, business_name, city, email, owner_name, industry,
               email_1_sent, email_2_sent, email_3_sent,
               CASE
                 WHEN email_2_sent IS NULL AND email_1_sent IS NOT NULL AND email_1_sent <= ? THEN 2
                 WHEN email_3_sent IS NULL AND email_2_sent IS NOT NULL AND email_2_sent <= ? THEN 3
               END as next_seq
        FROM leads
        WHERE status IN ('contacted', 'new')
          AND email IS NOT NULL AND email != ''
          AND unsubscribed = 0 AND bounced = 0
          AND replied IS NULL
          AND (
            (email_2_sent IS NULL AND email_1_sent IS NOT NULL AND email_1_sent <= ?)
            OR (email_3_sent IS NULL AND email_2_sent IS NOT NULL AND email_2_sent <= ?)
          )
        ORDER BY email_1_sent ASC
        LIMIT 30
    """, (three_days_ago, three_days_ago, three_days_ago, three_days_ago)).fetchall())

    linkedin = dict_rows(db.execute("""
        SELECT id, business_name, city, industry, owner_name
        FROM leads
        WHERE (linkedin_sent IS NULL OR linkedin_sent = '')
          AND status NOT IN ('bounced', 'lost')
          AND unsubscribed = 0
          AND business_name IS NOT NULL AND business_name != ''
        ORDER BY RANDOM()
        LIMIT 20
    """).fetchall())

    emails_today = db.execute(
        "SELECT COUNT(*) FROM send_log WHERE date(sent_at) = ? AND channel = 'email'", (today,)
    ).fetchone()[0]

    linkedin_today = db.execute(
        "SELECT COUNT(*) FROM leads WHERE linkedin_sent = ?", (today,)
    ).fetchone()[0]

    demos_week = db.execute(
        "SELECT COUNT(*) FROM leads WHERE demo_booked IS NOT NULL AND demo_date >= ?", (week_start,)
    ).fetchone()[0]

    db.close()
    return jsonify({
        "hot_leads": hot,
        "followups": followups,
        "linkedin_queue": linkedin,
        "emails_today": emails_today,
        "linkedin_today": linkedin_today,
        "demos_this_week": demos_week,
    })

# ─── API: Daily Wins ─────────────────────────────────────────────────────

@app.route("/api/wins")
def daily_wins():
    db = get_db()
    today = date.today().isoformat()
    week_start = (date.today() - timedelta(days=date.today().weekday())).isoformat()

    replies_today = dict_rows(db.execute("""
        SELECT id, business_name, city, industry, owner_name
        FROM leads WHERE reply_date = ? AND bounced = 0
    """, (today,)).fetchall())

    demos_today = dict_rows(db.execute("""
        SELECT id, business_name, city, industry, owner_name, demo_date
        FROM leads WHERE demo_booked = ? AND bounced = 0
    """, (today,)).fetchall())

    closed_week = dict_rows(db.execute("""
        SELECT id, business_name, city, industry, owner_name, closed_date
        FROM leads WHERE closed IS NOT NULL AND closed != '' AND closed != '0'
          AND closed_date >= ? AND bounced = 0
    """, (week_start,)).fetchall())

    db.close()
    return jsonify({
        "replies_today": replies_today,
        "demos_today": demos_today,
        "closed_this_week": closed_week,
    })

# ─── API: Pipeline ───────────────────────────────────────────────────────

@app.route("/api/pipeline")
def pipeline():
    db = get_db()
    stages = {
        "new": [], "contacted": [], "interested": [],
        "demo_booked": [], "closed": [], "lost": [],
    }

    rows = dict_rows(db.execute("""
        SELECT id, business_name, city, industry, status, email, owner_name,
               demo_booked, demo_date, closed, closed_date, notes,
               email_1_sent, email_2_sent, email_3_sent, replied
        FROM leads WHERE bounced = 0 AND unsubscribed = 0
        ORDER BY last_updated DESC
    """).fetchall())

    for r in rows:
        if r.get("closed") and r["closed"] not in (None, '', '0'):
            stages["closed"].append(r)
        elif r.get("demo_booked") and r["demo_booked"] not in (None, '', '0'):
            stages["demo_booked"].append(r)
        elif r["status"] in stages:
            stages[r["status"]].append(r)

    # MRR from clients table
    client_mrr = db.execute(
        "SELECT COALESCE(SUM(monthly_value), 0) FROM clients WHERE active = 1"
    ).fetchone()[0]
    closed_count = len(stages.get("closed", []))
    mrr = client_mrr if client_mrr > 0 else closed_count * 500

    db.close()
    return jsonify({
        "stages": {k: v[:50] for k, v in stages.items()},
        "counts": {k: len(v) for k, v in stages.items()},
        "mrr": mrr,
        "mrr_goal": 20000,
    })

# ─── API: Revenue ────────────────────────────────────────────────────────

@app.route("/api/revenue")
def revenue():
    db = get_db()
    today = date.today()
    month_start = today.replace(day=1).isoformat()

    client_mrr = db.execute(
        "SELECT COALESCE(SUM(monthly_value), 0) FROM clients WHERE active = 1"
    ).fetchone()[0]

    setup_fees_month = db.execute(
        "SELECT COALESCE(SUM(setup_fee), 0) FROM clients WHERE setup_fee_date >= ?",
        (month_start,)
    ).fetchone()[0]

    # Pipeline projections
    demo_count = db.execute(
        "SELECT COUNT(*) FROM leads WHERE demo_booked IS NOT NULL AND demo_booked != '' "
        "AND (closed IS NULL OR closed = '' OR closed = '0') AND bounced = 0"
    ).fetchone()[0]
    interested_count = db.execute(
        "SELECT COUNT(*) FROM leads WHERE status = 'interested' AND bounced = 0 "
        "AND (demo_booked IS NULL OR demo_booked = '')"
    ).fetchone()[0]
    contacted_count = db.execute(
        "SELECT COUNT(*) FROM leads WHERE status = 'contacted' AND bounced = 0"
    ).fetchone()[0]

    # Projections: demo=40% close, interested=15%, contacted=3%
    proj_30 = client_mrr + (demo_count * 0.4 * 500)
    proj_60 = proj_30 + (interested_count * 0.15 * 500)
    proj_90 = proj_60 + (contacted_count * 0.03 * 500)

    # Days since last close
    last_close = db.execute(
        "SELECT MAX(closed_date) FROM leads WHERE closed IS NOT NULL AND closed != '' AND closed != '0'"
    ).fetchone()[0]
    days_since_close = None
    if last_close:
        try:
            days_since_close = (today - datetime.fromisoformat(last_close).date()).days
        except:
            pass

    db.close()
    return jsonify({
        "mrr": client_mrr,
        "mrr_goal": 20000,
        "setup_fees_month": setup_fees_month,
        "proj_30": round(proj_30),
        "proj_60": round(proj_60),
        "proj_90": round(proj_90),
        "demo_pipeline": demo_count,
        "interested_pipeline": interested_count,
        "days_since_close": days_since_close,
    })

# ─── API: Outreach Health ────────────────────────────────────────────────

@app.route("/api/health")
def outreach_health():
    db = get_db()
    env = load_env()
    today = date.today().isoformat()
    max_emails = int(env.get("MAX_EMAILS_PER_DAY", 40))

    emails_today = db.execute(
        "SELECT COUNT(*) FROM send_log WHERE date(sent_at) = ? AND channel = 'email'", (today,)
    ).fetchone()[0]

    bounced_recent = db.execute(
        "SELECT COUNT(*) FROM leads WHERE bounced = 1 AND date_added >= ?",
        ((date.today() - timedelta(days=7)).isoformat(),)
    ).fetchone()[0]

    total_sent_week = db.execute(
        "SELECT COUNT(*) FROM send_log WHERE date(sent_at) >= ?",
        ((date.today() - timedelta(days=7)).isoformat(),)
    ).fetchone()[0]

    # Domain reputation heuristic
    bounce_rate = bounced_recent / max(total_sent_week, 1)
    if bounce_rate < 0.05:
        domain_health = "green"
    elif bounce_rate < 0.15:
        domain_health = "yellow"
    else:
        domain_health = "red"

    last_close = db.execute(
        "SELECT MAX(closed_date) FROM leads WHERE closed IS NOT NULL AND closed != '' AND closed != '0'"
    ).fetchone()[0]
    days_since_close = None
    if last_close:
        try:
            days_since_close = (date.today() - datetime.fromisoformat(last_close).date()).days
        except:
            pass

    db.close()
    return jsonify({
        "emails_today": emails_today,
        "max_emails": max_emails,
        "domain_health": domain_health,
        "bounce_rate_7d": round(bounce_rate * 100, 1),
        "days_since_close": days_since_close,
    })

# ─── API: Email Sequence Status ──────────────────────────────────────────

@app.route("/api/leads/<int:lead_id>/sequence")
def email_sequence(lead_id):
    db = get_db()
    lead = dict_row(db.execute(
        "SELECT id, business_name, email_1_sent, email_2_sent, email_3_sent, replied, reply_date "
        "FROM leads WHERE id = ?", (lead_id,)
    ).fetchone())
    if not lead:
        db.close()
        return jsonify({"error": "not found"}), 404

    current_email = 0
    next_fire = None
    if lead["email_3_sent"]:
        current_email = 3
    elif lead["email_2_sent"]:
        current_email = 2
        next_fire_date = datetime.fromisoformat(lead["email_2_sent"]) + timedelta(days=3)
        next_fire = next_fire_date.isoformat()
    elif lead["email_1_sent"]:
        current_email = 1
        next_fire_date = datetime.fromisoformat(lead["email_1_sent"]) + timedelta(days=3)
        next_fire = next_fire_date.isoformat()

    db.close()
    return jsonify({
        "lead_id": lead_id,
        "current_email": current_email,
        "next_fire": next_fire,
        "replied": lead["replied"] is not None,
        "reply_date": lead["reply_date"],
        "sequence_complete": current_email == 3 or lead["replied"] is not None,
    })

# ─── API: Demo Prep ──────────────────────────────────────────────────────

@app.route("/api/leads/<int:lead_id>/demo-prep")
def demo_prep(lead_id):
    db = get_db()
    lead = dict_row(db.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone())
    db.close()
    if not lead:
        return jsonify({"error": "not found"}), 404

    # Build prep data
    pain_points = []
    if lead.get("industry"):
        industry_pains = {
            "med spa": ["No-show appointments", "Inconsistent booking flow", "Manual follow-ups eating staff time",
                        "Losing leads who inquire but never book"],
            "dental": ["Patient scheduling gaps", "Insurance verification delays",
                       "Follow-up calls taking too much front desk time"],
            "chiropractor": ["Patient retention after initial visit", "Manual appointment reminders",
                            "Difficulty re-engaging past patients"],
            "gym": ["Member churn", "Lead follow-up falls through cracks",
                    "Staff overwhelmed with admin vs training"],
            "salon": ["Last-minute cancellations", "Rebooking no-shows",
                      "Upselling services without being pushy"],
        }
        for key, pains in industry_pains.items():
            if key in (lead.get("industry") or "").lower():
                pain_points = pains
                break
    if not pain_points:
        pain_points = ["Manual follow-ups consuming staff time",
                       "Leads slipping through the cracks",
                       "Inconsistent customer communication"]

    return jsonify({
        "lead": lead,
        "pain_points": pain_points,
        "demo_script": {
            "opener": f"Hey {lead.get('owner_name') or 'there'}, thanks for taking the time! I've been looking at {lead['business_name']} and I think there's a huge opportunity to automate your customer flow.",
            "discovery": "What does your current process look like when a new lead comes in? How are you handling follow-ups right now?",
            "pain_agitate": f"A lot of {lead.get('industry', 'business')} owners tell me the same thing — {pain_points[0].lower()}. Sound familiar?",
            "solution": "What Viora does is sit between your leads and your team — we handle the AI-powered follow-up, booking, and re-engagement automatically. Your team focuses on delivering great service.",
            "close": "Based on what you've told me, I think we could have this running for you within a week. The setup is $997 and then $497/month. Want to get started?",
        },
        "booking_url": BOOKING_URL,
    })

# ─── API: Leads Database ─────────────────────────────────────────────────

@app.route("/api/leads")
def leads_list():
    db = get_db()
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    industry = request.args.get("industry", "").strip()
    city = request.args.get("city", "").strip()
    has_email = request.args.get("has_email", "").strip()
    has_replied = request.args.get("has_replied", "").strip()
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))

    where = ["bounced = 0"]
    params = []

    if q:
        where.append("(business_name LIKE ? OR email LIKE ? OR owner_name LIKE ? OR city LIKE ?)")
        params.extend([f"%{q}%"] * 4)
    if status:
        where.append("status = ?")
        params.append(status)
    if industry:
        where.append("industry LIKE ?")
        params.append(f"%{industry}%")
    if city:
        where.append("city LIKE ?")
        params.append(f"%{city}%")
    if has_email == "1":
        where.append("email IS NOT NULL AND email != ''")
    if has_replied == "1":
        where.append("replied IS NOT NULL")

    where_sql = " AND ".join(where)
    total = db.execute(f"SELECT COUNT(*) FROM leads WHERE {where_sql}", params).fetchone()[0]
    rows = dict_rows(db.execute(f"""
        SELECT * FROM leads WHERE {where_sql}
        ORDER BY last_updated DESC, id DESC
        LIMIT ? OFFSET ?
    """, params + [per_page, (page - 1) * per_page]).fetchall())

    db.close()
    return jsonify({"leads": rows, "total": total, "page": page, "per_page": per_page})

# ─── API: Single Lead ────────────────────────────────────────────────────

@app.route("/api/leads/<int:lead_id>")
def lead_detail(lead_id):
    db = get_db()
    row = dict_row(db.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone())
    db.close()
    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify(row)

# ─── API: Update Lead ────────────────────────────────────────────────────

@app.route("/api/leads/<int:lead_id>", methods=["PATCH"])
def update_lead(lead_id):
    db = get_db()
    data = request.json or {}
    allowed = {"status", "notes", "replied", "reply_date", "demo_booked", "demo_date",
               "closed", "closed_date", "linkedin_sent", "email_2_sent", "email_3_sent",
               "unsubscribed"}
    sets = []
    params = []
    now = datetime.utcnow().isoformat()

    for k, v in data.items():
        if k in allowed:
            sets.append(f"{k} = ?")
            params.append(v)

    if not sets:
        return jsonify({"error": "nothing to update"}), 400

    sets.append("last_updated = ?")
    params.append(now)
    params.append(lead_id)

    db.execute(f"UPDATE leads SET {', '.join(sets)} WHERE id = ?", params)
    db.commit()
    row = dict_row(db.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone())
    db.close()
    return jsonify(row)

# ─── API: Quick status change ────────────────────────────────────────────

@app.route("/api/leads/<int:lead_id>/status", methods=["POST"])
def change_status(lead_id):
    db = get_db()
    data = request.json or {}
    new_status = data.get("status")
    now = datetime.utcnow().isoformat()

    if not new_status:
        return jsonify({"error": "status required"}), 400

    updates = {"status": new_status, "last_updated": now}

    if new_status == "interested":
        updates["replied"] = "1"
        updates["reply_date"] = date.today().isoformat()
    elif new_status == "demo_booked":
        updates["demo_booked"] = date.today().isoformat()
        updates["demo_date"] = data.get("demo_date", date.today().isoformat())
    elif new_status == "closed":
        updates["closed"] = "1"
        updates["closed_date"] = date.today().isoformat()

    set_clause = ", ".join(f"{k} = ?" for k in updates)
    vals = list(updates.values()) + [lead_id]
    db.execute(f"UPDATE leads SET {set_clause} WHERE id = ?", vals)
    db.commit()
    row = dict_row(db.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone())
    db.close()
    return jsonify(row)

# ─── API: Mark LinkedIn sent ─────────────────────────────────────────────

@app.route("/api/leads/<int:lead_id>/skip", methods=["POST"])
def skip_lead(lead_id):
    """Mark a lead as not_interested so it never shows in the LinkedIn queue again."""
    db = get_db()
    db.execute("UPDATE leads SET status = 'not_interested', notes = COALESCE(notes,'') || ' [skipped from CRM]' WHERE id = ?", (lead_id,))
    db.commit()
    db.close()
    return jsonify({"ok": True})

@app.route("/api/leads/<int:lead_id>/instagram", methods=["POST"])
def mark_instagram(lead_id):
    db = get_db()
    now = date.today().isoformat()
    now_ts = datetime.utcnow().isoformat()
    db.execute("UPDATE leads SET instagram_sent = ?, status = CASE WHEN status = 'new' THEN 'contacted' ELSE status END, last_updated = ? WHERE id = ?",
               (now, now_ts, lead_id))
    db.execute("""
        INSERT INTO send_log (lead_id, email_to, subject, seq_num, channel, sent_at, status)
        VALUES (?, '', 'Instagram/Facebook DM', 1, 'instagram', ?, 'sent')
    """, (lead_id, now_ts))
    db.commit()
    db.close()
    return jsonify({"ok": True, "marked": True})

@app.route("/api/leads/<int:lead_id>/linkedin", methods=["POST"])
def mark_linkedin(lead_id):
    db = get_db()
    now = date.today().isoformat()
    now_ts = datetime.utcnow().isoformat()
    # Mark lead as linkedin_sent
    db.execute("UPDATE leads SET linkedin_sent = ?, status = 'contacted', last_updated = ? WHERE id = ?",
               (now, now_ts, lead_id))
    # Log to send_log so stats bar count is accurate
    db.execute("""
        INSERT INTO send_log (lead_id, email_to, subject, seq_num, channel, sent_at, status)
        VALUES (?, '', 'LinkedIn DM', 1, 'linkedin', ?, 'sent')
    """, (lead_id, now_ts))
    db.commit()
    db.close()
    return jsonify({"ok": True, "marked": True})

# ─── API: Quick Add Lead ─────────────────────────────────────────────────

@app.route("/api/leads", methods=["POST"])
def add_lead():
    db = get_db()
    data = request.json or {}
    now = datetime.utcnow().isoformat()

    db.execute("""
        INSERT INTO leads (business_name, owner_name, email, phone, city, industry, status,
                           notes, date_added, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, 'warm_lead', ?, ?, ?)
    """, (
        data.get("business_name", ""),
        data.get("owner_name", ""),
        data.get("email", ""),
        data.get("phone", ""),
        data.get("city", ""),
        data.get("industry", ""),
        data.get("notes", ""),
        now, now,
    ))
    db.commit()
    lead_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    row = dict_row(db.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone())
    db.close()
    return jsonify(row), 201

# ─── API: Clients (CRUD) ─────────────────────────────────────────────────

@app.route("/api/clients")
def clients_list():
    db = get_db()
    rows = dict_rows(db.execute(
        "SELECT * FROM clients WHERE active = 1 ORDER BY start_date DESC"
    ).fetchall())
    total_mrr = sum(r.get("monthly_value", 0) or 0 for r in rows)
    db.close()
    return jsonify({"clients": rows, "total_mrr": total_mrr})

@app.route("/api/clients", methods=["POST"])
def add_client():
    db = get_db()
    data = request.json or {}
    now = datetime.utcnow().isoformat()
    db.execute("""
        INSERT INTO clients (lead_id, business_name, owner_name, email, phone, industry, city,
                             monthly_value, setup_fee, setup_fee_date, start_date, next_checkin, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("lead_id"),
        data.get("business_name", ""),
        data.get("owner_name", ""),
        data.get("email", ""),
        data.get("phone", ""),
        data.get("industry", ""),
        data.get("city", ""),
        data.get("monthly_value", 500),
        data.get("setup_fee", 0),
        data.get("setup_fee_date", date.today().isoformat()),
        data.get("start_date", date.today().isoformat()),
        data.get("next_checkin", (date.today() + timedelta(days=14)).isoformat()),
        data.get("notes", ""),
        now,
    ))
    db.commit()
    cid = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    row = dict_row(db.execute("SELECT * FROM clients WHERE id = ?", (cid,)).fetchone())
    db.close()
    return jsonify(row), 201

@app.route("/api/clients/<int:client_id>", methods=["PATCH"])
def update_client(client_id):
    db = get_db()
    data = request.json or {}
    allowed = {"business_name", "owner_name", "email", "phone", "monthly_value",
               "setup_fee", "next_checkin", "notes", "active"}
    sets = []
    params = []
    for k, v in data.items():
        if k in allowed:
            sets.append(f"{k} = ?")
            params.append(v)
    if not sets:
        return jsonify({"error": "nothing to update"}), 400
    params.append(client_id)
    db.execute(f"UPDATE clients SET {', '.join(sets)} WHERE id = ?", params)
    db.commit()
    row = dict_row(db.execute("SELECT * FROM clients WHERE id = ?", (client_id,)).fetchone())
    db.close()
    return jsonify(row)

# ─── API: Stats ──────────────────────────────────────────────────────────

@app.route("/api/stats")
def stats():
    db = get_db()
    today = date.today().isoformat()

    total = db.execute("SELECT COUNT(*) FROM leads WHERE bounced = 0").fetchone()[0]
    emails_today = db.execute(
        "SELECT COUNT(*) FROM send_log WHERE date(sent_at) = ? AND channel = 'email'", (today,)
    ).fetchone()[0]
    linkedin_today = db.execute(
        "SELECT COUNT(*) FROM send_log WHERE date(sent_at) = ? AND channel = 'linkedin'", (today,)
    ).fetchone()[0]
    instagram_today = db.execute(
        "SELECT COUNT(*) FROM send_log WHERE date(sent_at) = ? AND channel = 'instagram'", (today,)
    ).fetchone()[0]
    replies = db.execute("SELECT COUNT(*) FROM leads WHERE replied IS NOT NULL AND bounced = 0").fetchone()[0]
    demos = db.execute("SELECT COUNT(*) FROM leads WHERE demo_booked IS NOT NULL AND bounced = 0").fetchone()[0]
    hot_leads = db.execute(
        "SELECT COUNT(*) FROM leads WHERE status = 'interested' AND unsubscribed = 0 AND bounced = 0"
    ).fetchone()[0]
    closed = db.execute(
        "SELECT COUNT(*) FROM leads WHERE closed IS NOT NULL AND closed != '' AND closed != '0' AND bounced = 0"
    ).fetchone()[0]

    client_mrr = db.execute("SELECT COALESCE(SUM(monthly_value), 0) FROM clients WHERE active = 1").fetchone()[0]
    mrr = client_mrr if client_mrr > 0 else closed * 500

    industries = [r[0] for r in db.execute(
        "SELECT DISTINCT industry FROM leads WHERE industry IS NOT NULL AND industry != '' ORDER BY industry"
    ).fetchall()]
    cities = [r[0] for r in db.execute(
        "SELECT DISTINCT city FROM leads WHERE city IS NOT NULL AND city != '' ORDER BY city"
    ).fetchall()]

    db.close()
    return jsonify({
        "total_leads": total,
        "emails_today": emails_today,
        "linkedin_today": linkedin_today,
        "instagram_today": instagram_today,
        "replies": replies,
        "demos_booked": demos,
        "hot_leads": hot_leads,
        "clients_closed": closed,
        "mrr": mrr,
        "industries": industries,
        "cities": cities,
    })

# ─── API: Today Tab Data ─────────────────────────────────────────────────

@app.route("/api/today")
def today_data():
    db = get_db()
    today = date.today().isoformat()

    # DM counts for today
    dm_count = db.execute(
        "SELECT COUNT(*) FROM send_log WHERE date(sent_at) = ? AND channel = 'linkedin'", (today,)
    ).fetchone()[0]
    ig_count = db.execute(
        "SELECT COUNT(*) FROM send_log WHERE date(sent_at) = ? AND channel = 'instagram'", (today,)
    ).fetchone()[0]

    # 20 leads for Instagram/Facebook DM pitches (home service in Colorado)
    ig_leads = dict_rows(db.execute("""
        SELECT id, business_name, city, industry, owner_name
        FROM leads
        WHERE (instagram_sent IS NULL OR instagram_sent = '')
          AND status NOT IN ('bounced', 'lost', 'closed', 'not_interested')
          AND unsubscribed = 0
          AND business_name IS NOT NULL AND business_name != ''
          AND (
            LOWER(industry) LIKE '%hvac%'
            OR LOWER(industry) LIKE '%roofing%'
            OR LOWER(industry) LIKE '%roof%'
            OR LOWER(industry) LIKE '%contractor%'
            OR LOWER(industry) LIKE '%remodel%'
            OR LOWER(industry) LIKE '%plumb%'
            OR LOWER(industry) LIKE '%electric%'
            OR LOWER(industry) LIKE '%landscap%'
            OR LOWER(industry) LIKE '%painting%'
            OR LOWER(industry) LIKE '%handyman%'
            OR LOWER(industry) LIKE '%general contractor%'
            OR LOWER(industry) LIKE '%home service%'
            OR LOWER(industry) LIKE '%construction%'
          )
        ORDER BY RANDOM()
        LIMIT 20
    """).fetchall())

    # If not enough home-service leads, fill with any untouched leads from Colorado cities
    if len(ig_leads) < 20:
        existing_ids = [l['id'] for l in ig_leads]
        placeholders = ','.join('?' * len(existing_ids)) if existing_ids else '0'
        extra = dict_rows(db.execute(f"""
            SELECT id, business_name, city, industry, owner_name
            FROM leads
            WHERE (instagram_sent IS NULL OR instagram_sent = '')
              AND status NOT IN ('bounced', 'lost', 'closed', 'not_interested')
              AND unsubscribed = 0
              AND business_name IS NOT NULL AND business_name != ''
              AND id NOT IN ({placeholders})
            ORDER BY RANDOM()
            LIMIT ?
        """, existing_ids + [20 - len(ig_leads)]).fetchall())
        ig_leads.extend(extra)

    # 20 leads for LinkedIn DM pitches (not yet contacted on LinkedIn)
    pitch_leads = dict_rows(db.execute("""
        SELECT id, business_name, city, industry, owner_name
        FROM leads
        WHERE (linkedin_sent IS NULL OR linkedin_sent = '')
          AND status NOT IN ('bounced', 'lost', 'closed')
          AND unsubscribed = 0
          AND business_name IS NOT NULL AND business_name != ''
        ORDER BY RANDOM()
        LIMIT 20
    """).fetchall())

    # Hot leads (interested or replied)
    hot_leads = dict_rows(db.execute("""
        SELECT id, business_name, city, email, phone, owner_name, industry, website, notes
        FROM leads
        WHERE (status = 'interested' OR (replied IS NOT NULL AND replied != ''))
          AND unsubscribed = 0 AND bounced = 0
          AND (closed IS NULL OR closed = '' OR closed = '0')
        ORDER BY reply_date DESC LIMIT 20
    """).fetchall())

    # Demos booked
    demos = dict_rows(db.execute("""
        SELECT id, business_name, city, industry, owner_name, demo_date, website
        FROM leads
        WHERE demo_booked IS NOT NULL AND demo_booked != '' AND demo_booked != '0'
          AND (closed IS NULL OR closed = '' OR closed = '0')
          AND bounced = 0 AND unsubscribed = 0
        ORDER BY demo_date ASC LIMIT 20
    """).fetchall())

    db.close()
    return jsonify({
        "dm_count": dm_count,
        "ig_count": ig_count,
        "pitch_leads": pitch_leads,
        "ig_leads": ig_leads,
        "hot_leads": hot_leads,
        "demos": demos,
    })

# ─── API: Send Discord notification ──────────────────────────────────────

@app.route("/api/notify", methods=["POST"])
def notify():
    env = load_env()
    webhook = env.get("DISCORD_WEBHOOK")
    if not webhook:
        return jsonify({"error": "no webhook configured"}), 500
    data = request.json or {}
    msg = data.get("message", "CRM update")
    payload = json.dumps({"content": msg}).encode()
    req = urllib.request.Request(webhook, data=payload,
                                headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─── API: Billing ─────────────────────────────────────────────────────────

@app.route("/api/billing/dashboard")
def billing_dashboard():
    db = get_db()
    today = date.today()
    month_start = today.replace(day=1).isoformat()

    # Revenue this month (paid invoices)
    rev_invoices = db.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM invoices WHERE status = 'paid' AND paid_at >= ?",
        (month_start,)
    ).fetchone()[0]

    # Also count setup fees from clients table this month
    rev_setup = db.execute(
        "SELECT COALESCE(SUM(setup_fee), 0) FROM clients WHERE setup_fee_date >= ?",
        (month_start,)
    ).fetchone()[0]

    # MRR from active clients
    mrr = db.execute(
        "SELECT COALESCE(SUM(monthly_value), 0) FROM clients WHERE active = 1"
    ).fetchone()[0]

    total_revenue_month = rev_invoices + rev_setup

    # Outstanding (pending invoices)
    outstanding = db.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM invoices WHERE status IN ('pending', 'overdue')"
    ).fetchone()[0]
    outstanding_count = db.execute(
        "SELECT COUNT(*) FROM invoices WHERE status IN ('pending', 'overdue')"
    ).fetchone()[0]

    # Upcoming renewals (active clients)
    upcoming_renewals = dict_rows(db.execute("""
        SELECT c.id, c.business_name, c.owner_name, c.email, c.monthly_value, c.start_date
        FROM clients c WHERE c.active = 1
    """).fetchall())

    # Monthly revenue trend (last 6 months from invoices)
    months_data = []
    for i in range(5, -1, -1):
        m = today.month - i
        y = today.year
        while m <= 0:
            m += 12
            y -= 1
        m_start = f"{y}-{m:02d}-01"
        if m == 12:
            m_end = f"{y+1}-01-01"
        else:
            m_end = f"{y}-{m+1:02d}-01"
        rev = db.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM invoices WHERE status = 'paid' AND paid_at >= ? AND paid_at < ?",
            (m_start, m_end)
        ).fetchone()[0]
        months_data.append({"month": f"{y}-{m:02d}", "revenue": rev})

    db.close()
    return jsonify({
        "total_revenue_month": total_revenue_month,
        "mrr": mrr,
        "outstanding": outstanding,
        "outstanding_count": outstanding_count,
        "upcoming_renewals": upcoming_renewals[:10],
        "monthly_trend": months_data,
        "stripe_configured": bool(get_stripe_key()),
    })


@app.route("/api/billing/create-payment-link", methods=["POST"])
def create_payment_link():
    data = request.json or {}
    client_name = data.get("client_name", "")
    amount = float(data.get("amount", 0))
    description = data.get("description", "")
    client_email = data.get("client_email", "")
    inv_type = data.get("type", "custom")
    client_id = data.get("client_id")

    stripe_key = get_stripe_key()
    payment_url = None
    stripe_id = None

    if stripe_key:
        try:
            import stripe
            stripe.api_key = stripe_key
            link = stripe.PaymentLink.create(
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": description or f"Viora - {client_name}"},
                        "unit_amount": int(amount * 100),
                    },
                    "quantity": 1,
                }],
            )
            payment_url = link.url
            stripe_id = link.id
        except Exception as e:
            return jsonify({"error": f"Stripe error: {str(e)}", "stripe_configured": True}), 500
    else:
        payment_url = None

    # Save invoice to DB
    db = get_db()
    now = datetime.utcnow().isoformat()
    due = (date.today() + timedelta(days=7)).isoformat()
    db.execute("""
        INSERT INTO invoices (client_id, client_name, client_email, amount, description,
                              type, status, payment_link, stripe_payment_id, created_at, due_date)
        VALUES (?, ?, ?, ?, ?, ?, 'pending', ?, ?, ?, ?)
    """, (client_id, client_name, client_email, amount, description,
          inv_type, payment_url, stripe_id, now, due))
    db.commit()
    inv_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    invoice = dict_row(db.execute("SELECT * FROM invoices WHERE id = ?", (inv_id,)).fetchone())
    db.close()

    return jsonify({
        "invoice": invoice,
        "payment_url": payment_url,
        "stripe_configured": bool(stripe_key),
    })


@app.route("/api/billing/send-invoice", methods=["POST"])
def send_invoice():
    data = request.json or {}
    invoice_id = data.get("invoice_id")

    db = get_db()
    inv = dict_row(db.execute("SELECT * FROM invoices WHERE id = ?", (invoice_id,)).fetchone())
    db.close()

    if not inv:
        return jsonify({"error": "Invoice not found"}), 404
    if not inv.get("client_email"):
        return jsonify({"error": "No email address for this client"}), 400

    payment_section = ""
    if inv.get("payment_link"):
        payment_section = f'<p><a href="{inv["payment_link"]}" style="background:#7c3aed;color:white;padding:12px 24px;text-decoration:none;border-radius:6px;display:inline-block;margin:16px 0">Pay ${inv["amount"]:.2f} Now</a></p>'
    else:
        payment_section = f'<p><strong>Amount Due: ${inv["amount"]:.2f}</strong></p><p>Please contact us for payment arrangements.</p>'

    html_body = f"""
    <div style="font-family:sans-serif;max-width:600px;margin:0 auto">
        <h2 style="color:#7c3aed">Invoice from Viora</h2>
        <p>Hi {inv['client_name']},</p>
        <p>Here\'s your invoice for: <strong>{inv['description'] or 'Viora Services'}</strong></p>
        <table style="width:100%;border-collapse:collapse;margin:16px 0">
            <tr style="border-bottom:1px solid #eee"><td style="padding:8px">Description</td><td style="padding:8px;text-align:right">{inv['description'] or 'Viora Services'}</td></tr>
            <tr style="border-bottom:1px solid #eee"><td style="padding:8px">Amount</td><td style="padding:8px;text-align:right"><strong>${inv['amount']:.2f}</strong></td></tr>
            <tr><td style="padding:8px">Due Date</td><td style="padding:8px;text-align:right">{inv['due_date'] or 'Upon receipt'}</td></tr>
        </table>
        {payment_section}
        <p style="color:#666;font-size:12px">Thank you for your business!<br>\u2014 Viora AI</p>
    </div>
    """

    ok, msg = send_email_via_gmail(
        inv["client_email"],
        f"Invoice from Viora - ${inv['amount']:.2f}",
        html_body
    )

    if ok:
        return jsonify({"ok": True, "message": "Invoice sent"})
    else:
        return jsonify({"error": msg}), 500


@app.route("/api/billing/invoices")
def list_invoices():
    db = get_db()

    # Auto-update overdue invoices (pending + created more than 7 days ago)
    seven_ago = (date.today() - timedelta(days=7)).isoformat()
    db.execute("""
        UPDATE invoices SET status = 'overdue'
        WHERE status = 'pending' AND created_at <= ?
    """, (seven_ago,))
    db.commit()

    rows = dict_rows(db.execute(
        "SELECT * FROM invoices ORDER BY created_at DESC"
    ).fetchall())
    db.close()
    return jsonify({"invoices": rows})


@app.route("/api/billing/invoices/<int:inv_id>/pay", methods=["POST"])
def mark_invoice_paid(inv_id):
    db = get_db()
    now = datetime.utcnow().isoformat()
    db.execute("UPDATE invoices SET status = 'paid', paid_at = ? WHERE id = ?", (now, inv_id))
    db.commit()
    inv = dict_row(db.execute("SELECT * FROM invoices WHERE id = ?", (inv_id,)).fetchone())
    db.close()
    if not inv:
        return jsonify({"error": "not found"}), 404
    return jsonify(inv)


@app.route("/api/billing/invoices/<int:inv_id>", methods=["DELETE"])
def delete_invoice(inv_id):
    db = get_db()
    db.execute("DELETE FROM invoices WHERE id = ?", (inv_id,))
    db.commit()
    db.close()
    return jsonify({"ok": True})


# ─── AUTOMATION DATABASE ──────────────────────────────────────────────────

AUTOMATION_DB = {
    "ai_receptionist": {
        "name": "AI Receptionist",
        "trigger_keywords": ["phone", "call", "contact", "schedule", "book", "appointment", "consultation", "service"],
        "trigger_industries": ["med spa", "hvac", "law firm", "salon", "gym", "roofing", "auto repair", "cleaning service", "contractor", "other"],
        "roi_pitch": "Missing 30-40% of calls. At average $500 job, 5 missed calls/week = $10,000/month lost. Our AI answers 24/7 for $350/month = 2,757% ROI",
        "time_saved_low": 15, "time_saved_high": 20,
        "revenue_recovered_low": 5000, "revenue_recovered_high": 10000,
        "price": 350, "setup": 750, "difficulty": "Easy",
        "roi_low": 500, "roi_high": 2757,
    },
    "missed_call_textback": {
        "name": "Missed Call Text-Back",
        "trigger_keywords": ["phone", "call", "contact", "mobile", "text", "sms"],
        "trigger_industries": ["med spa", "hvac", "law firm", "salon", "gym", "roofing", "auto repair", "cleaning service", "contractor", "other"],
        "roi_pitch": "78% of customers buy from whoever responds first. Auto-text within 60 seconds captures leads before competitors. $100/month, pays for itself with 1 recovered lead.",
        "time_saved_low": 3, "time_saved_high": 5,
        "revenue_recovered_low": 1500, "revenue_recovered_high": 4000,
        "price": 100, "setup": 0, "difficulty": "Easy",
        "roi_low": 500, "roi_high": 1500,
    },
    "review_automation": {
        "name": "Review Automation",
        "trigger_keywords": ["review", "google", "yelp", "testimonial", "rating", "feedback", "local"],
        "trigger_industries": ["med spa", "hvac", "law firm", "salon", "gym", "roofing", "auto repair", "cleaning service", "contractor", "other"],
        "roi_pitch": "1 star increase on Google = 5-9% revenue increase. Automated requests get 3x more reviews. $150/month.",
        "time_saved_low": 2, "time_saved_high": 3,
        "revenue_recovered_low": 1000, "revenue_recovered_high": 3000,
        "price": 150, "setup": 0, "difficulty": "Easy",
        "roi_low": 200, "roi_high": 500,
    },
    "followup_sequences": {
        "name": "Follow-Up Sequences",
        "trigger_keywords": ["quote", "consultation", "estimate", "free", "contact", "lead", "inquiry", "form", "get started"],
        "trigger_industries": ["med spa", "hvac", "law firm", "salon", "gym", "roofing", "auto repair", "cleaning service", "contractor", "other"],
        "roi_pitch": "55% of sales happen after follow-up 5+. Automating 3-touch sequences recovers 20-30% of lost leads. $200/month.",
        "time_saved_low": 5, "time_saved_high": 8,
        "revenue_recovered_low": 2000, "revenue_recovered_high": 5000,
        "price": 200, "setup": 0, "difficulty": "Easy",
        "roi_low": 300, "roi_high": 600,
    },
    "appointment_reminders": {
        "name": "Appointment Reminders",
        "trigger_keywords": ["book", "appointment", "schedule", "reserve", "consultation", "calendar", "visit", "no-show"],
        "trigger_industries": ["med spa", "salon", "gym", "law firm", "auto repair", "contractor", "other"],
        "roi_pitch": "Reduces no-shows by 29%. For 100 appointments/month at $80 average = $2,300/month saved. $100/month addon.",
        "time_saved_low": 4, "time_saved_high": 6,
        "revenue_recovered_low": 1500, "revenue_recovered_high": 2300,
        "price": 100, "setup": 0, "difficulty": "Easy",
        "roi_low": 400, "roi_high": 800,
    },
}


def scrape_website(url):
    """Scrape a website and extract useful business info."""
    scraped = {
        "url": url, "title": "", "description": "", "services": [],
        "phone": "", "email": "", "location": "", "pricing_mentioned": False,
        "booking_system": "", "team_clues": "", "tech_stack": [],
        "full_text": "", "scrape_success": False,
    }
    if not HAS_SCRAPING:
        return scraped
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        resp = req_lib.get(url, headers=headers, timeout=10, allow_redirects=True)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        if soup.title:
            scraped["title"] = soup.title.string.strip() if soup.title.string else ""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            scraped["description"] = meta_desc["content"].strip()
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        full_text = soup.get_text(separator=" ", strip=True).lower()
        scraped["full_text"] = full_text[:5000]
        phone_patterns = re.findall(r'[\(]?\d{3}[\)\-\.\s]?\s?\d{3}[\-\.\s]?\d{4}', resp.text)
        if phone_patterns:
            scraped["phone"] = phone_patterns[0]
        email_patterns = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', resp.text)
        email_patterns = [e for e in email_patterns if not e.endswith(('.png', '.jpg', '.gif', '.svg'))]
        if email_patterns:
            scraped["email"] = email_patterns[0]
        address_tags = soup.find_all(string=re.compile(r'\d+\s+\w+\s+(st|street|ave|avenue|blvd|boulevard|rd|road|dr|drive|ln|lane|way|ct|court)', re.I))
        if address_tags:
            scraped["location"] = address_tags[0].strip()[:200]
        services = []
        for tag in soup.find_all(["h2", "h3", "h4", "li"]):
            text = tag.get_text(strip=True)
            if 3 < len(text) < 100:
                services.append(text)
        scraped["services"] = services[:15]
        if re.search(r'\$\d+|price|pricing|cost|fee|starting at|from \$', full_text):
            scraped["pricing_mentioned"] = True
        booking_kw = {"calendly": "Calendly", "acuity": "Acuity", "mindbody": "Mindbody",
            "vagaro": "Vagaro", "square appointments": "Square", "booksy": "Booksy",
            "book online": "Online Booking", "book now": "Online Booking", "schedule now": "Online Booking"}
        for kw, name in booking_kw.items():
            if kw in full_text:
                scraped["booking_system"] = name
                break
        tech_map = {"wordpress": "WordPress", "shopify": "Shopify", "wix": "Wix",
            "squarespace": "Squarespace", "webflow": "Webflow", "hubspot": "HubSpot",
            "mailchimp": "Mailchimp", "google tag manager": "GTM", "facebook pixel": "FB Pixel"}
        html_lower = resp.text.lower()
        for kw, name in tech_map.items():
            if kw in html_lower:
                scraped["tech_stack"].append(name)
        team_patterns = re.findall(r'(\d+)\s*(?:team members|staff|employees|professionals|experts|specialists)', full_text)
        if team_patterns:
            scraped["team_clues"] = f"~{team_patterns[0]} team members"
        elif any(w in full_text for w in ["our team", "meet the team", "meet our"]):
            scraped["team_clues"] = "Has team page (multi-person operation)"
        scraped["scrape_success"] = True
    except Exception as e:
        scraped["error"] = str(e)[:200]
    return scraped


def generate_recommendations(scraped_data, industry, business_name):
    """Generate automation recommendations based on scraped data and industry."""
    full_text = scraped_data.get("full_text", "").lower()
    services = " ".join(scraped_data.get("services", [])).lower()
    combined_text = full_text + " " + services + " " + industry.lower()
    recommendations = []
    for key, auto in AUTOMATION_DB.items():
        industry_match = any(ind in industry.lower() for ind in auto["trigger_industries"])
        if not industry_match:
            continue
        keyword_hits = [kw for kw in auto["trigger_keywords"] if kw in combined_text]
        force_include = key in ["ai_receptionist", "followup_automation", "review_automation"]
        if keyword_hits or force_include:
            why_reasons = []
            if scraped_data.get("scrape_success"):
                if key == "ai_receptionist":
                    if scraped_data.get("phone"):
                        why_reasons.append(f"Your phone number ({scraped_data['phone']}) is prominently displayed — you're clearly taking calls.")
                    if scraped_data.get("booking_system"):
                        why_reasons.append(f"You use {scraped_data['booking_system']} for booking, but an AI receptionist captures calls that never make it to online booking.")
                    else:
                        why_reasons.append("No online booking system detected — most leads are calling in, and every missed call is lost revenue.")
                elif key == "followup_automation":
                    if "contact" in combined_text or "form" in combined_text:
                        why_reasons.append("Your site has contact forms — leads who fill these need rapid follow-up or they go to competitors.")
                    if scraped_data.get("services"):
                        why_reasons.append(f"With {len(scraped_data['services'])}+ services listed, varied inquiries need personalized follow-up sequences.")
                elif key == "review_automation":
                    why_reasons.append(f"{business_name} is a local business — Google reviews directly impact your search ranking and customer trust.")
                elif key == "appointment_booking":
                    if scraped_data.get("booking_system"):
                        why_reasons.append(f"You use {scraped_data['booking_system']} — an AI booking bot can handle scheduling conversations and reduce no-shows.")
                    else:
                        why_reasons.append("No online booking detected — an AI bot can handle scheduling 24/7 without staff.")
                elif key == "lead_qualification":
                    if any(t in combined_text for t in ["facebook", "google ads", "ppc", "advertising"]):
                        why_reasons.append("We detected paid advertising signals — an AI qualifier ensures ad spend isn't wasted on unqualified leads.")
                    else:
                        why_reasons.append("Qualifying inbound leads manually takes significant time — AI pre-qualifies 24/7 and routes hot leads instantly.")
            if not why_reasons:
                why_reasons.append(auto["roi_pitch"])
            avg_revenue = (auto["revenue_recovered_low"] + auto["revenue_recovered_high"]) / 2
            price = auto["price"]
            roi_pct = round((avg_revenue / max(price, 1)) * 100) if price > 0 else 0
            rec = {
                "key": key, "name": auto["name"],
                "why": " ".join(why_reasons), "roi_pitch": auto["roi_pitch"],
                "time_saved": f"{auto['time_saved_low']}-{auto['time_saved_high']} hrs/week",
                "time_saved_low": auto["time_saved_low"], "time_saved_high": auto["time_saved_high"],
                "revenue_recovered": f"${auto['revenue_recovered_low']:,}-${auto['revenue_recovered_high']:,}/mo",
                "revenue_recovered_low": auto["revenue_recovered_low"],
                "revenue_recovered_high": auto["revenue_recovered_high"],
                "avg_revenue": avg_revenue, "price": price,
                "price_display": f"${price}/mo" if price > 0 else (auto.get("price_note", "Included")),
                "setup": auto.get("setup", 0), "difficulty": auto["difficulty"],
                "roi_pct": roi_pct, "roi_range": f"{auto['roi_low']}-{auto['roi_high']}%",
            }
            recommendations.append(rec)
    recommendations.sort(key=lambda r: r["roi_pct"], reverse=True)
    return recommendations[:5]


@app.route("/api/audit/generate", methods=["POST"])
def audit_generate():
    data = request.json or {}
    url = data.get("url", "").strip()
    business_name = data.get("business_name", "").strip()
    industry = data.get("industry", "other").strip()
    if not business_name:
        return jsonify({"error": "business_name is required"}), 400
    if url and not url.startswith(("http://", "https://")):
        url = "https://" + url
    scraped = scrape_website(url) if url else {
        "url": url, "scrape_success": False, "title": "", "description": "",
        "services": [], "phone": "", "email": "", "location": "",
        "pricing_mentioned": False, "booking_system": "", "team_clues": "",
        "tech_stack": [], "full_text": "",
    }
    recommendations = generate_recommendations(scraped, industry, business_name)
    total_monthly_cost = sum(r["price"] for r in recommendations)
    total_revenue_recovered = sum(r["avg_revenue"] for r in recommendations)
    total_time_saved = sum((r["time_saved_low"] + r["time_saved_high"]) / 2 for r in recommendations)
    total_roi = round((total_revenue_recovered / max(total_monthly_cost, 1)) * 100) if total_monthly_cost > 0 else 0
    lead_id = None
    try:
        db = get_db()
        lead = db.execute("SELECT id FROM leads WHERE business_name LIKE ? LIMIT 1", (f"%{business_name}%",)).fetchone()
        if lead:
            lead_id = lead[0]
        db.close()
    except:
        pass
    scraped_store = {k: v for k, v in scraped.items() if k != "full_text"}
    return jsonify({
        "business_name": business_name, "website": url, "industry": industry,
        "scraped_data": scraped_store, "recommendations": recommendations,
        "total_monthly_cost": total_monthly_cost,
        "total_revenue_recovered": total_revenue_recovered,
        "total_time_saved": round(total_time_saved),
        "total_roi_estimate": total_roi, "lead_id": lead_id,
    })


@app.route("/api/audit/save", methods=["POST"])
def audit_save():
    data = request.json or {}
    db = get_db()
    now = datetime.utcnow().isoformat()
    db.execute("""
        INSERT INTO audit_reports (business_name, website, industry, scraped_data,
                                    recommendations, total_roi_estimate, created_at, lead_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("business_name", ""), data.get("website", ""),
        data.get("industry", ""), json.dumps(data.get("scraped_data", {})),
        json.dumps(data.get("recommendations", [])),
        data.get("total_roi_estimate", 0), now, data.get("lead_id"),
    ))
    db.commit()
    report_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    db.close()
    return jsonify({"ok": True, "id": report_id})


@app.route("/api/audit/reports")
def audit_reports_list():
    db = get_db()
    rows = dict_rows(db.execute("SELECT * FROM audit_reports ORDER BY created_at DESC LIMIT 50").fetchall())
    db.close()
    for r in rows:
        try:
            r["scraped_data"] = json.loads(r.get("scraped_data") or "{}")
        except:
            r["scraped_data"] = {}
        try:
            r["recommendations"] = json.loads(r.get("recommendations") or "[]")
        except:
            r["recommendations"] = []
    return jsonify({"reports": rows})


@app.route("/api/audit/reports/<int:report_id>", methods=["DELETE"])
def audit_report_delete(report_id):
    db = get_db()
    db.execute("DELETE FROM audit_reports WHERE id = ?", (report_id,))
    db.commit()
    db.close()
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=False)
