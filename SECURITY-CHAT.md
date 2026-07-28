# Live chat — setup & protection

The chat is built and deployed but **inert until you add the keys below**.
With no `ANTHROPIC_API_KEY` set, the endpoint returns `503 not_configured`
and costs nothing. Nothing is exposed in the meantime.

Work through this in order. Step 1 is the one that actually caps your risk.

---

## 1. Set the spend cap FIRST — before the API key

This is the only protection that cannot be bypassed. Everything else is a
filter; this is the wall.

1. Go to <https://console.anthropic.com> → **Settings → Limits**
2. Set a **monthly spend limit**. Start at **$10**.
3. Set an **email alert** at ~50% of that.

At our caps a normal exchange costs roughly **$0.0004**, so $10 is about
25,000 messages — far beyond any genuine demo traffic. If you ever hit it,
that is a signal something is wrong, not that business is booming.

**Do not skip this. Do not do it "later".**

---

## 2. Create the API key

1. Console → **API Keys** → create one, scoped to this project.
2. In Vercel → your project → **Settings → Environment Variables**, add:

| Name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | `sk-ant-...` |
| `ALLOWED_ORIGIN` | `https://www.ownerdeck.com,https://ownerdeck.com` |
| `CHAT_ENABLED` | `on` |

3. Redeploy (Vercel → Deployments → ⋯ → Redeploy).

**Never put the key in `config.js`, any HTML, or any file in this repo.**
That file is public. A key in client-side JavaScript is typically found and
drained within days by automated scrapers.

---

## 3. Cloudflare Turnstile (free, ~5 minutes)

This is the single biggest win — it blocks scripted abuse before it ever
reaches your API.

1. Cloudflare dashboard → **Turnstile** → **Add site**
2. Domain `ownerdeck.com`, widget mode **Invisible**
3. You get two keys:
   - **Site key** (public) → put in `config.js` under `liveChat.turnstileSiteKey`
   - **Secret key** (private) → Vercel env var `TURNSTILE_SECRET`

Until the secret is set the endpoint still works but *skips* the human check,
relying on rate limits alone. Set it.

---

## 4. Durable rate limiting — Upstash (free tier)

Without this, rate limiting falls back to per-instance memory, which resets
on every cold start. It is a speed bump, not a wall.

1. <https://upstash.com> → create a free Redis database (pick an EU region)
2. Copy the **REST URL** and **REST token**
3. Add to Vercel:

| Name | Value |
|---|---|
| `UPSTASH_REDIS_REST_URL` | `https://....upstash.io` |
| `UPSTASH_REDIS_REST_TOKEN` | `A...` |

Now the limit of **15 messages per IP per hour** holds across all instances.

---

## 5. Cloudflare rate-limiting rule (recommended)

Blocks floods at the edge, so they never invoke your function and never cost
you anything.

Cloudflare → **Security → WAF → Rate limiting rules** → create:

- **If** URI Path starts with `/api/`
- **Then** when requests exceed **30 per 1 minute** per IP
- **Action** Block, for 10 minutes

---

## What is already enforced in code

`api/chat.js` applies all of this on every request:

| Control | Value |
|---|---|
| Model | `claude-haiku-4-5` (cheapest current Claude) |
| Max output tokens | 300 per reply |
| Max input length | 500 characters per message |
| Conversation cap | 12 exchanges, then it points to email |
| History replayed | last 12 messages only |
| Per-IP rate limit | 15 messages / hour |
| Origin check | must match `ALLOWED_ORIGIN` |
| Kill switch | `CHAT_ENABLED=off` |
| Prompt hardening | refuses anything that isn't about Ownerdeck |

The system prompt explicitly refuses code, translation, essays, roleplay and
general knowledge — so it cannot be repurposed as a free general chatbot,
which is the usual motive for abusing an endpoint like this.

---

## If something goes wrong

**To stop it instantly:** set `CHAT_ENABLED=off` in Vercel and redeploy.
No code change needed. Or set `liveChat.enabled = false` in `config.js` to
remove it from the page entirely.

**Signs of abuse:** a spend alert, a spike in Vercel function invocations, or
repeated `rate_limited` / `failed_challenge` responses in the logs.

**Where to look:** Vercel → your project → **Logs**, filter to `/api/chat`.

---

## Honest limitations

- **Turnstile is not unbreakable.** A determined attacker with a solver can
  get through. It stops the automated 99%, not a targeted human.
- **IP rate limiting is defeatable** with rotating proxies. The per-IP limit
  is a filter, not a guarantee.
- **The spend cap is the real guarantee.** If everything above fails, your
  loss is bounded by the number you set in step 1. That is why it comes first.
- **In-memory fallback is weak.** Until Upstash is configured, treat the rate
  limit as advisory.
