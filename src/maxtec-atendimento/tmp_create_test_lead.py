import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

DB_PATH = Path(r'C:\Users\JESUS TE AMA\.openclaw\state\control_tower.db')
LOCAL_TZ = timezone(timedelta(hours=-3))

def format_local(dt: datetime) -> str:
    return dt.astimezone(LOCAL_TZ).strftime('%Y-%m-%d %H:%M:%S')

now = datetime.now(LOCAL_TZ)
proxima = now - timedelta(minutes=1)
created = now - timedelta(minutes=5)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute('''INSERT OR REPLACE INTO entities_leads
    (lead_id, nome, whatsapp, nicho, status_funil, ultima_msg_em, ultima_acao, proxima_acao_em,
     valor_estimado, observacoes, origem, created_at, proxima_acao_tipo, responsavel_worker,
     engaged_at, funnel_stage)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    'L-TEST-DISPARO-001',
    'Teste Disparo',
    '+554185134105',
    'solar',
    'novo',
    format_local(now - timedelta(minutes=2)),
    '',
    format_local(proxima),
    0,
    'teste para disparo',
    'fb',
    format_local(created),
    'whatsapp_intro',
    'automation_core',
    '',
    '',
))
conn.commit()
conn.close()
print('lead L-TEST-DISPARO-001 inserido com proxima_acao_em', format_local(proxima))
