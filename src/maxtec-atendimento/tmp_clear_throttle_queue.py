import json
from pathlib import Path
path = Path.home() / '.openclaw' / 'workers' / 'whatsapp_throttle.json'
with path.open('r', encoding='utf-8') as f:
    config = json.load(f)
config['queue'] = []
config['sent_last_hour'] = []
config['last_sent_at'] = None
with path.open('w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)
print('fila limpa')
