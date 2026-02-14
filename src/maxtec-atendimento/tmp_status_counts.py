import sqlite3
from pathlib import Path

conn = sqlite3.connect(Path(r'C:\Users\JESUS TE AMA\.openclaw\state\control_tower.db'))
cur = conn.cursor()
cur.execute('SELECT status_funil, COUNT(*) FROM entities_leads GROUP BY status_funil')
for row in cur.fetchall():
    print(row)
conn.close()
