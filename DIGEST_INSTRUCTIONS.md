# 📋 Porsche Digest V1 — Instruções Detalhadas por Sessão

## Overview Geral

**Nome:** Porsche 993 Daily Digest Generator v4.0  
**Objetivo:** Gerar um digest premium diário com conteúdo sobre Porsche air-cooled 911  
**Inspiração:** Porsche Design System (PDS)  
**Dados:** USD/BRL prices, leilões ao vivo, valuation, vídeos curados  
**Deploy:** Cloudflare Pages  
**Atualização:** Diária (automática via cron)  

---

## 🎯 INSTRUÇÕES POR SESSÃO

### 1. 🏆 PORSCHE NEWSROOM & CLASSIC

**Objetivo:** Exibir artigos recentes do Porsche Newsroom em formato de carousel

**Dados Coletados:**
- Fonte: Porsche Newsroom (RSS feed simulado)
- 5 artigos com títulos, datas, descrições
- Imagens de herança (air-cooled era)

**Instrução HTML:**
```html
<section>
    <h2 class="section-title"><span>🏆</span> Porsche Newsroom & Classic</h2>
    <div class="carousel-container">
        <div class="carousel-track">
            <!-- Cards com: imagem, data, título, descrição, link "Read more" -->
        </div>
        <button class="carousel-prev">❮</button>
        <button class="carousel-next">❯</button>
    </div>
</section>
```

**Instrução CSS:**
- Cards: 280px width, rounded corners, shadow
- Carousel: horizontal scroll, smooth transitions
- Mobile: stack para 1 coluna

**Instrução JS:**
- Scroll listeners para navegação
- Arrow key support
- Auto-scroll indicator

**Dados Exigidos:**
```json
{
  "title": "string",
  "image_url": "https://...",
  "date": "X days ago",
  "description": "string",
  "link": "https://porsche.com/..."
}
```

**Evolução Sugerida:**
- [ ] Adicionar filtro por categoria (News, Stories, Technical)
- [ ] Implementar infinite scroll
- [ ] Adicionar "favorite" button
- [ ] Integrar com RSS real do Porsche Newsroom

---

### 2. 📈 MARKET & AUCTIONS

**Objetivo:** Mostrar leilões ao vivo com preços USD/BRL, plataforma, status

**Dados Coletados:**
- Fonte: Bring a Trailer + Cars & Bids (RSS feeds)
- 10 leilões ativos
- Preços, status (Active, Ending Soon, Ending)
- Logo da plataforma

**Instrução HTML:**
```html
<section>
    <h2 class="section-title"><span>📈</span> Market & Auctions</h2>
    <div class="market-table-wrap">
        <table class="market-table">
            <thead>
                <tr>
                    <th>PLATFORM</th>
                    <th>VEHICLE</th>
                    <th>PRICE (USD)</th>
                    <th>PRICE (BRL)</th>
                    <th>STATUS</th>
                </tr>
            </thead>
            <tbody>
                <!-- Rows geradas dinamicamente -->
            </tbody>
        </table>
    </div>
</section>
```

**Instrução CSS:**
- Tabela: full-width, striped rows
- Status badges: cores (verde=Active, amarelo=Ending Soon, vermelho=Ended)
- Mobile: horizontal scroll

**Instrução JS:**
- Sort por preço/data
- Filter por plataforma
- Currency toggle USD/BRL

**Dados Exigidos:**
```json
{
  "platform": "Bring a Trailer | Cars & Bids",
  "platform_logo": "https://...",
  "title": "1996 Porsche 911 Carrera 4S Coupe",
  "price_usd": 142500,
  "price_brl": 735300,
  "status": "Active | Ending Soon | Ended",
  "url": "https://bringatrailer.com/..."
}
```

