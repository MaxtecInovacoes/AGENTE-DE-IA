# 🔍 DIAGNÓSTICO COMPLETO - SISTEMA MAXTEC WHATSAPP

**Data:** 2026-02-10 09:46 GMT-3  
**Responsável:** Orion (Agent Manager)

---

## ⚠️ PROBLEMAS IDENTIFICADOS

### 1. **JOB CRON COM MODELO INVÁLIDO** (CRÍTICO)
- **Job:** `maxtec_responder_v2_core` (ID: `b99372c3-697f-4842-a763-1395823a251a`)
- **Erro:** `model not allowed: google-antigravity/gemini-3-flash`
- **Causa:** Arquivo `jobs.json` ainda contém `"model": "gemini-3-flash"` (modelo não registrado no OpenClaw)
- **Impacto:** Job roda a cada 5 minutos e FALHA toda vez
- **Solução aplicada:** Editei manualmente `C:\Users\JESUS TE AMA\.openclaw\cron\jobs.json` removendo o campo `model`
- **STATUS:** ⏳ **AGUARDANDO RESTART DO OPENCLAW** (correção não foi carregada)

---

### 2. **WEBHOOK PROCESSANDO GRUPOS** (RESOLVIDO ✅)
- **Problema:** Webhook estava capturando mensagens de TODOS os grupos do WhatsApp
- **Impacto:** Inbox do Convex ficou lotada com 200+ mensagens de grupos irrelevantes
- **Solução aplicada:** 
  - Adicionei filtro no `http.ts` do Convex:
    ```typescript
    const isGroup = remoteJid.includes("@g.us") || remoteJid.includes("@lid");
    if (isGroup) {
      return new Response("Ignored (Group Message)", { status: 200 });
    }
    ```
  - Limpei o Convex (209 tasks removidas, 19 leads apagados)
- **STATUS:** ✅ **RESOLVIDO** (deploy concluído)

---

### 3. **LEADS CHEGANDO MAS NÃO SENDO RESPONDIDOS** (ROOT CAUSE)

#### **Análise da Cadeia:**

**a) WEBHOOK → CONVEX (✅ FUNCIONANDO)**
- WhatsApp → WAHA → Convex webhook
- Webhook está ativo e processando
- Filtro de grupo funcionando

**b) CONVEX → GERAÇÃO DE RASCUNHO (⚠️ PARCIALMENTE FUNCIONANDO)**
- **Arquivo:** `mission_control_convex/convex/http.ts`
- **Código crítico:**
  ```typescript
  try {
    const aiResponse = await ctx.runAction(api.ai.generateResponse, {
      phone: phone,
      message: messageContent
    });

    if (aiResponse) {
      await ctx.runAction(api.whatsapp.sendMessage, {
        phone: finalRemoteJid,
        message: aiResponse
      });
    }
  } catch (error) {
    console.error("Erro no fluxo automático do Orion:", error);
  }
  ```

**Evidência de falha:**
- Tasks na Inbox com `draft_response: "Desculpe, tive um problema de conexão. Um momento, por favor."`
- **Isso é a resposta de FALLBACK do `ai.ts` quando a chamada ao OpenClaw Gateway FALHA!**

**c) CONVEX → OPENCLAW GATEWAY (❌ FALHANDO)**

**Arquivo:** `mission_control_convex/convex/ai.ts`  
**Chamada crítica:**
```typescript
const response = await fetch(`${openclawUrl}/api/v1/sessions/spawn`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${openclawToken}`
  },
  body: JSON.stringify({
    task: `${systemPrompt}...`,
    model: model,
    cleanup: "delete",
    runTimeoutSeconds: 30
  })
});
```

**Variáveis de ambiente (Convex `.env.local`):**
```
OPENCLAW_GATEWAY_URL=http://localhost:18789
OPENCLAW_GATEWAY_TOKEN=143c95d5b6c728eed1913489f0ef5c6111b4a986fd76e7ff
```

**PROBLEMA PROVÁVEL:**
1. O Convex roda na **nuvem** (aromatic-capybara-36.convex.cloud)
2. Está tentando chamar `http://localhost:18789` (que só existe na sua máquina local!)
3. A chamada FALHA, cai no `catch`, retorna `"Desculpe, tive um problema de conexão"`

