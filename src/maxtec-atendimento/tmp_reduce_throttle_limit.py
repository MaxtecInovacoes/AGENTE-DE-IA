import json
from pathlib import Path
path = Path.home() / '.openclaw' / 'workers' / 'whatsapp_throttle.json'
with path.open('r', encoding='utf-8') as f:
    config = json.load(f)
config.setdefault('settings', {})['hour_limit'] = 20
with path.open('w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)
print('hour limit reset to 20')
