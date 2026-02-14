import os
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path

env_path = Path('.').resolve() / '.env'
if not env_path.exists():
    raise SystemExit('.env missing')
with env_path.open('r', encoding='utf-8') as f:
    for line in f:
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
base_url = f'https://gateway.maton.ai/google-sheets/v4/spreadsheets/{spreadsheet_id}/values'

def read_tab(tab):
    resp = requests.get(f'{base_url}/{tab}', headers=headers, params={'majorDimension': 'ROWS'})
    resp.raise_for_status()
    return resp.json()

def column_letter(idx):
    letters = []
    while idx > 0:
        idx, rem = divmod(idx - 1, 26)
        letters.append(chr(65 + rem))
    return ''.join(reversed(letters)) or 'A'

def update_row(tab, range_name, values):
    resp = requests.put(f'{base_url}/{tab}!{range_name}', headers=headers, params={'valueInputOption': 'USER_ENTERED'}, json={'values': values})
    resp.raise_for_status()
    return resp.json()

now_local = datetime.now(timezone(timedelta(hours=-3)))
proxima = (now_local - timedelta(seconds=30)).isoformat(timespec='seconds')
created = (now_local - timedelta(minutes=5)).isoformat(timespec='seconds')
headers_row = read_tab('entities_leads').get('values', [])[0]
row_template = {name: '' for name in headers_row}
row_template.update({
    'lead_id': 'L-1ST-SEND',
    'nome': 'Lead Primeiro',
    'whatsapp': '+554185134105',
    'origem': 'fb',
    'nicho': 'solar',
    'status_funil': 'novo',
    'created_at': created,
    'ultima_msg_em': created,
    'ultima_acao': 'followup_ready',
    'proxima_acao_em': proxima,
    'proxima_acao_tipo': 'whatsapp_intro',
    'responsavel_worker': 'automation_core',
    'valor_estimado': '0',
    'observacoes': 'teste manual',
})
end_col = column_letter(len(headers_row))
row_values = [[row_template.get(col, '') for col in headers_row]]
print('updating first lead row with', row_template)
update_row('entities_leads', f'A2:{end_col}2', row_values)
print('updated row 2 (first lead)')
