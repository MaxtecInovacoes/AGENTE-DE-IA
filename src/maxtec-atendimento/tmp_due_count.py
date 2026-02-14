import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

LOCAL_TZ = timezone(timedelta(hours=-3))

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

conn = sqlite3.connect(Path(r'C:\Users\JESUS TE AMA\.openclaw\state\control_tower.db'))
cur = conn.cursor()
now = datetime.now(LOCAL_TZ)
cur.execute('SELECT count(*) FROM entities_leads WHERE status_funil = "novo"')
total = cur.fetchone()[0]
cur.execute('SELECT proxima_acao_em FROM entities_leads WHERE status_funil = "novo"')
count_due = 0
for (value,) in cur.fetchall():
    dt = parse_local(value)
    if not dt:
        continue
    if dt <= now:
        count_due += 1
print('now', now)
print('total novo', total)
print('due', count_due)
conn.close()
