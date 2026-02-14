import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re

DB_PATH = Path(r'C:\Users\JESUS TE AMA\.openclaw\state\control_tower.db')
LOCAL_TZ = timezone(timedelta(hours=-3))
PHONE_REGEX = re.compile(r'^\+\d{10,15}$')
NEW_STATUS = 'novo'
ALLOWED_NEW_TYPES = {'whatsapp_intro', 'follow-up'}
BLOCKED_STATUSES = {'fechado', 'cancelado', 'optout', 'opt-out', 'invalid_contact'}

def parse_local(value):
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        try:
            parsed = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=LOCAL_TZ)
    return parsed.astimezone(LOCAL_TZ)

def is_valid_whatsapp(value):
    return bool(value and PHONE_REGEX.match(value.strip()))

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute('SELECT lead_id, status_funil, whatsapp, proxima_acao_em, proxima_acao_tipo FROM entities_leads WHERE status_funil = "novo" ORDER BY lead_id ASC LIMIT 5')
now_local = datetime.now(LOCAL_TZ)
for row in cur.fetchall():
    lead_id, status, whatsapp, prox, tipo = row
    status_key = (status or '').strip().lower()
    tipo_key = (tipo or '').strip().lower()
    proxima_dt = parse_local(prox)
    has_whatsapp = is_valid_whatsapp(whatsapp)
    should_send = (
        status_key == NEW_STATUS
        and tipo_key in ALLOWED_NEW_TYPES
        and proxima_dt is not None
        and proxima_dt <= now_local
        and has_whatsapp
        and status_key not in BLOCKED_STATUSES
    )
    print(lead_id, whatsapp, tipo, proxima_dt, has_whatsapp, tipo_key in ALLOWED_NEW_TYPES, proxima_dt <= now_local if proxima_dt else None, should_send)
conn.close()
