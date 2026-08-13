# Porsche Digest V1 — Lessons Learned & Replicable Patterns

## 📊 **Project Overview**
- **Duration**: August 6-13, 2026 (7-day MVP to V1)
- **Stack**: Python 3.11 + HTML/CSS (vanilla) + Cloudflare Pages
- **Deploy**: GitHub → Cloudflare Pages via `wrangler pages deploy`
- **Line Count**: generate_digest.py grew from 549 → 1433 lines

## 🏗️ **Architecture Patterns**

### 1. Template-Based HTML Generation
**Pattern**: Single monolithic template with f-string interpolation
```python
html = f"""<!DOCTYPE html>...{variable}..."""
```
**Pros**: 
- Self-contained, easy to debug
- No external template engine

**Cons**:
- Escaped braces `{{ }}` everywhere
- Hard to maintain at 1400+ lines

**Better approach**: Use Jinja2 or extract HTML to template files

### 2. Cloudflare Pages Deployment
**Pattern**: `npx wrangler pages deploy . --project-name porsche-digest --branch main`
**Key env vars**:
- `CLOUDFLARE_API_TOKEN` (stored in `~/.hermes/.env`)
- `CLOUDFLARE_ACCOUNT_ID`

**Learning**: Need `~/.hermes/.env` for secrets, not project-local files

### 3. Archive System
**Pattern**: Daily snapshot of index.html → `archive/YYYY-MM-DD.html`
**CSS Injection**: History section injected before Sources section

## 🎨 **Design System Implementation**

### Porsche Design System (PDS) Guidelines
1. **Color Palette**:
   - Gold: `#d4af37`
   - Black: `#000000`
   - Gray: `#868686` (text), `#f4f4f4` (borders)
   - White: `#ffffff`

2. **Typography Hierarchy**:
   - Headings: `Playfair Display` (serif, premium)
   - Body: `Inter` (sans-serif, readable)
   - Section titles: `2.5rem` mobile → `3rem` desktop
   - Card titles: `1.125rem`

3. **Grid System**:
   - Desktop: `repeat(3, 1fr)` for cards, `grid-template-columns: minmax(280px, 1fr)` for responsive
   - Mobile: Single column, `@media (max-width: 768px)` and `@media (max-width: 430px)`

4. **Card Patterns**:
   - Rounded corners: `border-radius: 1rem`
   - Shadow: `0 5px 20px rgba(0,0,0,0.05)` → hover `0 20px 40px rgba(0,0,0,0.08)`
   - Border: `1px solid var(--porsche-light-gray)` → hover `var(--porsche-gold)`

### Thumbnail Patterns
1. **Carousel cards**: 600x400px, object-fit: cover
2. **Valuation cards**: 50x30px, object-fit: contain (car silhouettes)
3. **Market table**: 40x25px, object-fit: cover (mini car images)
4. **Parts cards**: SVG logos 40x40px
5. **Profile cards**: 50x50px, object-fit: contain (profile images)
6. **Video cards**: 120x120px, object-fit: cover (YouTube thumbnails)

### Lazy Loading Strategy
- Hero image: `loading="eager"`
- All other images: `loading="lazy"`
- Width/Height attributes on all images to prevent CLS

## 📱 **Mobile Optimization**

### iPhone Pro Max 17 UX
- Viewport width: 430px CSS
- Carousel: `min-width: 158px` → 2.5 cards visible
- Cards: `flex: 1 0 0` for equal distribution
- Font sizes: Reduce by 20-30% in mobile media query
- Padding: Reduce to 1rem from 2.5rem

### Breakpoints
```css
@media (max-width: 768px) { /* Tablet */ }
@media (max-width: 430px) { /* iPhone Pro Max 17 */ }
```

## 📡 **Data Sources & Scraping**

### 1. Porsche Stories (content-hub.imgix.net)
- Format: `https://content-hub.imgix.net/GUhocLc6.../{slug}?w=600`
- Returns: JSON with title, description, image, URL
- Carousel: 6 articles, auto-advanced

### 2. Auction Data
- **Bring a Trailer**: `https://bringatrailer.com/listing/{slug}/` (scraped)
- **Cars & Bids**: `https://carsandbids.com/listing/{slug}` (scraped)
- **Classic.com**: Market data API (valuation reference)

### 3. Currency Conversion
- Source: Xe.com API
- Rate: ~5.09-5.12 BRL per USD
- Displayed: Both USD and BRL on every listing

### 4. Hero Images
- Source: Porsche Stories CDN
- Pattern: `https://porsche-stories.imgix.net/{image}?w=1200&q=85`
- Date-based rotation via `daily_hero_image.py`

## 🚀 **Deployment Pipeline**

### Automated Steps
1. **Archive**: Save current `index.html` → `archive/YYYY-MM-DD.html`
2. **History Injection**: Inject archive history section into HTML
3. **Git Operations**: `git add . && git commit && git push origin main`
4. **Cloudflare Deploy**: `npx wrangler pages deploy . --project-name porsche-digest`
5. **Verification**: HTTP 200 check on both URLs

### Cron Configuration
```
Schedule: Daily at 07:00 UTC
Command: python generate_digest.py
Delivery: Telegram message with digest preview
```

## 🌐 **PWA Configuration**

### manifest.json
```json
{
  "name": "Porsche 993 Daily Digest",
  "short_name": "993 Digest",
  "theme_color": "#d4af37",
  "background_color": "#000000",
  "display": "standalone"
}
```

### Meta Tags (in HTML head)
- `<meta name="theme-color" content="#d4af37">`
- `<meta name="apple-mobile-web-app-capable" content="yes">`
- `<link rel="apple-touch-icon" href="/icon-192.png">`

## 🤖 **AI Content Curation**

### Video Curation Logic
- 3 videos per profile (Drivers, Collectors, Custom)
- Criteria: relevance + quality + engagement (view counts)
- Sources: YouTube, Porsche Stories, Hagerty, Canzoniero

### Parts Card Curation
- 3 suppliers: Suncoast, Partswise, FCP Euro
- Tags: OEM, AFTERMARKET, PERFORMANCE
- Links: Direct to exact product category

## 📊 **Telegram Integration**

### Message Format
```
🏆 Porsche 993 Daily Digest — DD/MM/YYYY
[Quote from Porsche engineer/designer]
📰 5 News Articles
🚗 10 Auction Listings
📈 Valuation Analysis
🔧 Technical Specs
```

### Cron Delivery
- Daily 07:00 UTC
- Delivered to Telegram home channel

## 🛡️ **Performance Optimizations**

1. **Lazy Loading**: 33 images with `loading="lazy"`
2. **Width/Height attributes**: All img tags
3. **Object-fit**: CSS instead of JS for image sizing
4. **CSS Grid/Flexbox**: No JS for layout
5. **Minimal dependencies**: Pure Python + stdlib only

## 📈 **Lessons for Future Projects**

1. Template engines (Jinja2) >> f-string HTML for >500 line files
2. Environment variables should use prefixed keys (`PORSCHE_`)
3. Image URLs should be validated before insertion
4. The `--cb` cache-buster query param is essential during dev
5. `npx wrangler pages deploy .` needs `--branch` and `--cwd` for reliability
6. Cloudflare Pages auto-deploys on git push — the `wrangler deploy` is redundant for production