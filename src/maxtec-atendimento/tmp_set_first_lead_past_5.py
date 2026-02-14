import os
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path

env_path = Path('.').resolve() / '.env'
with env_path.open() as handle:
    for line in handle:
        line=line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key,value=line.split('=',1)
        os.environ.setdefault(key.strip(), value.strip())
MATON_API_KEY=os.environ['MATON_API_KEY']
spreadsheet_id='1Basl2MvOHd0TvA-8yVwRmDnJMNeHSV7ICRvHQ8x_CDA'
headers={'Authorization':f'Bearer {MATON_API_KEY}','Content-Type':'application/json'}
base_url=f'https://gateway.maton.ai/google-sheets/v4/spreadsheets/{spreadsheet_id}/values'

def column_letter(idx):
    letters=[]
    while idx>0:
        idx,rem=divmod(idx-1,26)
        letters.append(chr(65+rem))
    return ''.join(reversed(letters)) or 'A'

def read_tab(tab):
    resp=requests.get(f'{base_url}/{tab}', headers=headers, params={'majorDimension':'ROWS'})
    resp.raise_for_status()
    return resp.json()

def update(tab, range_name, values):
    resp=requests.put(f'{base_url}/{tab}!{range_name}', headers=headers, params={'valueInputOption':'USER_ENTERED'}, json={'values':values})
    resp.raise_for_status()
    return resp.json()

now=datetime.now(timezone(timedelta(hours=-3)))
past=(now - timedelta(minutes=5)).isoformat(timespec='seconds')
created=now.isoformat(timespec='seconds')
data=read_tab('entities_leads')
header=data.get('values',[])[0]
row={name:'' for name in header}
row.update({
    'lead_id':'L-1ST-SEND',
    'nome':'Lead Primeiro',
    'whatsapp':'+554185134105',
    'origem':'fb',
    'nicho':'solar',
    'status_funil':'novo',
    'created_at':created,
    'ultima_msg_em':created,
    'ultima_acao':'followup_ready',
    'proxima_acao_em':past,
    'proxima_acao_tipo':'whatsapp_intro',
    'responsavel_worker':'automation_core',
    'valor_estimado':'0',
    'observacoes':'teste manual',
})
end_col=column_letter(len(header))
values=[[row.get(col,'') for col in header]]
update('entities_leads', f'A2:{end_col}2', values)
print('set first lead due at', past)
