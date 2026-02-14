import os
from pathlib import Path
import requests
from datetime import datetime, timezone

env_path = Path('.').resolve() / '.env'
with env_path.open() as handle:
    for line in handle:
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip())
MATON_API_KEY = os.environ['MATON_API_KEY']
spreadsheet_id = '1Basl2MvOHd0TvA-8yVwRmDnJMNeHSV7ICRvHQ8x_CDA'
url = f'https://gateway.maton.ai/google-sheets/v4/spreadsheets/{spreadsheet_id}/values/entities_leads'
headers = {'Authorization': f'Bearer {MATON_API_KEY}', 'Content-Type': 'application/json'}
resp = requests.get(url, headers=headers, params={'majorDimension': 'ROWS'})
resp.raise_for_status()
values = resp.json().get('values', [])
if not values:
    raise SystemExit('empty sheet')
headers_row = values[0]
rows = values[1:]
now = datetime.now(timezone.utc)

def parse_iso(value):
    if value.endswith('Z'):
        value = value[:-1] + '+00:00'
    return datetime.fromisoformat(value).astimezone(timezone.utc)

due = []
for row in rows:
    lead = dict(zip(headers_row, row))
    proxima = lead.get('proxima_acao_em')
    if not proxima:
        continue
    try:
        dt = parse_iso(proxima)
    except Exception as exc:
        continue
    status = lead.get('status_funil','').strip().lower()
    role = lead.get('lead_id')
    if dt <= now or status == 'novo':
        due.append((role, lead.get('nome'), proxima, status))

print('now UTC', now.isoformat())
print('due leads', len(due))
for item in due[:5]:
    print(item)
