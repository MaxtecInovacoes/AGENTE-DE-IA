import json
from pathlib import Path
path = Path.home() / '.openclaw' / 'workers' / 'whatsapp_throttle.json'
print('exists', path.exists())
with path.open('r', encoding='utf-8') as handle:
    print(json.dumps(json.load(handle), indent=2, ensure_ascii=False))
