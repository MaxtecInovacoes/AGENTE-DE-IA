import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path

LOCAL_TZ = timezone(timedelta(hours=-3))
conn = sqlite3.connect(Path(r'C:\Users\JESUS TE AMA\.openclaw\state\control_tower.db'))
cur = conn.cursor()
cur.execute("SELECT proxima_acao_em FROM entities_leads WHERE status_funil = 'novo'")
values = [row[0] for row in cur.fetchall() if row[0]]
print('count', len(values))
print('min', min(values[:10]))
cur.close()
