import sqlite3
from datetime import datetime, timedelta, timezone
import re
from pathlib import Path

DB_PATH = Path(r'C:\Users\JESUS TE AMA\.openclaw\state\control_tower.db')
LOCAL_TZ = timezone(timedelta(hours=-3))
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")
NEW_STATUS = "novo"
ALLOWED_NEW_TYPES = {"whatsapp_intro", "follow-up"}
BLOCKED_STATUSES = {"fechado", "cancelado", "optout", "opt-out", "invalid_contact"}

def parse_local(value):
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        try:
            parsed = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=LOCAL_TZ)
    return parsed.astimezone(LOCAL_TZ)

def valid_whatsapp(value):
    return bool(value and PHONE_REGEX.match(value.strip()))

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
now_local = datetime.now(LOCAL_TZ)
cur.execute("SELECT lead_id, status_funil, whatsapp, proxima_acao_em, proxima_acao_tipo FROM entities_leads")
should_send = []
for lead_id, status, whatsapp, prox, tipo in cur.fetchall():
    status_key = (status or "").strip().lower()
    if status_key != NEW_STATUS:
        continue
    tipo_key = (tipo or "").strip().lower()
    if tipo_key not in ALLOWED_NEW_TYPES:
        continue
    proxima_dt = parse_local(prox)
    if proxima_dt is None or proxima_dt > now_local:
        continue
    if not valid_whatsapp(whatsapp):
        continue
    if status_key in BLOCKED_STATUSES:
        continue
    should_send.append(lead_id)
print('now', now_local)
print('should send', len(should_send))
for lead_id in should_send[:5]:
    print(lead_id)
cur.close()
