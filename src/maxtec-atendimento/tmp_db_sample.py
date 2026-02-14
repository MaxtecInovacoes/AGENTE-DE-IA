import sqlite3
from pathlib import Path
conn = sqlite3.connect(Path(r'C:\Users\JESUS TE AMA\.openclaw\state\control_tower.db'))
cur = conn.cursor()
cur.execute('SELECT lead_id, status_funil, proxima_acao_em, whatsapp, engaged_at, funnel_stage FROM entities_leads LIMIT 10')
rows = cur.fetchall()
print('sample', len(rows))
for row in rows:
    print(row)
conn.close()