**Regras de Status:**
- "Active" = verde (#27ae60)
- "Ending Soon" = amarelo (#f39c12)
- "Ending" = vermelho (#e74c3c)

**Evolução Sugerida:**
- [ ] Integrar API real de BAT/C&B
- [ ] Adicionar gráfico de histórico de preços
- [ ] Alertas quando carro específico aparece
- [ ] Comparar preços entre plataformas
- [ ] Exportar CSV/PDF

---

### 3. 💰 VALUATION ANALYSIS

**Objetivo:** Mostrar análise de mercado (preços médios, trends YoY, range)

**Dados Coletados:**
- Fonte: Classic.com, BAT Index, PCA Market Report
- 3 modelos: C4S, Carrera, Turbo
- Preços avg, range (min-max), YoY trend

**Instrução HTML:**
```html
<section>
    <h2 class="section-title"><span>💰</span> Valuation Analysis</h2>
    
    <!-- Chart.js Graph -->
    <div class="valuation-charts">
        <div class="valuation-chart-container">
            <canvas id="valuationChart"></canvas>
        </div>
    </div>
    
    <!-- 3-Column Grid -->
    <div class="valuation-grid">
        <div class="valuation-card">
            <!-- Model, price, trend, range bar -->
        </div>
        <!-- ... repeat 3x -->
    </div>
</section>
```

**Instrução CSS:**
- Grid: 3 colunas (auto-fit minmax 250px)
- Cards: branco background, hover shadow
- Range bar: visual da faixa de preços

**Instrução JS (Chart.js):**
```javascript
const ctx = document.getElementById('valuationChart').getContext('2d');
const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['2024', '2025', '2026'],
    datasets: [
      {
        label: 'C4S',
        data: [138000, 146500, 155000],
        borderColor: '#d4af37',
        backgroundColor: 'rgba(212, 175, 55, 0.1)'
      },
      // ... Carrera, Turbo
    ]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { position: 'top' }
    },
    scales: {
      y: {
        beginAtZero: false,
        title: { display: true, text: 'Price (USD)' }
      }
    }
  }
});
```

**Dados Exigidos:**
```json
{
  "model": "C4S | Carrera | Turbo",
  "avg_price_usd": 155000,
  "avg_price_brl": 792550,
  "yoy_change": "+12%",
  "range_low": 60000,
  "range_high": 395000,
  "source": "Classic.com Market Data 2025-2026"
}
```

**Range Bar Visual:**
- Barra preenchida proporcionalmente à faixa
- Posição = (preço_avg - min) / (max - min)

**Evolução Sugerida:**
- [ ] Adicionar 5-year trend chart
- [ ] Comparar com inflação/mercado geral
- [ ] Previsão de preços (AI)
- [ ] Alertas quando preço ultrapassa X%
- [ ] Integração com APIs de valuation reais

---

### 4. 🔧 993 PARTS & ACCESSORIES

**Objetivo:** Listar fornecedores oficiais de peças para o 993

**Dados Coletados:**
- Fornecedores: Suncoast Parts, Partswise, FCP Euro
- Logo, descrição, categoria (OEM/Aftermarket/Performance)
- Link direto

**Instrução HTML:**
```html
<section>
    <h2 class="section-title"><span>🔧</span> 993 Parts & Accessories</h2>
    <span>Official parts suppliers for your 1996 Carrera 4S (VIN: WP0AA2999TS320294)</span>
    
    <div class="profiles-grid">
        <a href="https://..." class="profile-card">
            <div class="profile-thumb-container">
                <img src="logo.png" alt="Supplier" loading="lazy">
            </div>
            <span class="profile-tag">OEM PARTS</span>
            <h3>Suncoast Porsche Parts</h3>
            <p>Official Porsche parts supplier...</p>
        </a>
        <!-- ... repeat 3x -->
    </div>
</section>
```

**Instrução CSS:**
- Grid: 3 colunas (auto-fit)
- Cards: image top, tag badge, título, descrição
- Hover: card lift effect

**Dados Exigidos:**
```json
{
  "name": "Suncoast Porsche Parts",
  "category": "OEM PARTS | OEM/AFTERMARKET | PERFORMANCE",
  "logo_url": "https://porsche-stories.imgix.net/suncoast-logo.png",
  "description": "Official Porsche parts supplier...",
  "url": "https://www.suncoastparts.com/..."
}
```

**Evolução Sugerida:**
- [ ] Adicionar preços de peças populares
- [ ] Integrar com APIs de inventory
- [ ] Comparador de preços entre fornecedores
- [ ] Guia de compras por modelo
- [ ] Avaliações de usuários

---

### 5. 🔗 PORSCHE REFERENCE PROFILES

**Objetivo:** Destacar 3 comunidades/personas diferentes de entusiastas 993

**Personas:**

**A. DRIVERS COMMUNITY**
- **Foco:** Road-focused, travel, meetups, lifestyle
- **Vibe:** Dynamic, adventurous, social
- **Imagem:** Community gathering em road trip
- **URL:** Link para perfil PCNA ou comunidade oficial

**B. COLLECTORS (PORSCHE PERFECTION)**
- **Foco:** Originality, low mileage, exclusivity, valuation
- **Vibe:** Premium, meticulous, investment-focused
- **Imagem:** Pristine 993 Turbo em garagem
- **URL:** Link para Porsche Club ou collectors group

**C. CUSTOM COMMUNITY**
- **Foco:** Modifications, performance, tuning, builds
- **Vibe:** Creative, technical, progressive
- **Imagem:** Modified/restomod 993
- **URL:** Link para Rennlist ou custom forums

**Instrução HTML:**
```html
<section>
    <h2 class="section-title"><span>🔗</span> Porsche Reference Profiles</h2>
    
    <div class="profiles-grid">
        <a href="/previews/porsche_drivers.html" class="profile-card">
            <img src="drivers.jpg" alt="Drivers Community">
            <span class="profile-tag">COMMUNITY</span>
            <h3>Porsche Drivers</h3>
            <p>Community resources for road-focused enthusiasts...</p>
        </a>
        <!-- ... Collectors, Custom -->
    </div>
</section>
```

**Instrução CSS:**
- Grid: 3 colunas
- Card: image 40x40px thumbnail
- Tag: colored badge (COMMUNITY, COLLECTORS, CUSTOM)

**Dados Exigidos:**
```json
{
  "name": "Porsche Drivers | Porsche Collectors | Porsche Custom",
  "type": "COMMUNITY | COLLECTORS | CUSTOM",
  "thumbnail": "https://...",
  "description": "string",
  "url": "https://..."
}
```

**Evolução Sugerida:**
- [ ] Adicionar membros destacados
- [ ] Integrar feeds de posts recentes
- [ ] Event calendar
- [ ] Forum integration
- [ ] Achievements/badges

---

### 6. 🔥 911 TURBO S 2026 — LEGACY EVOLUTION

**Objetivo:** Mostrar evolução do 993 Turbo até 2026 (comparativa)

**Seções:**

**A. Headline**
- "911 Turbo S (2026) — The Next Generation"
- Subtitle: "Tracing the evolution from 993 Turbo to the latest iteration"

**B. 3 Highlight Cards**
1. **Power:** 640 hp (vs 993 Turbo's 424 hp)
   - "Up from the 993 Turbo S's 424 hp. Full hybrid powertrain coming 2026."
   
2. **0-60 mph:** 2.1s (vs 993 Turbo's 3.6s)
   - "vs 993 Turbo S at 3.6s. 40% faster than the air-cooled legend."
   
3. **Active Aerodynamics**
   - "Adaptive spoiler, front axle lift, and active air intake flaps."

**Instrução HTML:**
```html
<section>
    <h2><span>🔥</span> 911 Turbo S (2026) — The Next Generation</h2>
    <p>Tracing the evolution from 993 Turbo to the latest iteration</p>
    
    <div class="turbo-s-grid">
        <div class="turbo-s-card">
            <img src="turbo-power.jpg" alt="Power">
            <h4>⚡ Power: 640 hp → 3.0L Twin-Turbo</h4>
            <p>Up from the 993 Turbo S's 424 hp...</p>
        </div>
        <!-- ... repeat 3x -->
    </div>
</section>
```

**Dados Exigidos:**
```json
{
  "headline": "911 Turbo S (2026) — The Next Generation",
  "subhead": "Tracing the evolution...",
  "highlights": [
    {
      "title": "Power: 640 hp → 3.0L Twin-Turbo",
      "desc": "Up from...",
      "image": "https://..."
    }
  ]
}
```

**Evolução Sugerida:**
- [ ] Adicionar timeline visual 993 → 992 → 2026
- [ ] Spec comparison table
- [ ] Price comparison
- [ ] Availability/pre-order info
- [ ] Teaser video

---

### 7. 🔧 TECHNICAL SPECIFICATIONS

**Objetivo:** Detalhar specs do seu 993 específico

**Informações Estáticas (do seu Porsche):**
```
Modelo: 1996 Porsche 911 Carrera 4S
VIN: WP0AA2999TS320294
Motor: M64/21 Varioram (3.6L, 282 hp, 210 kW)
Transmissão: 6-speed manual (G64/20)
Tração: Viscous AWD (Carrera 4S)
Ano: 1996
Cor: Arctic Silver Metallic (570)
Chassis: Widebody (Turbo-look)
Suspensão: M030 sport suspension
Freios: Brembo 4-piston
```

**Instrução HTML:**
```html
<section>
    <h2><span>🔧</span> Technical Specifications</h2>
    <span>M64/21 Varioram • 993 Carrera 4S</span>
    
    <div class="specs-grid">
        <div class="spec-block">
            <strong>ENGINE</strong>
            <p>Flat-6 M64/21 Varioram<br/>3.6L, 282 hp (210 kW)</p>
        </div>
        <!-- ... repeat para cada spec -->
    </div>
</section>
```

**Instrução CSS:**
- Grid: 2 colunas
- Cada bloco: label bold + detalhes

**Evolução Sugerida:**
- [ ] Adicionar maintenance intervals
- [ ] Known issues por modelo
- [ ] Modificações recomendadas
- [ ] Consumo de combustível
- [ ] Performance figures (0-60, top speed)

---

### 8. 📹 DAILY PORSCHE VIDEO PICKS

**Objetivo:** Mostrar 3 vídeos curados por cada persona

**Estrutura:**
```
Porsche Drivers Profile
  ├─ Vídeo 1: Track/performance focused
  ├─ Vídeo 2: Road trip/lifestyle
  └─ Vídeo 3: Technical/mechanical

Porsche Collectors Profile
  ├─ Vídeo 1: Restoration/pristine condition
  ├─ Vídeo 2: Rare models/special editions
  └─ Vídeo 3: History/heritage

Porsche Custom Community
  ├─ Vídeo 1: Build/modification process
  ├─ Vídeo 2: Engine work/performance upgrade
  └─ Vídeo 3: Finished build showcase
```

**Instrução HTML:**
```html
<section>
    <h2><span>📹</span> Daily Porsche Video Picks</h2>
    <p>Curated by profile — relevance, quality, and engagement</p>
    
    <div class="video-profiles">
        <div class="video-profile-section">
            <h4>Porsche Drivers Profile</h4>
            <div class="video-row">
                <a href="https://youtube.com/..." class="video-card">
                    <div class="video-thumbnail">
                        <img src="https://img.youtube.com/vi/ID/sddefault.jpg" alt="Title">
                        <div class="video-duration">12:34</div>
                    </div>
                    <div class="video-content">
                        <h5>Title</h5>
                        <span class="video-channel">Channel</span>
                        <span class="video-views">45K views</span>
                    </div>
                </a>
                <!-- ... repeat 3x -->
            </div>
        </div>
        <!-- ... repeat para Collectors, Custom -->
    </div>
</section>
```

**Dados Exigidos:**
```json
{
  "profile": "drivers | collectors | custom",
  "videos": [
    {
      "title": "Video Title",
      "channel": "Channel Name",
      "url": "https://youtube.com/watch?v=ID",
      "thumbnail": "https://img.youtube.com/vi/ID/sddefault.jpg",
      "views": "45K",
      "duration": "12:34"
    }
  ]
}
```

**Curação Manual (Instrução):**
- Drivers: buscar "993 carrera track" + "air-cooled 911 road trip"
- Collectors: buscar "993 restoration" + "rare 911 models"
- Custom: buscar "993 build" + "air-cooled engine swap"

**Evolução Sugerida:**
- [ ] Integrar YouTube API v3
- [ ] Auto-curate baseado em tags
- [ ] User ratings (👍👎)
- [ ] Add to playlist feature
- [ ] Comment section

---

## 📊 DADOS GLOBAIS (Aplicados a Todas Seções)

### Exchange Rate (Atualizado Diariamente)
```
Fonte: exchangerate-api.com
Fallback: 5.11 BRL/USD (se API falhar)
Uso: Converter todos os preços USD → BRL
```

### Datas e Formatação
```
Date Format: "d de B de Y" (ex: "16 de August de 2026")
Currency USD: "$142,500" (formatado com comma)
Currency BRL: "R$738,150" (formatado com comma)
Dias: "0 days ago", "3 days ago", "12 days ago"
```

### Attribution (Footer)
```
"Generated by Hermes Carrera • Sources: Porsche Stories, 
Bring a Trailer, Cars & Bids, Xe.com, Classic.com"
```

---

## 🎨 DESIGN SYSTEM GLOBAL

### Cores (Porsche Design System Inspired)
```
Primary Black: #000000
Porsche Gold: #d4af37
Light Gray: #f5f5f5
Dark Gray: #2c2c2c
Accent Green (Status Active): #27ae60
Accent Yellow (Status Ending): #f39c12
Accent Red (Status Ended): #e74c3c
```

### Typography
```
Headlines: Bold, 28-32px
Subtitles: Regular, 16-18px
Body: Regular, 14-16px
Captions: 12-14px
Font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
```

### Spacing
```
Section padding: 2rem (desktop), 1.5rem (mobile)
Card gap: 2rem
Mobile breakpoint: 768px
```

---

## 🔄 FLUXO DE GERAÇÃO DIÁRIA

1. **Coleta de Dados**
   - Fetch Porsche Newsroom (RSS)
   - Fetch auctions (BAT + C&B RSS)
   - Fetch valuation data (API ou mock)
   - Fetch videos (YouTube API ou curated list)

2. **Processamento**
   - Converter USD → BRL
   - Format datas
   - Sort auctions por status/preço
   - Organize vídeos por profile

3. **Template Rendering**
   - Gerar HTML com todas as seções
   - Incluir CSS inline + externo
   - Incluir JS (Chart.js, carousel, etc)

4. **Deployment**
   - Write index.html
   - Archive versão anterior
   - Deploy para Cloudflare Pages
   - Atualizar CNAME (digest.costafamily.ai)

5. **Notificação**
   - Enviar resumo para Telegram (@Danrcbh_bot)
   - Log de sucesso/erros

---

## 🚀 EVOLUÇÕES RECOMENDADAS (ROADMAP)

### Curto Prazo (1-2 semanas)
- [ ] Integrar YouTube API v3 (em vez de links manuais)
- [ ] Integrar BAT RSS oficial
- [ ] Adicionar filtros na tabela de auctions
- [ ] Implementar "Favorite listings" com LocalStorage

### Médio Prazo (1 mês)
- [ ] Integrar Classic.com API para valuation real
- [ ] Adicionar alerts (preço ultrapassa X, novo carro aparece)
- [ ] Implementar dark mode
- [ ] Adicionar multilíngue (EN/PT-BR/DE)

### Longo Prazo (2-3 meses)
- [ ] Machine Learning para curação de vídeos
- [ ] Previsão de preços com AI
- [ ] Community features (comments, likes, shares)
- [ ] Mobile app native
- [ ] Integração com Discord/Slack para alerts

---

## 📝 CHECKLIST DE MANUTENÇÃO DIÁRIA

- [ ] Executar `python generate_digest.py`
- [ ] Verificar dados de auctions (se algum faltando)
- [ ] Validar preços USD/BRL
- [ ] Testar links (Newsroom, YouTube, BAT, C&B)
- [ ] Verificar Cloudflare deploy
- [ ] Confirmar receipt no Telegram

---

**Versão:** V1 (Aprovada)  
**Data:** 16 Agosto 2026  
**Próxima Atualização:** Automática (daily cron)  
**Maintainer:** Hermes Carrera
