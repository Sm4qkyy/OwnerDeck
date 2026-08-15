# Adds the visual weight the page was missing: the product shown working, the
# verticals expanded into something that says "this is for you" whatever the
# reader runs, and a footer with structure.
#
# No invented figures. The conversation below carries no prices, because the
# brief's number rule allows only the three plan prices and the Limassol 14 —
# so it demonstrates the two things that need no number at all: the hour it
# replies at, and the language it replies in.
import io, re, sys

p = 'index.html'
t = io.open(p, encoding='utf-8').read()


def ico(d):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>')

CAR   = ico('<path d="M3 13l2-5a2 2 0 0 1 2-1h10a2 2 0 0 1 2 1l2 5"/><path d="M3 13h18v4H3z"/>'
            '<circle cx="7" cy="18" r="1.4"/><circle cx="17" cy="18" r="1.4"/>')
KEY   = ico('<circle cx="8" cy="12" r="4"/><path d="M12 12h9M18 12v3M15 12v2"/>')
BOAT  = ico('<path d="M3 17h18l-2 4H5z"/><path d="M12 3v11M12 5l6 9H6z"/>')
DIVE  = ico('<path d="M4 18c2 0 2-2 4-2s2 2 4 2 2-2 4-2 2 2 4 2"/><circle cx="12" cy="8" r="4"/>')
HOUSE = ico('<path d="M4 11l8-6 8 6"/><path d="M6 10v9h12v-9"/><path d="M10 19v-5h4v5"/>')
CLINIC= ico('<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M12 9v6M9 12h6"/>')
CHAIR = ico('<path d="M8 4v7a4 4 0 0 0 8 0V4"/><path d="M12 15v5M9 20h6"/>')
BED   = ico('<path d="M3 18v-6h18v6"/><path d="M3 12V8h7v4"/><path d="M14 12V8h7v4"/><path d="M3 18v2M21 18v2"/>')

TRADES = [
    (CAR,   'Car, scooter and buggy rental',
     'What is free on those dates, the rate for that many days, delivery to a hotel, insurance, the deposit.'),
    (BOAT,  'Boat charters and tours',
     'Half day or full, how many people, where you meet, what is included, and the weather call kept for you.'),
    (DIVE,  'Watersports and diving',
     'Certification level, group size, gear included or not, the times that still have space.'),
    (HOUSE, 'Villas and short-term rentals',
     'Which dates are open, how many guests, key handover, cleaning windows, the deposit.'),
    (KEY,   'Estate agencies',
     'Which viewings are free, the asking price, the area, and getting the appointment in the diary.'),
    (CLINIC,'Private clinics',
     'Which slots are open, which practitioner, how to prepare, what to bring, how long it takes.'),
    (CHAIR, 'Salons, barbers and spas',
     'Which service, which stylist, how long it takes, what it costs, and the next free slot.'),
    (BED,   'Guesthouses and small hotels',
     'Rooms free on those nights, breakfast, parking, late arrival, and the booking confirmed back.'),
]

trades_html = '\n'.join(
    '        <article class="trade" data-reveal="%d">\n'
    '          <h3 class="trade__h">%s<span>%s</span></h3>\n'
    '          <p>%s</p>\n'
    '        </article>' % (i * 40, svg, name, detail)
    for i, (svg, name, detail) in enumerate(TRADES))

# ---------------------------------------------------------------- showcase
WA  = ico('<path d="M4 20l1.3-4A8 8 0 1 1 8 18.7z"/>')
IG  = ico('<rect x="3.5" y="3.5" width="17" height="17" rx="4.5"/><circle cx="12" cy="12" r="3.6"/>'
          '<circle cx="17" cy="7" r="1" fill="currentColor" stroke="none"/>')
WEB = ico('<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5a13 13 0 0 1 0 17a13 13 0 0 1 0-17"/>')

