import os
from pathlib import Path
import requests

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
url=f'https://gateway.maton.ai/google-sheets/v4/spreadsheets/{spreadsheet_id}/values/events_log'
resp=requests.get(url,headers=headers,params={'majorDimension':'ROWS'})
resp.raise_for_status()
values=resp.json().get('values',[])
followup=0
whatsapp=0
lead_ids_followup=set()
lead_ids_whatsapp=set()
for row in values[1:]:
    acao=row[6] if len(row)>6 else ''
    entity=row[3] if len(row)>3 else ''
    if acao=='followup_send':
        followup+=1
        lead_ids_followup.add(entity)
    if acao=='whatsapp_send':
        whatsapp+=1
        lead_ids_whatsapp.add(entity)
print('sheet rows',len(values)-1)
print('followup_send',followup)
print('whatsapp_send',whatsapp)
print('lead_ids followup sample',list(lead_ids_followup)[:5])
print('lead_ids whatsapp sample',list(lead_ids_whatsapp)[:5])
