import sqlite3
from pathlib import Path

conn = sqlite3.connect(Path(r'C:\Users\JESUS TE AMA\.openclaw\state\control_tower.db'))
cur = conn.cursor()
cur.execute('SELECT event_id, timestamp, entity_type, acao, resumo FROM events_log ORDER BY timestamp')
rows = cur.fetchall()
print('events', len(rows))
for row in rows:
    print(row)
conn.close()
