import sqlite3
from pathlib import Path
conn = sqlite3.connect(Path(r'C:\Users\JESUS TE AMA\.openclaw\state\control_tower.db'))
cur = conn.cursor()
cur.execute("SELECT lead_id, status_funil, whatsapp, proxima_acao_em, proxima_acao_tipo FROM entities_leads WHERE lead_id = 'l:1815208865850778'")
row = cur.fetchone()
print(row)
conn.close()
