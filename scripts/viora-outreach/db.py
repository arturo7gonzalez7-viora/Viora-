#!/usr/bin/env python3
"""
VIORA OUTREACH — SQLite CRM Database
Replaces fragile CSV files with a proper database.
Handles deduplication, status tracking, and sequence state.
"""

import sqlite3
import csv
from datetime import datetime
from pathlib import Path
from config import DB_PATH

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    """Create tables if they don't exist."""
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS leads (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        business_name   TEXT NOT NULL,
        address         TEXT,
        phone           TEXT,
        website         TEXT,
        email           TEXT,
        email_confidence TEXT,
        owner_name      TEXT,
        rating          REAL,
        total_reviews   INTEGER DEFAULT 0,
        place_id        TEXT UNIQUE,
        industry        TEXT,
        city            TEXT,
        status          TEXT DEFAULT 'new',
        -- Sequence tracking
        email_1_sent    TEXT,
        email_2_sent    TEXT,
        email_3_sent    TEXT,
        linkedin_sent   TEXT,
        replied         TEXT,
        reply_date      TEXT,
        demo_booked     TEXT,
        demo_date       TEXT,
        closed          TEXT,
        closed_date     TEXT,
        unsubscribed    INTEGER DEFAULT 0,
        bounced         INTEGER DEFAULT 0,
        notes           TEXT,
        date_added      TEXT,
        last_updated    TEXT,
        -- Dedup key
        UNIQUE(phone, business_name)
    );

    CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
    CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email);
    CREATE INDEX IF NOT EXISTS idx_leads_city ON leads(city);
    CREATE INDEX IF NOT EXISTS idx_leads_industry ON leads(industry);

    CREATE TABLE IF NOT EXISTS send_log (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        lead_id     INTEGER REFERENCES leads(id),
        email_to    TEXT,
        subject     TEXT,
        seq_num     INTEGER,
        channel     TEXT DEFAULT 'email',
        sent_at     TEXT,
        status      TEXT DEFAULT 'sent'
    );

    CREATE TABLE IF NOT EXISTS daily_stats (
        date            TEXT PRIMARY KEY,
        emails_sent     INTEGER DEFAULT 0,
        linkedin_sent   INTEGER DEFAULT 0,
        leads_scraped   INTEGER DEFAULT 0,
        emails_found    INTEGER DEFAULT 0,
        replies         INTEGER DEFAULT 0,
        demos_booked    INTEGER DEFAULT 0,
        deals_closed    INTEGER DEFAULT 0
    );
    """)
    conn.commit()
    conn.close()

def upsert_lead(lead_dict):
    """Insert or skip a lead (dedup by place_id or phone+name)."""
    conn = get_conn()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lead_dict["date_added"] = lead_dict.get("date_added", now)
    lead_dict["last_updated"] = now

    try:
        conn.execute("""
            INSERT OR IGNORE INTO leads
            (business_name, address, phone, website, email, owner_name,
             rating, total_reviews, place_id, industry, city, status,
             date_added, last_updated)
            VALUES
            (:business_name, :address, :phone, :website, :email, :owner_name,
             :rating, :total_reviews, :place_id, :industry, :city, 'new',
             :date_added, :last_updated)
        """, {
            "business_name": lead_dict.get("business_name", ""),
            "address":       lead_dict.get("address", ""),
            "phone":         lead_dict.get("phone", ""),
            "website":       lead_dict.get("website", ""),
            "email":         lead_dict.get("email", ""),
            "owner_name":    lead_dict.get("owner_name", ""),
            "rating":        lead_dict.get("rating", None),
            "total_reviews": lead_dict.get("total_reviews", 0),
            "place_id":      lead_dict.get("place_id", ""),
            "industry":      lead_dict.get("industry", ""),
            "city":          lead_dict.get("city", ""),
            "date_added":    lead_dict["date_added"],
            "last_updated":  lead_dict["last_updated"],
        })
        conn.commit()
        inserted = conn.total_changes
    except sqlite3.IntegrityError:
        inserted = 0
    finally:
        conn.close()
    return inserted

def bulk_upsert_leads(leads_list):
    """Batch insert leads, skip duplicates. Returns count of new leads."""
    conn = get_conn()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    inserted = 0
    for lead in leads_list:
        try:
            cursor = conn.execute("""
                INSERT OR IGNORE INTO leads
                (business_name, address, phone, website, email, owner_name,
                 rating, total_reviews, place_id, industry, city, status,
                 date_added, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'new', ?, ?)
            """, (
                lead.get("business_name", ""),
                lead.get("address", ""),
                lead.get("phone", ""),
                lead.get("website", ""),
                lead.get("email", ""),
                lead.get("owner_name", ""),
                lead.get("rating", None),
                lead.get("total_reviews", 0),
                lead.get("place_id", ""),
                lead.get("industry", ""),
                lead.get("city", ""),
                now, now,
            ))
            # rowcount is 0 for INSERT OR IGNORE that was ignored (duplicate)
            if cursor.rowcount > 0:
                inserted += 1
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    conn.close()
    return inserted

def get_leads_needing_emails():
    """Get leads that have an email but haven't finished the sequence."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT * FROM leads
        WHERE email IS NOT NULL AND email != ''
          AND unsubscribed = 0
          AND bounced = 0
          AND status NOT IN ('closed', 'not_interested', 'sequence_complete')
          AND (
              email_1_sent IS NULL
              OR (email_2_sent IS NULL AND email_1_sent IS NOT NULL
                  AND julianday('now') - julianday(email_1_sent) >= 3
                  AND (replied IS NULL OR replied = ''))
              OR (email_3_sent IS NULL AND email_2_sent IS NOT NULL
                  AND julianday('now') - julianday(email_2_sent) >= 4
                  AND (replied IS NULL OR replied = ''))
          )
        ORDER BY
            CASE WHEN email_1_sent IS NULL THEN 0
                 WHEN email_2_sent IS NULL THEN 1
                 ELSE 2 END,
            date_added ASC
    """).fetchall()
    conn.close()
    return rows

def get_leads_needing_email_lookup():
    """Get leads with a website but no email."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT * FROM leads
        WHERE (email IS NULL OR email = '')
          AND website IS NOT NULL AND website != ''
          AND status = 'new'
        ORDER BY date_added ASC
    """).fetchall()
    conn.close()
    return rows

def get_leads_for_linkedin():
    """Get leads not yet contacted on LinkedIn."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT * FROM leads
        WHERE linkedin_sent IS NULL
          AND unsubscribed = 0
          AND status NOT IN ('closed', 'not_interested')
        ORDER BY
            CASE WHEN email IS NOT NULL AND email != '' THEN 0 ELSE 1 END,
            date_added ASC
    """).fetchall()
    conn.close()
    return rows

def update_lead(lead_id, **kwargs):
    """Update specific fields on a lead."""
    conn = get_conn()
    kwargs["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sets = ", ".join(f"{k} = ?" for k in kwargs)
    vals = list(kwargs.values()) + [lead_id]
    conn.execute(f"UPDATE leads SET {sets} WHERE id = ?", vals)
    conn.commit()
    conn.close()

def log_send(lead_id, email_to, subject, seq_num, channel="email"):
    """Log an outbound message."""
    conn = get_conn()
    conn.execute("""
        INSERT INTO send_log (lead_id, email_to, subject, seq_num, channel, sent_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (lead_id, email_to, subject, seq_num, channel,
          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_stats(date_str=None):
    """Get stats for a given date (default: today)."""
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    conn = get_conn()

    stats = {
        "date": date_str,
        "total_leads": conn.execute("SELECT COUNT(*) FROM leads").fetchone()[0],
        "leads_with_email": conn.execute(
            "SELECT COUNT(*) FROM leads WHERE email IS NOT NULL AND email != ''").fetchone()[0],
        "emails_sent_today": conn.execute(
            "SELECT COUNT(*) FROM send_log WHERE channel='email' AND sent_at LIKE ?",
            (f"{date_str}%",)).fetchone()[0],
        "linkedin_sent_today": conn.execute(
            "SELECT COUNT(*) FROM send_log WHERE channel='linkedin' AND sent_at LIKE ?",
            (f"{date_str}%",)).fetchone()[0],
        "total_email_1": conn.execute(
            "SELECT COUNT(*) FROM leads WHERE email_1_sent IS NOT NULL").fetchone()[0],
        "total_email_2": conn.execute(
            "SELECT COUNT(*) FROM leads WHERE email_2_sent IS NOT NULL").fetchone()[0],
        "total_email_3": conn.execute(
            "SELECT COUNT(*) FROM leads WHERE email_3_sent IS NOT NULL").fetchone()[0],
        "total_replied": conn.execute(
            "SELECT COUNT(*) FROM leads WHERE replied IS NOT NULL AND replied != ''").fetchone()[0],
        "total_demos": conn.execute(
            "SELECT COUNT(*) FROM leads WHERE demo_booked IS NOT NULL").fetchone()[0],
        "total_closed": conn.execute(
            "SELECT COUNT(*) FROM leads WHERE status = 'closed'").fetchone()[0],
        "total_unsubscribed": conn.execute(
            "SELECT COUNT(*) FROM leads WHERE unsubscribed = 1").fetchone()[0],
        "total_bounced": conn.execute(
            "SELECT COUNT(*) FROM leads WHERE bounced = 1").fetchone()[0],
        "sequence_complete": conn.execute(
            "SELECT COUNT(*) FROM leads WHERE status = 'sequence_complete'").fetchone()[0],
        "in_sequence": conn.execute(
            "SELECT COUNT(*) FROM leads WHERE email_1_sent IS NOT NULL AND status = 'contacted'").fetchone()[0],
    }
    conn.close()
    return stats

def import_csv(csv_path):
    """Import leads from an existing CSV file into the database."""
    path = Path(csv_path)
    if not path.exists():
        print(f"❌ CSV not found: {csv_path}")
        return 0

    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    imported = 0
    for row in rows:
        try:
            upsert_lead(row)
            imported += 1
        except Exception:
            pass
    print(f"✅ Imported {imported}/{len(rows)} leads from {path.name}")
    return imported

# Initialize on import
init_db()