SHOWCASE = """
  <!-- ============================================================
       3. Seeing it work
       ============================================================ -->
  <section class="section section--tint" id="seeing">
    <div class="wrap">
      <p class="eyebrow" data-reveal>What your customer sees</p>
      <div class="showcase">
        <div data-reveal="80">
          <h2>It answers like you would, at an hour you would not.</h2>
          <p class="lede">Same number your customers already have. It knows what you
            offer and when you are free, so the reply is a real answer rather than a
            promise to get back to them.</p>

          <p class="eyebrow" style="margin-top:var(--s6)">Where it answers</p>
          <div class="channels-row">
            <span class="channel-chip">%s WhatsApp</span>
            <span class="channel-chip">%s Instagram DMs</span>
            <span class="channel-chip">%s Website chat</span>
          </div>
        </div>

        <div class="phone" data-reveal="180">
          <div class="phone__screen">
            <div class="phone__bar">
              <span class="phone__av" aria-hidden="true">O</span>
              <span>
                <span class="phone__who">Your business</span>
                <span class="phone__state">online</span>
              </span>
            </div>
            <div class="phone__thread">
              <p class="thread__stamp">Saturday, 23:41</p>
              <p class="bubble bubble--them">Hi, are you open Saturday?</p>
              <p class="bubble bubble--us">Yes, Saturday is open. What time suits you?
                <span class="bubble__meta">Replied in two seconds</span></p>
              <p class="bubble bubble--them">Около 6, можно?</p>
              <p class="bubble bubble--us">Конечно. Записал вас на субботу, 18:00.
                Подтверждение отправлено.</p>
              <p class="thread__note">Language detected on its own. Nothing to set up.</p>
              <p class="bubble bubble--them">Спасибо</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
""" % (WA, IG, WEB)

CARDS_MARK = """  <!-- ============================================================
       3. The five cards, expanded"""
assert CARDS_MARK in t, 'cards marker not found'
t = t.replace(CARDS_MARK, SHOWCASE + """
  <!-- ============================================================
       4. The five cards, expanded""")

# ---------------------------------------------------------------- verticals
OLD_WHO = re.search(r'(?s)  <!-- =+\n       \d+\. Who it is for\n       =+ -->.*?</section>\n', t)
assert OLD_WHO, 'who-it-is-for section not found'

NEW_WHO = """  <!-- ============================================================
       Who it is for
       ============================================================ -->
  <section class="section" id="who">
    <div class="wrap">
      <p class="eyebrow" data-reveal>Who it is for</p>
      <h2 class="headline-tight" data-reveal="80">Anything with a price, a calendar and a customer waiting.</h2>
      <p class="lede" data-reveal="140">The questions change. The shape does not: someone
        wants to know if you are free, what it costs, and how to book it. Here is what
        that looks like in each.</p>

      <div class="trades" style="margin-top:var(--s6)">
%s
      </div>
    </div>
  </section>
""" % trades_html

t = t[:OLD_WHO.start()] + NEW_WHO + t[OLD_WHO.end():]

# ---------------------------------------------------------------- footer
OLD_FOOT = re.search(r'(?s)<footer class="footer">.*?</footer>', t)
assert OLD_FOOT, 'footer not found'

NEW_FOOT = """<footer class="footer">
  <div class="wrap">
    <div class="footer__cols">
      <div class="footer__brand">
        <p class="footer__mark">Ownerdeck</p>
        <p>The website, the enquiries, the bookings and the follow-up after —
          run from one set of facts about your business.</p>
      </div>
      <nav aria-label="Product">
        <p class="footer__h">Product</p>
        <a href="#cards">The five cards</a>
        <a href="#how">How setup works</a>
        <a href="#pricing">Pricing</a>
        <a href="#faq">Questions</a>
        <a href="/demo">See it work</a>
      </nav>
      <nav aria-label="Reading">
        <p class="footer__h">Reading</p>
        <a href="/whatsapp-bot-car-rental">For car rental</a>
        <a href="/whatsapp-booking-bot-boat-charter-tours">For charters and tours</a>
        <a href="/stop-losing-bookings-slow-whatsapp-replies">Slow replies cost bookings</a>
        <a href="/do-i-need-a-new-number-whatsapp-bot">Do I need a new number</a>
      </nav>
      <nav aria-label="Contact">
        <p class="footer__h">Get in touch</p>
        <a href="https://wa.me/447520689685" rel="noopener">WhatsApp</a>
        <a href="https://www.instagram.com/ownerdeckcy/" rel="noopener">Instagram</a>
        <a href="mailto:mark@ownerdeck.com">mark@ownerdeck.com</a>
      </nav>
    </div>
    <div class="footer__base">
      <span>&copy; 2026 Ownerdeck</span>
      <span class="footer__spacer"></span>
      <a href="/privacy">Privacy</a>
      <a href="/terms" rel="nofollow">Terms</a>
      <a href="/stats" rel="nofollow">&middot;</a>
    </div>
  </div>
</footer>"""

t = t[:OLD_FOOT.start()] + NEW_FOOT + t[OLD_FOOT.end():]

io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('index.html: showcase, %d trades and a structured footer' % len(TRADES))
