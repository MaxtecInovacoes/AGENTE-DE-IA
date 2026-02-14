import uuid
from datetime import datetime, timezone
from scripts.sheet_helpers import get_sheet_client
client, state = get_sheet_client()
events_tab = state['mapping']['events_log']
row = [
    f"E-{uuid.uuid4().hex[:8]}",
    datetime.now(timezone.utc).isoformat(),
    "automation",
    "CONTROL_TOWER",
    "control_tower",
    "psycho_sales_system",
    "psycho_sales_v1_finalized",
    "close_probability active=True; priority_queue active=True; facebook_loop active=True",
]
client.append_row(events_tab, row)
