import sqlite3
from pathlib import Path
conn=sqlite3.connect(Path(r'C:\Users\JESUS TE AMA\.openclaw\state\control_tower.db'))
cur=conn.cursor()
cur.execute("SELECT COUNT(*) FROM events_log WHERE acao='followup_send' AND entity_id='L-1ST-SEND'")
count=cur.fetchone()[0]
print('followup_send L-1ST-SEND',count)
cur.execute("SELECT COUNT(*) FROM events_log WHERE acao='whatsapp_send' AND entity_id='L-1ST-SEND'")
count2=cur.fetchone()[0]
print('whatsapp_send L-1ST-SEND',count2)
conn.close()
