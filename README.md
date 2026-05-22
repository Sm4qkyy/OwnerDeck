# OwnerDeck — Marketing Site

A single-page marketing site for OwnerDeck, the automated owner reporting service for short-term rental managers in Cyprus & Greece.

## Files

- `index.html` — main page (all sections in one file)
- `styles.css` — all styling
- `script.js` — nav, FAQ accordion, reveal animations
- `report_page_1.png` to `report_page_4.png` — PDF preview images embedded throughout

## Deploy to Vercel (recommended — free, fast, 5 minutes)

### Option A: Drag & drop (easiest)

1. Go to https://vercel.com → sign up with GitHub or email
2. From the dashboard, click "Add New..." → "Project"
3. Drag the entire `ownerdeck-site` folder into the upload area
4. Click Deploy
5. Done — you'll get a `*.vercel.app` URL within ~30 seconds

### Option B: GitHub-based (better long-term)

1. Push this folder to a GitHub repo (e.g. `ownerdeck-site`)
2. Import the repo into Vercel
3. Auto-deploys on every push

## Connect ownerdeck.com to Vercel

1. In Vercel project dashboard → Settings → Domains
2. Add `ownerdeck.com` and `www.ownerdeck.com`
3. Vercel will show DNS records you need to add at Namecheap/Porkbun
4. In your registrar's DNS settings, add:
   - **A record:** `@` → `76.76.21.21`
   - **CNAME:** `www` → `cname.vercel-dns.com`
5. Wait 10–60 min for DNS propagation
6. SSL certificate auto-installs

## Editing the site

Open `index.html` in any text editor. Text changes are straightforward — search for the section heading you want to edit and update the text inside the relevant `<h2>`, `<p>`, or list items.

To change colors/fonts: edit the `:root` block at the top of `styles.css`.

## What's next

1. **Replace report previews** as you build real client reports — swap the PNGs with real (anonymized) client outputs once you have them
2. **Add testimonials section** after client #3 — slot it between "How it works" and "Features"
3. **Add a blog** later for SEO — Vercel supports markdown blogs via simple folder structures

Built fast. Iterate fast.
