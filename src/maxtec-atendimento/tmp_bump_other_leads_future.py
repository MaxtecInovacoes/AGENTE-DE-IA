import os
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path

env_path = Path('.').resolve() / '.env'
with env_path.open() as f:
    for line in f:
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

def update_range(tab, range_name, values):
    resp=requests.put(f'{base_url}/{tab}!{range_name}', headers=headers, params={'valueInputOption':'USER_ENTERED'}, json={'values':values})
    resp.raise_for_status()
    return resp.json()

now = datetime.now(timezone(timedelta(hours=-3)))
future = (now + timedelta(days=1)).isoformat(timespec='seconds')
data = read_tab('entities_leads')
values = data.get('values',[])
if len(values)<=2:
    raise SystemExit('not enough rows')
header=values[0]
rows=values[1:]
updated=[]
for idx,row in enumerate(rows, start=2):
    if idx==2:
        continue
    row_dict={header[i]: row[i] if i<len(row) else '' for i in range(len(header))}
    row_dict['proxima_acao_em']=future
    if not row_dict.get('status_funil'):
        row_dict['status_funil']='novo'
    updated.append([row_dict.get(col,'') for col in header])
end_col=column_letter(len(header))
update_range('entities_leads', f'A3:{end_col}{len(rows)+1}', updated)
print('other leads bumped to future', len(updated))
