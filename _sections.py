# Header (theme toggle + mobile menu) and two new sections for index.html.
# Kept as a script so the exact markup is reviewable rather than buried in a diff.
import io, sys

p = 'index.html'
t = io.open(p, encoding='utf-8').read()

# ---------------------------------------------------------------- head script
OLD_HEAD = """<!-- Marks that scripting is available. Every motion rule in brand.css is
     scoped to .js, so with this line unreached the page still renders in
     full rather than waiting for a class JavaScript never adds. -->
<script>document.documentElement.classList.add('js')</script>"""

NEW_HEAD = """<!-- Runs before first paint, and does two things.
     .js marks that scripting is available: every motion rule in brand.css is
     scoped to it, so with this line unreached the page still renders in full
     rather than waiting for a class JavaScript never adds.
     data-theme is read here rather than in motion.js because a deferred script
     would repaint the page light-then-dark on every load. -->
<script>
(function () {
  var r = document.documentElement;
  r.classList.add('js');
  try {
    var t = localStorage.getItem('od_theme');
    if (t === 'light' || t === 'dark') r.setAttribute('data-theme', t);
  } catch (e) {}
})();
</script>"""

assert OLD_HEAD in t, 'head bootstrap not found'
t = t.replace(OLD_HEAD, NEW_HEAD)

# ---------------------------------------------------------------- header
OLD_HEADER = """<header class="masthead">
  <div class="wrap masthead__bar">
    <a class="masthead__mark" href="/">Ownerdeck</a>
    <nav class="masthead__nav" aria-label="Sections">
      <a href="#cards">The cards</a>
      <a href="#pricing">Pricing</a>
      <a href="#faq">Questions</a>
    </nav>
    <a class="btn btn--quiet masthead__cta" href="#pricing">See pricing</a>
  </div>
</header>"""

SUN = ('<svg class="ic-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
       'stroke-width="1.7" stroke-linecap="round" aria-hidden="true">'
       '<circle cx="12" cy="12" r="4.2"/>'
       '<path d="M12 2.2v2M12 19.8v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4'
       'M2.2 12h2M19.8 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>')
MOON = ('<svg class="ic-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>')

NEW_HEADER = """<header class="masthead">
  <div class="wrap masthead__bar">
    <a class="masthead__mark" href="/">Ownerdeck</a>
    <nav class="masthead__nav" aria-label="Sections">
      <a href="#cards">The cards</a>
      <a href="#how">Setup</a>
      <a href="#pricing">Pricing</a>
      <a href="#faq">Questions</a>
    </nav>
    <div class="masthead__tools">
      <button id="theme-toggle" class="icon-btn" type="button" aria-label="Switch theme">
        %s%s
      </button>
      <a class="btn btn--quiet masthead__cta" href="#pricing">See pricing</a>

      <!-- <details> rather than a scripted panel: it opens, closes and takes
           keyboard focus with no JavaScript at all. motion.js only adds
           close-on-navigate and close-on-Escape. -->
      <details class="mmenu">
        <summary class="mmenu__trigger" aria-label="Open menu">
          <span class="mmenu__bars" aria-hidden="true"><i></i></span>
        </summary>
        <div class="mmenu__panel">
          <a href="#cards">The five cards</a>
          <a href="#how">How setup works</a>
          <a href="#pricing">Pricing</a>
          <a href="#faq">Questions</a>
          <a href="#who">Who it is for</a>
          <a href="/demo">See it work</a>
          <a class="btn btn--primary od-btn--primary"
             href="https://wa.me/447520689685?text=Hi%%20Mark%%20%%E2%%80%%94%%20I%%20saw%%20Ownerdeck%%20and%%20I%%27d%%20like%%20to%%20know%%20more."
             rel="noopener">Message me on WhatsApp</a>
          <p class="mmenu__note">mark@ownerdeck.com</p>
        </div>
      </details>
    </div>
  </div>
</header>""" % (SUN, MOON)

