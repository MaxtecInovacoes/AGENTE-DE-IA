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
url=f'https://gateway.maton.ai/google-sheets/v4/spreadsheets/{spreadsheet_id}/values/entities_leads'
resp=requests.get(url,headers=headers,params={'majorDimension':'ROWS'})
resp.raise_for_status()
values=resp.json().get('values',[])
if len(values)>1:
    print('row2', values[1])
else:
    print('no row2')
