import sqlite3
from pathlib import Path
conn=sqlite3.connect(Path(r'C:\Users\JESUS TE AMA\.openclaw\state\control_tower.db'))
cur=conn.cursor()
cur.execute("SELECT COUNT(*) FROM events_log WHERE acao='whatsapp_send'")
count=cur.fetchone()[0]
print('whatsapp_send events',count)
cur.execute("SELECT entity_id,resumo FROM events_log WHERE acao='whatsapp_send' ORDER BY timestamp DESC LIMIT 5")
for row in cur.fetchall():
    print(row)
conn.close()