---

### 4. **INFRAESTRUTURA DE DEPLOYMENT** (ARQUITETURA INCORRETA)

**Setup atual:**
```
WhatsApp (local) 
  ↓
WAHA (local:3001)
  ↓
Convex Webhook (NUVEM - aromatic-capybara-36.convex.site)
  ↓
OpenClaw Gateway (LOCAL - localhost:18789) ❌ NÃO ALCANÇÁVEL
```

**O Convex na NUVEM não consegue chamar `localhost:18789` da sua máquina!**

---

## 🛠️ SOLUÇÕES POSSÍVEIS

### **Opção A: MOVER TUDO PARA LOCAL** (Recomendado para MVP)
1. Desativar o webhook automático no Convex
2. Criar um worker Python local que:
   - Escuta o webhook do WAHA diretamente
   - Processa mensagens
   - Chama OpenClaw Gateway local
   - Envia resposta via WAHA

**Prós:**
- Tudo local, sem custos
- Fácil de debugar
- OpenClaw Gateway acessível

**Contras:**
- Precisa manter máquina ligada 24/7

---

### **Opção B: EXPOR OPENCLAW VIA NGROK/TÚNEL**
1. Criar túnel público para `localhost:18789`
2. Atualizar `OPENCLAW_GATEWAY_URL` no Convex para a URL pública
3. Manter arquitetura atual

**Prós:**
- Convex continua na nuvem (escalável)
- Menos mudanças no código

**Contras:**
- Segurança (expor OpenClaw na internet)
- Túneis gratuitos reiniciam (URL muda)

---

### **Opção C: MIGRAR OPENCLAW PARA VPS**
1. Hospedar OpenClaw em um VPS (AWS, DigitalOcean, etc.)
2. Apontar Convex para o IP público do VPS
3. Manter WAHA local OU migrar também

**Prós:**
- Produção-ready
- Escalável
- Sem depender de máquina local

**Contras:**
- Custo mensal ($5-20/mês)
- Setup mais complexo

---

## 📊 STATUS GERAL DOS COMPONENTES

| Componente | Status | Detalhes |
|------------|--------|----------|
| WAHA | ✅ WORKING | Conectado, engine WEBJS |
| Webhook Convex | ✅ OK | Filtrando grupos corretamente |
| Convex Database | ✅ LIMPO | 2 tasks na inbox (testes recentes) |
| OpenClaw Gateway | ✅ RODANDO | Localhost:18789 ativo |
| Job `maxtec_responder_v2_core` | ❌ ERRO | Modelo inválido, aguarda restart |
| Convex → OpenClaw | ❌ FALHA | Não alcança localhost da nuvem |

---

## 🎯 AÇÃO IMEDIATA RECOMENDADA

**FASE 1: CORRIGIR JOB CRON**
```bash
openclaw gateway restart
```

**FASE 2: ESCOLHER ARQUITETURA**
Franz precisa decidir entre:
1. Mover webhook para worker Python local (Opção A)
2. Expor OpenClaw via túnel (Opção B)
3. Migrar para VPS (Opção C)

**FASE 3: TESTE DE PONTA A PONTA**
1. Enviar mensagem de teste no WhatsApp
2. Verificar se rascunho é gerado
3. Confirmar envio automático

---

## 📝 NOTAS TÉCNICAS

- **Sessões do OpenClaw:** 16 sessões ativas (maioria grupos do WhatsApp)
- **Modelo configurado:** `claude-sonnet-4-5` (correto)
- **Token OpenClaw válido:** Sim (143c95d5b6c728...)
- **Convex deployment:** `aromatic-capybara-36` (dev)

---

**Próximo passo:** Aguardando decisão de Franz sobre qual arquitetura seguir.
