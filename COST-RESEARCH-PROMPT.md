# Cost research brief — Ownerdeck

The pricing model in `_margins.py` works, but most of what it rests on is
marked `ASSUMED` and has never been checked against a published figure. This
brief exists to replace those guesses with sourced numbers, so a pricing
decision can be made on evidence rather than on my estimates.

Paste everything below the line into an AI with live web access.

---

## The brief

You have web access. Establish the **real, current, sourced** cost of running
the business below, then say what pricing structure is solvent.

### The business

**Ownerdeck** builds and then runs the online side of small owner-operated
businesses in Cyprus — car, scooter and boat rental, tours, villas,
guesthouses, clinics, salons. Run by **one person, a sole trader**, working
remotely.

Each client gets some or all of: a website, a database behind it, an AI
assistant answering on WhatsApp, Instagram DMs and website chat, bookings with
deposits and a calendar, a Google Business Profile, and follow-up campaigns.

Current pricing: €600 build + €99/month; €1,900 + €249/month; €2,400 +
€299/month. Not VAT registered.

### What the current model assumes, and what needs checking

Every figure below is currently a guess. Find the real one, cite it, and say
how far off the guess is.

| Assumption | Currently modelled as | What to establish |
|---|---|---|
| AI model cost | Claude Haiku 4.5, ~$1/$5 per MTok, 250 conversations/client/month, 8 messages each, 5,000 input and 300 output tokens per message, prompt caching on 70% of input | Current published Anthropic prices; whether caching applies at this prompt size; realistic token counts for this kind of assistant |
| WhatsApp messaging | €0.03 per utility template message, applied to 25% of conversations | Meta's **current** WhatsApp Business Platform pricing for Cyprus. Note: Meta moved from conversation-based to per-message pricing during 2025 — establish what actually applies now, and what is free |
| Instagram messaging | Not modelled at all | Whether Meta charges for Instagram Messaging API at this volume |
| Hosting | €2/month per client | Real cost of hosting a small static site plus serverless functions at this scale (Vercel, Netlify, Cloudflare) |
| Database | €3/month per client | Real cost of small managed Postgres per client (Supabase, Neon, Railway) including whether free tiers are viable commercially |
| Domain | €1.20/month | Typical `.com` and `.com.cy` registration and renewal |
| Payment processing | Stripe at 1.5% + €0.25 | Stripe's **actual** published rates for a Cyprus business, EU cards and non-EU cards separately |
| Support time | 0.75–2 hours per client per month | Any published benchmark for ongoing support load on managed web or chatbot services |
| Target hourly | €45/hour, **before tax** | See the section below — this is the biggest gap |

### The gap the current model ignores entirely: tax

The model targets €45/hour and treats that as take-home. It is not. For a
**sole trader in the Republic of Cyprus**, establish:

- Income tax bands and rates currently in force.
- Social Insurance contribution rate for a self-employed person, and how the
  notional income brackets work.
- GESY (General Healthcare System) contribution rate for the self-employed.
- Any other mandatory contribution.
- The **VAT registration threshold**, and what changes at the point it is
  crossed — Ownerdeck is not registered, so the level at which it must be
  matters directly to pricing.
- Whether a sole trader can deduct these hosting, API and software costs
  against income, and what records are required.

Then answer plainly: **to clear €45/hour net, what must be charged gross?**

### Volume, which nobody has measured

The model assumes 250 conversations per client per month. Find whatever
evidence exists for:

- Typical enquiry volume for a small car or scooter rental operator, a boat
  charter, a villa, a salon — in season and out of it.
- How seasonal Cyprus tourism actually is, month by month, and therefore how
  far a summer figure over-states an annual average.
- What proportion of enquiries arrive outside business hours, since that is
  the claim the whole product rests on.

If no reliable public figure exists for a line, say so rather than estimating.

### Then answer the actual question

1. **What does one client of each tier genuinely cost per month**, with tax
   and every fee included? Give a range, not a point estimate, and show the
   working.
2. **What is the true break-even** on each tier — the month at which the build
   hours are recovered?
3. **How many clients before this replaces a salary?** State the salary you
   are assuming and where you got it.
4. **Is the current pricing solvent?** If yes, at what churn rate does it stop
   being solvent?
5. **What structure would you recommend**, given that the competitive research
   found the €1,900–€2,400 upfront to be a severe outlier against a market
   where UENI charges $79 setup and Visito charges nothing? Model it: setup,
   monthly, minimum term, and what is left if a client leaves the day the term
   ends.
6. **What is the single largest cost risk** — the line that, if the guess is
   badly wrong, breaks the model?

### Rules on evidence

- **A URL for every figure.** Prefer the vendor's or the government's own
  page over a summary, a blog or a comparison site.
- **Never invent a rate, a threshold or a percentage.** If it is not
  published, write "not published" and say where you looked.
- **Date every tax and pricing figure**, and say which year it applies to.
  Cyprus tax bands and Meta's messaging prices have both moved recently.
- **Separate observed from inferred**, and mark inferences as such.
- **Say what you could not check.** A short honest answer beats a confident
  wrong one, and a wrong cost figure here produces a price that loses money on
  every client.
- Where a cost depends on volume, give the formula rather than a single
  number.

### Output

1. A table replacing every `ASSUMED` line above with a sourced figure, the
   URL, the date, and how far the current guess was off.
2. The six answers, with working shown.
3. A one-paragraph verdict: is the current pricing safe, and if not, what is
   the smallest change that makes it safe?

Keep it under 2,000 words. Leave a section thin if the evidence is thin, and
say why.
