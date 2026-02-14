import sqlite3
from pathlib import Path

db_path = Path(r'C:\Users\JESUS TE AMA\.openclaw\state\control_tower.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute('SELECT lead_id, nome, status_funil, proxima_acao_em, ultima_msg_em FROM entities_leads ORDER BY lead_id')
rows = cur.fetchall()
print('total leads', len(rows))
for row in rows[:20]:
    print(row)
conn.close()
