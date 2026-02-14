const payload = {
  "event": "messages.upsert",
  "instance": "zapmax",
  "data": {
    "key": {
      "remoteJid": "554192049684@s.whatsapp.net",
      "fromMe": false,
      "id": "TEST_ORION_" + Date.now()
    },
    "pushName": "Teste Orion",
    "message": {
      "conversation": "Teste de integração Orion PROD"
    },
    "messageType": "conversation"
  }
};

async function testWebhook() {
  const url = 'https://courteous-clownfish-298.convex.site/webhook/evolution';
  console.log(`🚀 Disparando simulação de webhook para: ${url}`);
  
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  const text = await response.text();
  console.log(`Status: ${response.status}`);
  console.log(`Body: ${text}`);
  
  console.log("\n⌛ Aguardando 5 segundos para processamento dos logs...");
  await new Promise(r => setTimeout(r, 5000));
}

testWebhook();
