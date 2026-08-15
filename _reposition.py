# Repositions the homepage: Ownerdeck builds the online essentials — website,
# database, AI chat assistant, bookings, Google listing — rather than selling
# one assistant.
#
# The deck motif survives the change better than it survived the last one: the
# name is a deck of cards, and "services you add as you grow" is exactly what a
# hand of cards is. Only what the cards CONTAIN changes.
#
# Pricing is now setup + monthly, because _margins.py showed a monthly-only
# price never repays a 36-hour build inside a year.
import io, re

p = 'index.html'
t = io.open(p, encoding='utf-8').read()


def ico(d):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>')

I_SITE = ico('<rect x="3" y="4" width="18" height="15" rx="2"/><path d="M3 9h18"/>'
             '<path d="M6.5 6.5h.01M9 6.5h.01"/>')
I_DATA = ico('<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6"/>'
             '<path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>')
I_ANS  = ico('<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12.5h5"/>')
I_BOOK = ico('<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>'
             '<path d="M8.5 14.5l2 2 4-4"/>')
I_REACH= ico('<path d="M12 21s7-5.4 7-11a7 7 0 1 0-14 0c0 5.6 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>')

SERVICES = [
    ('site',   'Site',   I_SITE,
     'A fast website, designed and built for you. It reads live from your database, '
     'so the prices on it are the prices you actually charge.',
     'Most owners have a site nobody has opened the code of in years.'),
    ('data',   'Data',   I_DATA,
     'One database behind everything. Services, prices, availability, customers and '
     'bookings in one place instead of a spreadsheet, a notebook and your head.',
     'This is the part that makes the rest of it possible.'),
    ('answer', 'Answer', I_ANS,
     'An AI chat assistant on WhatsApp, Instagram DMs and your own site. It answers '
     'in any language, at any hour, from your real prices and real availability.',
     'Every customer message answered — even at 2am.'),
    ('book',   'Book',   I_BOOK,
     'Real availability, confirmations, deposits and a calendar that fills itself. '
     'The booking lands on your phone the moment it happens.',
     'For anyone still confirming every booking by hand.'),
    ('reach',  'Reach',  I_REACH,
     'Google Business Profile set up properly so you turn up in the map, and a review '
     'request sent after every booking.',
     'For anyone who has never claimed their listing.'),
]

# ---------------------------------------------------------------- hero deck
hero_cards = '\n'.join(
    '            <li class="card" style="--pip: var(--%s)">\n'
    '              <span class="card__pip" aria-hidden="true"></span>\n'
    '              <p class="card__name">%s</p>\n'
    '              <p class="card__line">%s</p>\n'
    '            </li>' % (key, name, short)
    for key, name, short in [
        ('site',   'Site',   'A website that never goes stale.'),
        ('book',   'Data',   'One database behind everything.'),
        ('answer', 'Answer', 'An AI assistant on every channel.'),
        ('return', 'Book',   'Availability, deposits, calendar.'),
        ('reach',  'Reach',  'Google listing, and the reviews after.'),
    ])

OLD_DECK = re.search(r'(?s)          <ul class="deck deck--fan".*?</ul>', t)
assert OLD_DECK, 'hero deck not found'
t = t[:OLD_DECK.start()] + (
    '          <ul class="deck deck--fan" aria-labelledby="deck-label">\n'
    + hero_cards + '\n          </ul>') + t[OLD_DECK.end():]

# ---------------------------------------------------------------- headline + lede
t = t.replace('<h1 data-split>Ownerdeck runs the online side of your business.</h1>',
              '<h1 data-split>We build the online side of your business.</h1>')
t = t.replace(
"""            Tell it about your business once — what you offer, your prices, your hours,
            your photos. That one set of facts becomes your website, answers your
            messages, quotes your prices and takes your bookings.""",
"""            Website, database, AI chat assistant, bookings, Google listing. Built for
            you, wired to one set of facts about your business, and run for you after.
            Take the ones you need and add the rest when you are ready.""")

# ---------------------------------------------------------------- services section
services_html = '\n'.join(
    '        <li class="card" style="--pip: var(--%s)" data-reveal="%d">\n'
    '          <span class="card__pip" aria-hidden="true"></span>\n'
    '          <div class="card__ico">%s</div>\n'
    '          <h3 class="card__name">%s</h3>\n'
    '          <p class="card__line">%s</p>\n'
    '          <p class="card__who">%s</p>\n'
    '        </li>' % (key, i * 90, icon, name, long, short)
    for i, (key, name, icon, long, short) in enumerate(SERVICES))

