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
headers_row = values[0]
rows = values[1:]
print('total', len(rows))
ingored = []
data = []
for row in rows:
    lead = dict(zip(headers_row, row))
    proxima = lead.get('proxima_acao_em')
    if not proxima:
        continue
    data.append((lead['lead_id'], lead['nome'], proxima))

data.sort(key=lambda x: x[2])
for item in data[:10]:
    print(item)
print('earliest', data[0][2] if data else None)