assert OLD_HEADER in t, 'header not found'
t = t.replace(OLD_HEADER, NEW_HEADER)

# ---------------------------------------------------------------- what it does not do
NOTDO = """
  <!-- ============================================================
       4. What it does not do
       ============================================================ -->
  <section class="section" id="limits">
    <div class="wrap">
      <p class="eyebrow" data-reveal>Where it stops</p>
      <div class="split split--wide-right">
        <h2 data-reveal="80">And the things it does not do, plainly.</h2>
        <div data-reveal="160">
          <ul class="notdo">
            <li><strong>It does not take payment.</strong> Deposits and balances stay
              between you and your customer.</li>
            <li><strong>It does not handle complaints or disputes.</strong> Those reach
              you, as they should.</li>
            <li><strong>It does not manage your contracts or your diary.</strong> It
              reads your availability; it does not run your office.</li>
            <li><strong>It does not replace anyone on your team.</strong> The person
              answering at 11pm is you, and this gives you that hour back.</li>
            <li><strong>It does not invent a price.</strong> It quotes from your own
              numbers or it says it needs to check.</li>
            <li><strong>It does not guess.</strong> A question outside what you have
              told it gets handed to you, and you see every one in the log.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
"""

# ---------------------------------------------------------------- setup
def ico(paths):
    return ('<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.4" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            + paths + '</svg>')

TALK = ico('<path d="M8 11h32v22H23l-9 8v-8H8Z"/><path d="M15 19h18M15 25h12"/>')
BUILD = ico('<path d="M24 6 8 14v12c0 8 7 14 16 16 9-2 16-8 16-16V14Z"/>'
            '<path d="M17 24l5 5 10-11"/>')
LIVE = ico('<rect x="14" y="5" width="20" height="38" rx="3"/>'
           '<path d="M22 10h4"/><path d="M18 22h12M18 28h8"/><circle cx="24" cy="37" r="1.4"/>')

HOW = """
  <!-- ============================================================
       7. How setup works
       ============================================================ -->
  <section class="section" id="how">
    <div class="wrap">
      <p class="eyebrow" data-reveal>How setup works</p>
      <h2 class="headline-tight" data-reveal="80">One conversation, then it is running.</h2>

      <div class="steps" style="margin-top:var(--s7)">
        <article class="step-card" data-reveal>
          <p class="step-card__n"></p>
          <div class="step-card__ico">%s</div>
          <h3>You tell me about the business</h3>
          <p>What you offer, your prices, your hours, your policies, your photos. Once,
            in your own words. That is your part of it.</p>
        </article>

        <article class="step-card" data-reveal="110">
          <p class="step-card__n"></p>
          <div class="step-card__ico">%s</div>
          <h3>I build it and test it</h3>
          <p>On your own number, against your real prices, checked properly before a
            single customer sees it. If your availability lives in a spreadsheet, that
            works too.</p>
        </article>

        <article class="step-card" data-reveal="220">
          <p class="step-card__n"></p>
          <div class="step-card__ico">%s</div>
          <h3>It goes live, and nothing changes</h3>
          <p>Same number on your cards, same listing, same customers. The difference is
            that the messages get answered and the bookings arrive on your phone.</p>
        </article>
      </div>
    </div>
  </section>
""" % (TALK, BUILD, LIVE)

# --- insert: limits after the cards section, how before pricing ---
CARDS_END = """    </div>
  </section>

  <!-- ============================================================
       4. The problem"""
assert CARDS_END in t, 'cards/problem seam not found'
t = t.replace(CARDS_END, """    </div>
  </section>
""" + NOTDO + """
  <!-- ============================================================
       5. The problem""")

PRICING_START = """  <!-- ============================================================
       6. Pricing"""
assert PRICING_START in t, 'pricing seam not found'
t = t.replace(PRICING_START, HOW + """
  <!-- ============================================================
       8. Pricing""")

io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('index.html: header, #limits and #how written')
