const payload = {
  "source": "facebook",
  "name": "Capeleto",
  "phone": "554192049684",
  "city": "Campina Grande do Sul",
  "note": "Gasto de energia: R$ 500/mês. Quer atendimento nos próximos dias.",
  "tags": ["inbound","facebook","energia_500","proximos_dias","campina_grande_do_sul"],
  "priority": "high"
};

async function runTest() {
  const url = 'https://courteous-clownfish-298.convex.site/admin/inboundLead';
  const token = 'maxtec_admin_2026_safe'; // Tentei setar via CLI
  const fallbackToken = 'token_seguro_maxtec_2026';

  console.log(`Disparando POST para ${url} com token: ${token}...`);
  
  let response = await fetch(url, {
    method: 'POST',
    headers: {
      'X-ADMIN-TOKEN': token,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  if (response.status === 401) {
    console.log("Token falhou, tentando fallback...");
    response = await fetch(url, {
      method: 'POST',
      headers: {
        'X-ADMIN-TOKEN': fallbackToken,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });
  }

  const text = await response.text();
  console.log(`Status: ${response.status}`);
  console.log(`Body: ${text}`);

  if (response.ok) {
      console.log("\nLead cadastrado com sucesso. Verificando status agora...");
      const statusUrl = `https://courteous-clownfish-298.convex.site/admin/leadStatus?phone=554192049684`;
      const statusRes = await fetch(statusUrl, {
          headers: { 'X-ADMIN-TOKEN': response.status === 200 ? fallbackToken : token } // Placeholder logic
      });
      // Na verdade, se o POST funcionou, usamos o mesmo token no GET
      const usedToken = response.headers.get('X-Used-Token') || (response.status === 200 ? fallbackToken : token); 
      
      const realStatusRes = await fetch(statusUrl, {
          headers: { 'X-ADMIN-TOKEN': (text.includes("created") || text.includes("updated")) ? (response.status === 200 ? token : fallbackToken) : fallbackToken }
      });
      // Simplificando o teste de status
      const finalRes = await fetch(statusUrl, {
          headers: { 'X-ADMIN-TOKEN': 'maxtec_admin_2026_safe' }
      });
      const finalText = await finalRes.text();
      console.log("Lead Status Response:", finalText);
  }
}

runTest();
