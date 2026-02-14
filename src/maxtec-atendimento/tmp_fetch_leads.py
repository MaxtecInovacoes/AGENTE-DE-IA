import os
from pathlib import Path
import requests

env_path = Path('.').resolve() / '.env'
if not env_path.exists():
    raise SystemExit('.env missing')
with env_path.open() as handle:
    for line in handle:
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip())

MATON_API_KEY = os.environ.get('MATON_API_KEY')
if not MATON_API_KEY:
    raise SystemExit('MATON_API_KEY missing')
spreadsheet_id = '1Basl2MvOHd0TvA-8yVwRmDnJMNeHSV7ICRvHQ8x_CDA'
headers = {
    'Authorization': f'Bearer {MATON_API_KEY}',
    'Content-Type': 'application/json',
}
url = f'https://gateway.maton.ai/google-sheets/v4/spreadsheets/{spreadsheet_id}/values/entities_leads'
resp = requests.get(url, headers=headers, params={'majorDimension': 'ROWS'})
resp.raise_for_status()
data = resp.json()
values = data.get('values') or []
print('values', len(values))
for row in values[:5]:
    print(row)
