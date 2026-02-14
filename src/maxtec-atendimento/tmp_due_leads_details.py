import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re

LOCAL_TZ = timezone(timedelta(hours=-3))
PHONE_REGEX = re.compile(r'^\+\d{10,15}$')
ALLOWED_TYPES = {'whatsapp_intro','follow-up'}

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

def valid_whatsapp(value):
    return bool(value and PHONE_REGEX.match(value.strip()))

conn = sqlite3.connect(Path(r'C:\Users\JESUS TE AMA\.openclaw\state\control_tower.db'))
cur = conn.cursor()
now = datetime.now(LOCAL_TZ)
cur.execute('SELECT lead_id, whatsapp, proxima_acao_em, proxima_acao_tipo FROM entities_leads WHERE status_funil = "novo"')
count=0
for lead_id, whatsapp, proxima, tipo in cur.fetchall():
    proxima_dt = parse_local(proxima)
    if not proxima_dt:
        continue
    if proxima_dt <= now:
        count += 1
        print(lead_id, whatsapp, tipo, proxima_dt, valid_whatsapp(whatsapp), tipo and tipo.strip().lower() in ALLOWED_TYPES)
        if count >= 10:
            break
print('due count', count)
conn.close()
