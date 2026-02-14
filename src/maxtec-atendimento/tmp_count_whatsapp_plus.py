import sqlite3
import re
from pathlib import Path

conn = sqlite3.connect(Path(r'C:\Users\JESUS TE AMA\.openclaw\state\control_tower.db'))
cur = conn.cursor()
regex = re.compile(r'^\+\d{10,15}$')
cur.execute('SELECT whatsapp FROM entities_leads')
plus_count = 0
total = 0
for (value,) in cur.fetchall():
    if value and regex.match(value.strip()):
        plus_count += 1
    total += 1
print('plus', plus_count, 'total', total)
conn.close()