OLD_CARDS = re.search(r'(?s)      <ul class="deck deck--list">.*?</ul>', t)
assert OLD_CARDS, 'expanded card list not found'
t = t[:OLD_CARDS.start()] + (
    '      <ul class="deck deck--list">\n' + services_html + '\n      </ul>') + t[OLD_CARDS.end():]

t = t.replace('<p class="eyebrow" data-reveal>The five cards</p>',
              '<p class="eyebrow" data-reveal>What we build</p>')
t = t.replace('<h2 class="headline-tight" data-reveal="80">Start with a hand. Add cards as you grow.</h2>',
              '<h2 class="headline-tight" data-reveal="80">Five services. Start with a hand, add cards as you grow.</h2>')

# ---------------------------------------------------------------- pricing
OLD_PRICING = re.search(
    r'(?s)      <div class="plans">.*?      <div class="pricing__note"[^>]*>.*?\n      </div>', t)
assert OLD_PRICING, 'pricing block not found'

NEW_PRICING = """      <div class="plans">
        <article class="plan" data-spotlight data-reveal>
          <h3 class="plan__name">Answer</h3>
          <p class="plan__price">&euro;600 <span>setup</span></p>
          <p class="plan__then">then &euro;150 / month</p>
          <p class="plan__what"><strong>The AI chat assistant.</strong> On WhatsApp,
            Instagram DMs and your existing site. Any language, any hour.</p>
        </article>

        <article class="plan plan--common" data-spotlight data-reveal="110">
          <p class="plan__tag">The common choice</p>
          <h3 class="plan__name">Deck</h3>
          <p class="plan__price">&euro;1,800 <span>setup</span></p>
          <p class="plan__then">then &euro;249 / month</p>
          <p class="plan__what"><strong>Site + Data + Answer + Book.</strong> The website,
            the database behind it, the assistant answering, and the bookings landing on
            your phone.</p>
        </article>

        <article class="plan" data-spotlight data-reveal="220">
          <h3 class="plan__name">Full Deck</h3>
          <p class="plan__price">&euro;2,400 <span>setup</span></p>
          <p class="plan__then">then &euro;299 / month</p>
          <p class="plan__what"><strong>All five.</strong> Everything above, plus your
            Google listing set up properly and a review request after every booking.</p>
        </article>
      </div>

      <div class="pricing__note" data-reveal>
        <p><strong>Starting from nothing?</strong> Everything built from zero in a week,
          no setup fee, &euro;249 a month on a twelve month term. The build is paid for
          across the year instead of up front.</p>
        <p class="pricing__terms">No VAT. The monthly covers hosting, the database, the
          assistant and the changes you ask for. Cancel a monthly-only plan any time.</p>
      </div>"""

t = t[:OLD_PRICING.start()] + NEW_PRICING + t[OLD_PRICING.end():]

# ---------------------------------------------------------------- title / meta
t = t.replace('<title>Ownerdeck — website, enquiries and bookings, run for you</title>',
              '<title>Ownerdeck — websites, databases and AI chat assistants for small business</title>')
t = re.sub(r'<meta name="description" content="[^"]*">',
           '<meta name="description" content="We build the online side of your business: '
           'a fast website, the database behind it, an AI chat assistant on WhatsApp and '
           'Instagram, real bookings and your Google listing. From &euro;150 a month.">', t, count=1)
for a, b in [
    ('<meta property="og:title" content="Ownerdeck — website, enquiries and bookings, run for you">',
     '<meta property="og:title" content="Ownerdeck — websites, databases and AI chat assistants">'),
    ('<meta name="twitter:title" content="Ownerdeck — website, enquiries and bookings, run for you">',
     '<meta name="twitter:title" content="Ownerdeck — websites, databases and AI chat assistants">'),
]:
    t = t.replace(a, b)
t = re.sub(r'<meta property="og:description" content="[^"]*">',
           '<meta property="og:description" content="Website, database, AI chat assistant, '
           'bookings and Google listing. Built for you and run for you after.">', t, count=1)
t = re.sub(r'<meta name="twitter:description" content="[^"]*">',
           '<meta name="twitter:description" content="The online side of your business, '
           'built and run.">', t, count=1)

# JSON-LD offers now carry a setup price too.
t = t.replace('"description": "Ownerdeck runs the online side of a small tourism business: '
              'the website, the enquiries, the bookings and the follow-up after."',
              '"description": "Ownerdeck builds and runs the online side of a small business: '
              'the website, the database behind it, an AI chat assistant, the bookings and '
              'the Google listing."')

io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('index.html repositioned: 5 services, setup + monthly pricing, new meta')
