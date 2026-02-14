import requests
spreadsheet_id = '1Basl2MvOHd0TvA-8yVwRmDnJMNeHSV7ICRvHQ8x_CDA'
key = 'NbhFknVYQW20kc8Nx1UCDS-tCtxXDJxOF-ZmbcA_FBRMexAhPbGBSKFCNSmSoIHhG1LQGEgx-hVXf6squ8gnIhExqphr76nI2L1FXPos1w'
headers = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}

def write(range_name, values):
    url = f'https://gateway.maton.ai/google-sheets/v4/spreadsheets/{spreadsheet_id}/values/{range_name}?valueInputOption=USER_ENTERED'
    resp = requests.put(url, headers=headers, json={'values': [values]})
    print(range_name, resp.status_code, resp.text)

write('entities_leads!A1:M1', [
    'lead_id','nome','whatsapp','origem','nicho','status_funil','ultima_msg_em','ultima_acao','proxima_acao_em','proxima_acao_tipo','responsavel_worker','valor_estimado','observacoes'
])
write('entities_projects!A1:H1', [
    'project_id','cliente','nicho','status','ultima_acao','proxima_acao_em','link_pasta','observacoes'
])
write('events_log!A1:H1', [
    'event_id','timestamp','entity_type','entity_id','source','worker','acao','resumo'
])
write('alerts_queue!A1:G1', [
    'alert_id','timestamp','severidade','entity_id','motivo','status','owner'
])
