# Page content for _build_site.py.
#
# Only the <main> body of each page lives here. Head, header, footer, call to
# action band and page navigation are assembled by the builder.
#
# `data-t` marks an element as translatable. The builder turns it into a
# content-hashed data-i18n key. Put it only on elements whose contents are
# plain text — translations are applied through textContent, which would wipe
# out any nested markup.
import io
import os

import _legal

HERE = os.path.dirname(os.path.abspath(__file__))


def img_size(slug):
    """Real pixel dimensions, read from the file.

    These were hardcoded, and hardcoded wrong — every strip tile claimed
    1024x1024 and every trade tile 1600x1067, when the photos range from
    680x1024 to 1600x1200. The containers use aspect-ratio and object-fit so
    nothing rendered badly, but width/height on an <img> is a statement about
    the file, and a wrong one is worse than none.
    """
    path = os.path.join(HERE, 'img', slug + '.webp')
    try:
        from PIL import Image
        with Image.open(path) as im:
            return ' width="%d" height="%d"' % im.size
    except Exception:
        # No Pillow, or no file. Omit rather than guess — the CSS reserves the
        # box either way.
        return ''


def _frag(name):
    """Demo's body, page styles and stepper script still live in their own
    files. They are page-specific and long, and inlining them here would bury
    the rest of the content."""
    with io.open(os.path.join(HERE, name), encoding='utf-8') as f:
        return f.read()

TICK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M20 6 9 17l-5-5"/></svg>')


def icon(paths):
    return ('<svg class="dcard__i" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true">%s</svg>' % paths)


# The five cards, plus the data layer they all read from.
CARDS = [
    ('answer', 'Answer',
     'Enquiries handled on WhatsApp, Instagram DMs and website chat. Any language, any hour.',
     'Owners who lose bookings to slow replies.',
     '<path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 8.9 8.9 0 0 1-4-.9L3 21l1.9-4.9A8.4 8.4 0 0 1 12 3a8.4 8.4 0 0 1 9 8.5Z"/>'),
    ('site', 'Site',
     'A fast website that reads live from your prices, so it never goes stale.',
     'Anyone whose website has not been touched in years.',
     '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M7 6.5h.01"/>'),
    ('book', 'Book',
     'Real availability, confirmations, deposits and a calendar that fills itself in.',
     'Businesses still taking bookings by phone and paper.',
     '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 11h18M9 16l2 2 4-4"/>'),
    ('reach', 'Reach',
     'Your Google listing set up properly, and a review request after every booking.',
     'Owners who are hard to find and rarely reviewed.',
     '<circle cx="12" cy="10.5" r="3"/><path d="M20 10.5c0 6-8 11.5-8 11.5S4 16.5 4 10.5a8 8 0 1 1 16 0Z"/>'),
    ('return', 'Return',
     'Reminders, off-season offers, and past customers who come back.',
     'Seasonal businesses with quiet months to fill.',
     '<path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 3v6h-6"/>'),
]

TRADES = [
    ('car',        'Car and 4x4 rental',
     'A grey SUV parked side-on against a concrete wall',
     'Fleet, day rates, insurance and delivery, all answered from one price list.'),
    ('scooter',    'Scooter and bike hire',
     'Four electric scooters in a row against a concrete wall',
     'Walk-ups and day hires without the phone ringing all afternoon.'),
    ('boat',       'Boat and jetski charter',
     'A white rigid inflatable boat moored at a concrete pontoon',
     'Half-day and full-day slots, weather holds, deposits taken up front.'),
    ('diving',     'Tours, excursions and diving',
     'Dive gear on a quay — tank, buoyancy jacket, regulator and fins',
     'Group sizes, pick-up points and departure times that stay in step.'),
    ('villa-pool', 'Villas and short-term rentals',
     'Loungers beside an infinity pool looking out to sea',
     'Nightly rates by season, minimum stays and availability that is actually true.'),
    ('hotel',      'Guesthouses and small hotels',
     'A made bed by a floor-to-ceiling window with a sea view',
     'Room types, breakfast, late check-out — asked and answered at 2am.'),
    ('estate',     'Estate agencies',
     'Modern flat-roofed houses stepping up a slope',
     'Listings that stay current and viewings booked without the back and forth.'),
    ('clinic',     'Private clinics',
     'A treatment couch and stool in a bright, empty room',
     'Appointment slots, first-visit questions and reminders that cut no-shows.'),
    ('salon',      'Salons and spas',
     'Black scissors, comb and clips laid on a stone counter',
     'Treatments, durations and prices, with the diary kept full.'),
    ('restaurant', 'Restaurants and tavernas',
     'A table for two on a terrace, laid before service',
     'Covers, sittings and the same three questions every evening.'),
    ('watersports', 'Watersports rental',
     'Paddleboards stacked upright on pale sand',
     'Hourly hires, weather calls and kit back before sunset.'),
    ('fitness',    'Fitness and yoga studios',
     'Rolled exercise mats against a concrete wall',
     'Class times, drop-ins and memberships without a spreadsheet.'),
    ('photographer', 'Photographers and studios',
     'A camera on a tripod facing a large window',
     'Shoot dates, packages and deposits agreed before the call.'),
    ('dentist',    'Dentists',
     'A modern dental chair beside a window',
     'Appointments, first-visit questions and reminders that cut no-shows.'),
    ('barber',     'Barbers',
     'A black barber chair facing a frameless mirror',
     'Walk-ins, regulars and a diary that fills itself.'),
]


def deck_grid(link=True):
    out = []
    for slug, name, line, _for, path in CARDS:
        tag = 'a' if link else 'div'
        href = ' href="/what-we-build#%s"' % slug if link else ''
        out.append(
            f'        <{tag} class="dcard"{href} data-reveal>{icon(path)}'
            f'<span class="dcard__name" data-t>{name}</span>'
            f'<span class="dcard__line" data-t>{line}</span></{tag}>')
    return '\n'.join(out)


# Six of the nine trades, for the home page. Recognition beats completeness
# here — the full set lives on /who-its-for.
# Six of the fifteen, for the home page. Rental first, because that is what the
# headline now leads with, then enough breadth to show it is not only rental.
STRIP = ['car', 'scooter', 'boat', 'villa-pool', 'clinic', 'salon']


def strip_grid():
    by_slug = {t[0]: t for t in TRADES}
    out = []
    for slug in STRIP:
        _s, name, alt, _line = by_slug[slug]
        out.append(
            f'        <li data-reveal><figure>'
            f'<div class="strip__img"><img src="/img/{slug}.webp"{img_size(slug)} '
            f'loading="lazy" decoding="async" alt="{alt}"></div>'
            f'<figcaption data-t>{name}</figcaption></figure></li>')
    return '\n'.join(out)


# Floating cards behind the hero. The brand is a deck, so the ambient shapes
# are cards — not abstract blobs, and not a 3D model that would need a library
# the CSP forbids and would fight a flat monochrome design.
#
# Each carries a depth: od.js multiplies the scroll offset by it, so they drift
# at different rates and the hero gains a little parallax. Negative depths move
# against the scroll. They are decorative and aria-hidden.
FLOATERS = [
    # (icon slug, top%, left%, rotation deg, depth, scale)
    ('answer', 14,  3, -12, 0.22, 1.0),
    ('book',   64,  9,   8, -0.16, 0.8),
    ('site',    6, 44,  14, 0.30, 0.7),
    ('return', 78, 38, -6, 0.12, 0.85),
    ('reach',  30, 92,  10, -0.24, 0.75),
]


def hero_floaters():
    """Two nested elements on purpose.

    The outer .floater is the only thing od.js touches: it writes --shift on
    scroll and the transform on that element consumes it. The inner card owns
    the idle drift and the 3D tilt, as a keyframe animation.

    They cannot share an element. An animation takes ownership of transform for
    as long as it runs and outranks an ordinary declaration, so a float
    keyframe on .floater would silently kill the scroll parallax — the same
    trap that killed the hover tilt on the old deck.
    """
    paths = {c[0]: c[4] for c in CARDS}
    out = []
    for i, (slug, _top, _left, rot, depth, scale) in enumerate(FLOATERS):
        # Negative delays start every card at a different point in its cycle,
        # so they are already spread out on the first frame instead of rising
        # together and drifting apart over the first half minute.
        # Rounded, because 7.5 + 3 * 1.4 in binary floating point is
        # 11.700000000000001 and that lands verbatim in the shipped markup.
        dur = round(7.5 + i * 1.4, 2)
        delay = round(-(i * 2.3), 2)
        out.append(
            f'        <span class="floater" data-depth="{depth}" aria-hidden="true" '
            f'style="--f-c:var(--f-{slug})">'
            f'<span class="floater__card" style="--rot:{rot}deg;--scale:{scale};'
            f'--dur:{dur}s;--delay:{delay}s">'
            f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" '
            f'stroke-linecap="round" stroke-linejoin="round">{paths[slug]}</svg>'
            f'</span></span>')
    return '\n'.join(out)


def chat_mock():
    return '''<div class="mock" data-reveal="120">
          <div class="mock__bar">
            <span class="mock__title" data-t>Answer</span>
            <span class="mock__meta">WHATSAPP &middot; 02:14</span>
          </div>
          <div class="mock__body">
            <p class="bub bub--them" data-t>Do you have a jeep for tomorrow? What&rsquo;s the price for 3 days?</p>
            <p class="bub bub--us" data-t>Yes — a Suzuki Jimny is free tomorrow. Three days is &euro;135, insurance included. Want me to hold it?</p>
            <p class="bub bub--them" data-t>Yes please</p>
          </div>
          <div class="mock__foot">
            <span class="mock__tick">%s</span>
            <span data-t>Booking confirmed. Deposit taken, added to the July calendar.</span>
          </div>
        </div>''' % TICK


def pages(WA, ARROW, EMAIL):
    P = []

    # ------------------------------------------------------------- index
    P.append(dict(
        slug='index', in_flow=False,
        nav='Home',
        title='Ownerdeck — run the online side of your business',
        desc='We build and run the online side of your business: the website, '
             'the database behind it, an AI assistant answering your messages, '
             'the bookings and the follow-up. Set your prices once.',
        body=f'''  <section class="section section--hero" id="hero">
    <div class="hero__field" aria-hidden="true">
{hero_floaters()}
    </div>
    <div class="wrap">
      <div class="split">
        <div>
          <h1 data-t>Run the online side of your rental business.</h1>
          <p class="lede" data-reveal="80" data-t>Car, scooter and boat hire, answered at 2am. Ownerdeck runs the website, the enquiries, the bookings and the follow-up after — so the questions that arrive while you are asleep are already dealt with by morning.</p>

          <div class="cred" data-reveal="140">
            <span class="cred__n">14</span>
            <span class="cred__l" data-t>enquiries booked between 9pm and 8am last month, for one car rental operator in Limassol</span>
          </div>

          <div class="btn-row" data-reveal="200" style="margin-top:2rem">
            <a class="btn btn--primary" href="/demo"><span data-t>See it work</span>{ARROW}</a>
            <a class="btn btn--ghost" href="/start" data-t>Get started</a>
          </div>
          <p class="note" data-reveal="240" style="margin-top:1.25rem" data-t>No VAT. No long contract on the entry plan. Works the same way for villas, clinics and salons — see who it is for.</p>
        </div>
        <div class="emblem-wrap">
          <div class="emblem" role="img" aria-label="The Ownerdeck monogram"></div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--edge">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow" data-t>The reality</p>
        <h2 data-t>The online side runs whether you are watching or not.</h2>
      </div>
      <ol class="numbered">
        <li data-reveal><b>01</b><span data-t>Enquiries arrive at 11pm and wait until morning.</span></li>
        <li data-reveal><b>02</b><span data-t>Prices are out of date in three different places.</span></li>
        <li data-reveal><b>03</b><span data-t>Customers move on while they wait for a reply.</span></li>
        <li data-reveal><b>04</b><span data-t>The website has not been touched since it was built.</span></li>
      </ol>
    </div>
  </section>

  <section class="section section--sunk section--edge">
    <div class="wrap">
      <div class="split">
        <div>
          <p class="eyebrow" data-t>The one idea</p>
          <h2 data-t>Tell it once. It runs everything.</h2>
          <p class="lede" data-t>You give Ownerdeck the facts about your business one time. That single set of facts becomes everything your customers see. Change a price in one place and everything says the same thing.</p>
          <div class="btn-row" style="margin-top:2rem">
            <a class="btn btn--ghost" href="/how-it-works"><span data-t>How it fits together</span>{ARROW}</a>
          </div>
        </div>
        <div class="grid grid--2">
          <div class="tile" data-reveal>
            <p class="eyebrow" style="margin:0" data-t>What you tell us once</p>
            <ul class="chips">
              <li class="chip" data-on="1" data-t>Services</li><li class="chip" data-on="1" data-t>Prices</li>
              <li class="chip" data-on="1" data-t>Availability</li><li class="chip" data-on="1" data-t>Hours</li>
              <li class="chip" data-on="1" data-t>Policies</li><li class="chip" data-on="1" data-t>Photos</li>
            </ul>
          </div>
          <div class="tile" data-reveal>
            <p class="eyebrow" style="margin:0" data-t>What it runs</p>
            <ul class="chips">
              <li class="chip" data-on="1" data-t>Website</li><li class="chip" data-on="1" data-t>Messages</li>
              <li class="chip" data-on="1" data-t>Bookings</li><li class="chip" data-on="1" data-t>Google</li>
              <li class="chip" data-on="1" data-t>Follow-up</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--edge">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow" data-t>The deck</p>
        <h2 data-t>Five cards. One system.</h2>
        <p class="lede" data-t>Start with the card you need and add the rest as you grow. Each one reads from the same set of facts.</p>
      </div>
      <div class="deck deck--row">
{deck_grid()}
      </div>
      <div class="btn-row" style="margin-top:2.5rem">
        <a class="btn btn--ghost" href="/what-we-build"><span data-t>What each card does</span>{ARROW}</a>
      </div>
    </div>
  </section>

  <section class="section section--sunk section--edge">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow" data-t>Who we build for</p>
        <h2 data-t>You have answered these questions a thousand times.</h2>
        <p class="lede" data-t>Different trades, the same four questions all day. What does it cost. Is it free on Saturday. Do you deliver. Can I pay a deposit now.</p>
      </div>
      <ul class="strip">
{strip_grid()}
      </ul>
      <div class="btn-row" style="margin-top:2.5rem">
        <a class="btn btn--ghost" href="/who-its-for"><span data-t>Every trade we build for</span>{ARROW}</a>
      </div>
    </div>
  </section>

  <section class="section section--edge">
    <div class="wrap">
      <div class="split">
        <div data-reveal>
          <p class="eyebrow" data-t>Proof &middot; Limassol</p>
          <div class="stat">
            <span class="stat__n">14</span>
            <span class="stat__l" data-t>enquiries booked between 9pm and 8am last month</span>
          </div>
          <p class="lede" style="margin-top:2rem" data-t>A car rental operator in Limassol, live at &euro;150 a month. The after-hours coverage booked those 14 enquiries automatically — ones the owner would otherwise have picked up the next morning, if they were still waiting.</p>
        </div>
        <div class="ledger" data-reveal="120">
          <div class="ledger__row"><span class="mono">LAST 30 DAYS</span><b data-t>Car rental, Limassol</b></div>
          <div class="ledger__row"><span data-t>Enquiries answered</span><b>212</b></div>
          <div class="ledger__row"><span data-t>Answered after hours</span><b>14</b></div>
          <div class="ledger__row"><span data-t>Average reply time</span><b data-t>under a minute</b></div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--sunk section--edge">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow" data-t>No lock-in</p>
        <h2 data-t>You own all of it.</h2>
        <p class="lede" data-t>The usual worry about handing your online side to someone else is that you never get it back. So here is the deal in plain words, and it is the same deal written into the terms.</p>
      </div>
      <div class="grid grid--4">
        <div class="tile" data-reveal>
          <h3 class="t-h4" data-t>Your site, your data, your number</h3>
          <p data-t>The website, the database and the WhatsApp number stay yours throughout. We never hold them.</p>
        </div>
        <div class="tile" data-reveal>
          <h3 class="t-h4" data-t>Leave with thirty days&rsquo; notice</h3>
          <p data-t>No twelve month tie-in. We hand over the site files and an export of your database, free.</p>
        </div>
        <div class="tile" data-reveal>
          <h3 class="t-h4" data-t>We never touch your money</h3>
          <p data-t>Deposits run through your own account and your own payment provider. We take no cut of a booking.</p>
        </div>
        <div class="tile" data-reveal>
          <h3 class="t-h4" data-t>The price is the price</h3>
          <p data-t>No VAT, no setup surprises. If a job falls outside your plan we quote it before starting.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--edge">
    <div class="wrap">
      <div class="split">
        <div>
          <p class="eyebrow" data-t>Who you are dealing with</p>
          <h2 data-t>One person builds it. The same person answers you.</h2>
          <p class="lede" data-t>Ownerdeck is not an agency with account managers and a ticket queue. You get the person who wrote the thing, on WhatsApp, usually the same day. That is the whole reason a small operator can get work at this standard at this price.</p>
          <div class="btn-row" style="margin-top:2rem">
            <a class="btn btn--ghost" href="{WA}" rel="noopener"><span data-t>Message me directly</span>{ARROW}</a>
          </div>
        </div>
        <div class="namecard" data-reveal="120">
          <div class="namecard__top">
            <span class="od-mark" aria-hidden="true"></span>
            <span class="mock__meta">Larnaca &middot; Cyprus</span>
          </div>
          <p class="namecard__name">Mark Saade</p>
          <p class="namecard__role" data-t>Builds it, runs it, and answers the messages.</p>
          <ul class="namecard__facts">
            <li data-t>Sole trader, established in Cyprus</li>
            <li data-t>Not registered for VAT, so no VAT on any fee</li>
            <li data-t>Works remotely, so where you are does not matter</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

'''))

    # ------------------------------------------------------ what we build
    cards_long = []
    for slug, name, line, forwho, path in CARDS:
        cards_long.append(f'''      <article class="panel" id="{slug}" data-reveal style="margin-bottom:1.25rem">
        <div class="split" style="gap:3rem;align-items:start">
          <div>
            {icon(path)}
            <h2 class="t-h3" data-t>{name}</h2>
            <p class="lede" data-t>{line}</p>
          </div>
          <div>
            <p class="eyebrow" data-t>Who it is for</p>
            <p data-t>{forwho}</p>
          </div>
        </div>
      </article>''')

    P.append(dict(
        slug='what-we-build', in_flow=True, nav='What we build',
        title='What we build — Ownerdeck',
        desc='The five cards: Answer, Site, Book, Reach and Return, and the '
             'single set of facts underneath them all.',
        body=f'''  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow" data-t>What we build</p>
        <h1 data-t>Five cards. One system.</h1>
        <p class="lede" data-t>Start with the card you need and add the rest as you grow. Every card reads from the same set of facts, so nothing you own can contradict anything else you own.</p>
      </div>
{chr(10).join(cards_long)}

      <article class="panel" data-reveal style="margin-bottom:1.25rem">
        <p class="eyebrow" data-t>Answer, in practice</p>
        <div class="split" style="gap:3rem;align-items:center">
          <div>
            <p class="lede" data-t>Two in the morning, a question about a jeep, and a held booking by the time you wake up. No template and no menu of options — it read the question and answered from your prices.</p>
          </div>
          <div>{chat_mock()}</div>
        </div>
      </article>

      <article class="panel panel--plain" id="data" data-reveal>
        <div class="split" style="gap:3rem;align-items:start">
          <div>
            <p class="eyebrow" data-t>Underneath all of it</p>
            <h2 class="t-h3" data-t>Data</h2>
            <p class="lede" data-t>The database every card reads from. Your services, prices, seasons, availability, hours and policies, in one place with an admin screen you can actually use.</p>
          </div>
          <div>
            <p class="eyebrow" data-t>Why it matters</p>
            <p data-t>Without it, a price change means editing the website, correcting the assistant and remembering what you told Google. With it, you change one number.</p>
          </div>
        </div>
      </article>
    </div>
  </section>

'''))

    # ------------------------------------------------------- how it works
    P.append(dict(
        slug='how-it-works', in_flow=True, nav='How it works',
        title='How it works — Ownerdeck',
        desc='What you tell us once, what it runs, and what actually happens '
             'in the first week.',
        body=f'''  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow" data-t>How it works</p>
        <h1 data-t>Tell it once. It runs everything.</h1>
        <p class="lede" data-t>Most small businesses keep the same facts in four places and keep three of them wrong. Ownerdeck keeps them in one place and points everything else at it.</p>
      </div>

      <div class="grid grid--3">
        <div class="tile" data-reveal>
          <span class="tile__n">01</span>
          <h2 class="t-h3" data-t>You tell us the facts</h2>
          <p data-t>Services, prices, seasons, availability, opening hours, deposit and cancellation policy, photos. One conversation, usually about an hour.</p>
        </div>
        <div class="tile" data-reveal>
          <span class="tile__n">02</span>
          <h2 class="t-h3" data-t>We build it around them</h2>
          <p data-t>The database, then the website on top of it, then the assistant that answers from it, then bookings and the follow-up if you have taken those cards.</p>
        </div>
        <div class="tile" data-reveal>
          <span class="tile__n">03</span>
          <h2 class="t-h3" data-t>It runs, and we keep it running</h2>
          <p data-t>Hosting, backups, updates and the changes you ask for are the monthly fee. You send a message, we make the change.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--sunk section--edge">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow" data-t>The wiring</p>
        <h2 data-t>One set of facts, five outputs.</h2>
      </div>
      <div class="grid grid--2">
        <div class="panel" data-reveal>
          <p class="eyebrow" data-t>What you tell us once</p>
          <ul class="chips" style="margin-top:1rem">
            <li class="chip" data-on="1" data-t>Services</li><li class="chip" data-on="1" data-t>Prices</li>
            <li class="chip" data-on="1" data-t>Seasons</li><li class="chip" data-on="1" data-t>Availability</li>
            <li class="chip" data-on="1" data-t>Hours</li><li class="chip" data-on="1" data-t>Policies</li>
            <li class="chip" data-on="1" data-t>Photos</li>
          </ul>
        </div>
        <div class="panel" data-reveal>
          <p class="eyebrow" data-t>What reads from it</p>
          <ul class="chips" style="margin-top:1rem">
            <li class="chip" data-on="1" data-t>Your website</li><li class="chip" data-on="1" data-t>WhatsApp replies</li>
            <li class="chip" data-on="1" data-t>Instagram DMs</li><li class="chip" data-on="1" data-t>Website chat</li>
            <li class="chip" data-on="1" data-t>Booking confirmations</li><li class="chip" data-on="1" data-t>Google listing</li>
            <li class="chip" data-on="1" data-t>Follow-up messages</li>
          </ul>
        </div>
      </div>
      <p class="note" style="margin-top:1.5rem;text-align:center" data-t>Change a price in one place and every one of those changes with it.</p>
    </div>
  </section>

  <section class="section section--edge">
    <div class="wrap">
      <div class="split">
        <div>
          <p class="eyebrow" data-t>The first week</p>
          <h2 data-t>What actually happens.</h2>
          <p class="lede" data-t>No project plan, no kick-off deck. A conversation, a build, a check, and then it is live.</p>
        </div>
        <ol class="numbered">
          <li data-reveal><b>DAY 1</b><span data-t>We talk for an hour and write down everything your business charges for.</span></li>
          <li data-reveal><b>DAY 2</b><span data-t>You get the database and the admin screen, filled in, to correct.</span></li>
          <li data-reveal><b>DAY 4</b><span data-t>The site and the assistant are live on a test link for you to try.</span></li>
          <li data-reveal><b>DAY 6</b><span data-t>We point your number and your domain at it, and it goes live.</span></li>
        </ol>
      </div>
    </div>
  </section>

  <section class="section section--sunk section--edge">
    <div class="wrap">
      <div class="split">
        <div>
          <p class="eyebrow" data-t>Where the line is</p>
          <h2 data-t>The assistant knows your prices. It does not invent them.</h2>
          <p class="lede" data-t>It answers from your database and nothing else. When it does not know, it says so and hands the conversation to you rather than guessing. You can take over any conversation at any time.</p>
        </div>
        <div>{chat_mock()}</div>
      </div>
    </div>
  </section>

'''))

    # ------------------------------------------------------------ pricing
    plans = [
        dict(id='site', name='Site', flag=None, lead=False,
             desc='A proper website with an AI chat on it. The chat answers on your site — WhatsApp and Instagram start at the Deck.',
             build='&euro;600', month='&euro;99',
             on=['Site'],
             inc=['A fast website — your services, prices and contact details',
                  'An AI chat on the site, answering from your prices',
                  'Hosting, domain and certificate',
                  'Works properly on a phone, and on Google',
                  'Changes when you need them — you message, we change it',
                  'Backups and security updates'],
             out=['The assistant on WhatsApp and Instagram',
                  'Live database and admin screen',
                  'Bookings, deposits and calendar', 'Google listing',
                  'Follow-up campaigns'],
             cta='Start with Site'),
        dict(id='deck', name='Deck', flag='Common choice', lead=True,
             desc='The website, the database behind it, the assistant answering, and the bookings landing on your phone.',
             build='&euro;1,900', month='&euro;249',
             on=['Answer', 'Site', 'Book'],
             inc=['Everything in Site',
                  'The AI assistant on WhatsApp, Instagram DMs and website chat',
                  'A website that reads live from your prices',
                  'The database and an admin screen you control',
                  'Real availability, confirmations and deposits',
                  'A calendar that fills itself in'],
             out=['Google listing', 'Follow-up campaigns'],
             cta='Get the Deck'),
        dict(id='full-deck', name='Full Deck', flag=None, lead=False,
             desc='All five cards. Everything above, plus your Google listing set up properly and customers who come back.',
             build='&euro;2,400', month='&euro;299',
             on=['Answer', 'Site', 'Book', 'Reach', 'Return'],
             inc=['Everything in Deck',
                  'Google Business Profile set up and kept current',
                  'A review request after every booking',
                  'Reminders and off-season offers',
                  'Past customers brought back'],
             out=[],
             cta='Get the Full Deck'),
    ]

    plan_html = []
    for p in plans:
        chips = ''.join(
            '<li class="chip" data-on="%s" data-t>%s</li>' % ('1' if n in p['on'] else '0', n)
            for _s, n, _l, _f, _p in CARDS)
        inc = ''.join('<li>%s<span data-t>%s</span></li>' % (TICK, i) for i in p['inc'])
        out = ''
        if p['out']:
            out = ('<p class="note" style="margin-top:.25rem"><span data-t>Not included:</span> '
                   + ', '.join('<span data-t>%s</span>' % o for o in p['out']) + '.</p>')
        flag = '<span class="plan__flag" data-t>%s</span>' % p['flag'] if p['flag'] else ''
        plan_html.append(f'''        <div class="plan{' plan--lead' if p['lead'] else ''}" id="{p['id']}" data-reveal>
          <div class="plan__top"><h2 class="plan__name" data-t>{p['name']}</h2>{flag}</div>
          <p class="plan__desc" data-t>{p['desc']}</p>
          <div class="plan__price">
            <span class="plan__build">{p['build']}</span>
            <span class="plan__unit" data-t>one-off, to build it</span>
            <span class="plan__then">{p['month']} <span class="plan__unit" data-t>per month after</span></span>
          </div>
          <ul class="chips">{chips}</ul>
          <ul>{inc}</ul>
          {out}
          <a class="btn btn--primary" href="/start?plan={p['name'].replace(' ', '+')}" data-t>{p['cta']}</a>
        </div>''')

    P.append(dict(
        slug='pricing', in_flow=True, nav='Pricing',
        scripts='<script src="/calc.js?v=20260815a" defer></script>\n',
        title='Pricing — Ownerdeck',
        desc='Three hands: Site at €600 to build and €99 a month, Deck at '
             '€1,900 and €249, Full Deck at €2,400 and €299. No VAT.',
        body=f'''  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow" data-t>Pricing</p>
        <h1 data-t>Pick a hand. Add cards as you grow.</h1>
        <p class="lede" data-t>A one-off fee to build it, then a monthly fee to run it. The monthly covers hosting, the database, the assistant, backups and the changes you ask for. No VAT is charged.</p>
      </div>
      <div class="plans">
{chr(10).join(plan_html)}
      </div>

      <div class="panel" style="margin-top:2rem" data-reveal>
        <div class="split" style="gap:2.5rem;align-items:center">
          <div>
            <p class="eyebrow" data-t>Custom</p>
            <h3 data-t>Need something that is not on this list?</h3>
            <p data-t>A bigger site, several locations, a system you already use that has to connect to it, or a job that does not fit a card. Tell us what you need and we will send a written quote — a fixed price, no obligation.</p>
          </div>
          <div><a class="btn btn--primary" href="/start?plan=Custom"><span data-t>Ask for a quote</span>{ARROW}</a></div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--edge">
    <div class="wrap measure">
      <p class="eyebrow" data-t>The only number that matters</p>
      <h2 data-t>How many bookings pay for it?</h2>
      <p class="lede" data-t>Not what it costs. What it has to earn back. Drag your average booking and see.</p>

      <div class="calc" data-reveal>
        <label class="calc__row" for="calc-value">
          <span class="calc__label" data-t>Your average booking</span>
          <output class="calc__out" id="calc-value-out">&euro;180</output>
        </label>
        <input class="calc__range" id="calc-value" type="range"
               min="30" max="600" step="10" value="180"
               aria-describedby="calc-answer">

        <label class="calc__row" for="calc-plan">
          <span class="calc__label" data-t>Plan</span>
        </label>
        <select class="calc__select" id="calc-plan">
          <option value="99">Site &mdash; &euro;99 / month</option>
          <option value="249" selected>Deck &mdash; &euro;249 / month</option>
          <option value="299">Full Deck &mdash; &euro;299 / month</option>
        </select>

        <p class="calc__answer" id="calc-answer" aria-live="polite">
          <b id="calc-n">1.4</b> <span data-t>bookings a month covers it.</span>
        </p>
        <p class="note" data-t>Your own average, your own plan. It does not count the enquiries you were already going to answer yourself &mdash; only the ones that would otherwise have waited until morning.</p>
      </div>
    </div>
  </section>

  <section class="section section--sunk section--edge">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow" data-t>What the monthly covers</p>
        <h2 data-t>Running it is the job, not an extra.</h2>
      </div>
      <div class="grid grid--4">
        <div class="tile" data-reveal><h3 data-t>Hosting and domain</h3><p data-t>The site, the certificate and the domain renewal.</p></div>
        <div class="tile" data-reveal><h3 data-t>The assistant running</h3><p data-t>Every message answered, every hour, at our cost not yours.</p></div>
        <div class="tile" data-reveal><h3 data-t>Backups and updates</h3><p data-t>Kept online, kept current, kept backed up.</p></div>
        <div class="tile" data-reveal><h3 data-t>Changes you ask for</h3><p data-t>New prices, new services, new photos. You message, we change it.</p></div>
      </div>
      <p class="note" style="margin-top:2rem" data-t>Not covered: rebuilding the site from scratch, adding a card you did not take, or work outside the online side of the business. We will quote before doing any of it.</p>
    </div>
  </section>

  <section class="section section--edge">
    <div class="wrap measure">
      <p class="eyebrow" data-t>Money questions</p>
      <h2 data-t>The awkward ones, answered.</h2>
      <div class="faq" style="margin-top:2.5rem">
        <details><summary data-t>Why is there a build fee now?</summary><div><p data-t>Because building a website, a database and a working assistant takes real days, and a monthly-only price means every new client starts deeply underwater. The build fee covers the build at cost. The monthly is what keeps it running.</p></div></details>
        <details><summary data-t>Is there VAT on top?</summary><div><p data-t>No. Ownerdeck is not registered for VAT, so the prices shown are the prices you pay.</p></div></details>
        <details><summary data-t>Can I stop paying?</summary><div><p data-t>Yes, with a month&rsquo;s notice, on any plan. There is no minimum term. If you stop, you keep the site files and an export of your database, and we hand both over free.</p></div></details>
        <details><summary data-t>Do you take a cut of my bookings?</summary><div><p data-t>No. Deposits and payments run through your own account and your own payment provider. We never handle your customers&rsquo; money.</p></div></details>
        <details><summary data-t>What if I only want the assistant?</summary><div><p data-t>The assistant starts at the Deck, because it is only as good as the database behind it. Pointing it at a website with no live prices is how you get an assistant that confidently quotes last year&rsquo;s rates. If you already have a website you are happy with and want the assistant bolted onto it, we will quote for that separately — just ask.</p></div></details>
      </div>
    </div>
  </section>

'''))

    # -------------------------------------------------------- who its for
    trade_html = []
    for slug, name, alt, line in TRADES:
        trade_html.append(f'''        <li class="trade" data-reveal>
          <div class="trade__img"><img src="/img/{slug}.webp"{img_size(slug)} loading="lazy" decoding="async" alt="{alt}"></div>
          <div class="trade__body"><h2 data-t>{name}</h2><p data-t>{line}</p></div>
        </li>''')

    P.append(dict(
        slug='who-its-for', in_flow=True, nav="Who it's for",
        title="Who it's for — Ownerdeck",
        desc='Built for owner-operated businesses that run on bookings: rental, '
             'charter, tours, villas, hotels, estate agencies, clinics and salons.',
        body=f'''  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow" data-t>Who it is for</p>
        <h1 data-t>Built for businesses that run on bookings.</h1>
        <p class="lede" data-t>If your customers ask what it costs, whether it is free, and can they have it tomorrow — this is built for you. The trade changes, the questions do not.</p>
      </div>
      <ul class="trades">
{chr(10).join(trade_html)}
      </ul>
      <p class="note" style="margin-top:2rem" data-t>Not on the list? If your business takes bookings or answers the same questions all day, it will fit. Ask us.</p>
    </div>
  </section>

  <section class="section section--sunk section--edge">
    <div class="wrap">
      <div class="split">
        <div data-reveal>
          <p class="eyebrow" data-t>Proof &middot; Limassol</p>
          <div class="stat">
            <span class="stat__n">14</span>
            <span class="stat__l" data-t>enquiries booked between 9pm and 8am last month</span>
          </div>
          <p class="lede" style="margin-top:2rem" data-t>A car rental operator in Limassol, live at &euro;150 a month. Those 14 were booked while the owner was asleep.</p>
        </div>
        <div class="ledger" data-reveal="120">
          <div class="ledger__row"><span class="mono">LAST 30 DAYS</span><b data-t>Car rental, Limassol</b></div>
          <div class="ledger__row"><span data-t>Enquiries answered</span><b>212</b></div>
          <div class="ledger__row"><span data-t>Answered after hours</span><b>14</b></div>
          <div class="ledger__row"><span data-t>Average reply time</span><b data-t>under a minute</b></div>
        </div>
      </div>
    </div>
  </section>

'''))

    # ---------------------------------------------------------- questions
    QA = [
        ('I already have a website. Do I have to replace it?',
         'No. If you are happy with it, we can point the assistant at it and leave it alone. But if it is out of date and nobody can edit it, replacing it is usually cheaper than maintaining it.'),
        ('Do I need a new phone number?',
         'No. The assistant runs on your existing WhatsApp Business number. Your customers keep messaging the number they already have.'),
        ('What happens when it does not know the answer?',
         'It says so and hands the conversation to you, with everything the customer already said. It never guesses at a price or an availability.'),
        ('Can I take over a conversation?',
         'At any time. You reply from your own phone and the assistant steps back for that conversation.'),
        ('What languages does it answer in?',
         'Whatever the customer writes in. It reads the message, answers in the same language, and your prices stay the same in all of them.'),
        ('Who owns the website and the data?',
         'You do. The site, the database and the phone number are yours. If you leave, we hand over the site files and an export of your data.'),
        ('How long does it take to go live?',
         'About a week for the Deck, less for Answer. The slow part is usually waiting on photos and a decision about prices.'),
        ('I am not technical. Is that a problem?',
         'No. Everything you need to change day to day is a form with words on it, and if you would rather not, you message us and we change it.'),
        ('Do you work outside Cyprus?',
         'Yes. Everything is remote and the assistant does not care where it runs. Most clients are in Cyprus because that is where we are.'),
        ('What if the assistant gets something wrong?',
         'Tell us and we fix the facts it read from, so it cannot get the same thing wrong twice. It answers from your database, so a wrong answer is almost always a wrong entry.'),
        ('Is my customers&rsquo; data safe?',
         'Conversations are processed to answer them and stored so you can read your own history. We do not sell data or use it to advertise. The privacy notice sets out exactly who processes what.'),
        ('Why not just use ChatGPT?',
         'Because ChatGPT does not know whether the Jimny is free on Saturday. It writes a convincing sentence about your prices without having seen them. Ownerdeck answers from your database — the actual fleet, the actual rates, the actual calendar — and when it does not know, it says so and passes the conversation to you. The writing is the easy part. Being right is the product.'),
        ('Can I start small and add later?',
         'That is the point of the deck. Start with Site to get online properly, move to the Deck when you want the messages answered and the bookings taken, add Reach and Return when you want the quiet months filled.'),
    ]
    qa_html = '\n'.join(
        f'        <details><summary data-t>{q}</summary><div><p data-t>{a}</p></div></details>'
        for q, a in QA)

    P.append(dict(
        slug='questions', in_flow=True, nav='Questions',
        title='Questions — Ownerdeck',
        desc='The questions owners actually ask: numbers, ownership, languages, '
             'what happens when the assistant does not know.',
        body=f'''  <section class="section">
    <div class="wrap measure">
      <p class="eyebrow" data-t>Questions</p>
      <h1 data-t>Everything owners ask.</h1>
      <p class="lede" data-t>If yours is not here, message us — it probably belongs on this page.</p>
      <div class="faq" style="margin-top:3rem">
{qa_html}
      </div>
    </div>
  </section>

'''))

    # ---------------------------------------------------------- get started
    # data-t goes on the visible label only. data-value stays English on
    # purpose: it is what ends up in the WhatsApp message and the Stripe
    # metadata, and those are read by us, not by the visitor. Without the
    # data-t these twelve buttons were the only text on the site that never
    # changed when the language did.
    trade_picks = '\n'.join(
        f'          <button class="pick" type="button" data-pick="trade" '
        f'aria-pressed="false" data-value="{name}"><b data-t>{name}</b></button>'
        for _s, name, _alt, _l in TRADES)

    plan_picks = '\n'.join(
        f'''          <button class="pick" type="button" data-pick="plan" aria-pressed="false"
                  data-value="{p['name']}" data-price="{p['build']} + {p['month']}/mo">
            <b data-t>{p['name']}</b><span data-t>{p['build'].replace('&euro;', '€')} to build, then {p['month'].replace('&euro;', '€')} a month</span>
          </button>''' for p in plans)

    P.append(dict(
        slug='start', in_flow=False, no_cta=True, nav='Get started',
        title='Get started — Ownerdeck',
        desc='Three questions and we will know exactly what you need before you '
             'send a single message.',
        scripts='<script src="/start.js?v=20260815a" defer></script>\n',
        body=f'''  <section class="section">
    <div class="wrap">
      <div class="flow" id="start">
        <div class="flow__dots" aria-hidden="true"><span></span><span></span><span></span><span></span></div>

        <section class="flow__step" data-step="1">
          <p class="eyebrow" data-t>Step one</p>
          <h2 tabindex="-1" data-focus data-t>What kind of business is it?</h2>
          <p class="lede" style="margin-bottom:2rem" data-t>So the quote is about your trade rather than a generic package.</p>
          <div class="flow__grid">
{trade_picks}
            <button class="pick" type="button" data-pick="trade" aria-pressed="false" data-value="Something else"><b data-t>Something else</b></button>
          </div>
        </section>

        <section class="flow__step" data-step="2">
          <p class="eyebrow" data-t>Step two</p>
          <h2 tabindex="-1" data-focus data-t>How much of it do you want run for you?</h2>
          <p class="lede" style="margin-bottom:2rem" data-t>Not sure? Pick the middle one — we will tell you honestly if you need less.</p>
          <div class="flow__grid">
{plan_picks}
            <button class="pick" type="button" data-pick="plan" aria-pressed="false" data-value="Not sure yet"><b data-t>Not sure yet</b><span data-t>Talk it through first</span></button>
          </div>
          <button class="flow__back" type="button" data-go="back" data-t>Back</button>
        </section>

        <section class="flow__step" data-step="3">
          <p class="eyebrow" data-t>Step three</p>
          <h2 tabindex="-1" data-focus data-t>Anything we should know?</h2>
          <p class="lede" style="margin-bottom:2rem" data-t>Optional. A sentence about what is not working now is usually enough.</p>
          <label class="visually-hidden" for="flow-note" data-t>Anything we should know</label>
          <textarea id="flow-note" maxlength="400" placeholder="We get most enquiries on Instagram at night and lose half of them…"></textarea>
          <div class="btn-row" style="margin-top:1.5rem">
            <a class="btn btn--primary" href="#" data-go="next"><span data-t>See what happens next</span>{ARROW}</a>
          </div>
          <button class="flow__back" type="button" data-go="back" data-t>Back</button>
        </section>

        <section class="flow__step" data-step="4">
          <p class="eyebrow" data-t>Last step</p>
          <h2 tabindex="-1" data-focus data-t>That is everything we need.</h2>
          <p class="lede" data-t>Open the chat and it will already say all of this, so you are not repeating yourself. You will get a straight answer, usually the same day.</p>
          <dl class="flow__summary" id="flow-summary"></dl>

          <div class="deposit" id="flow-paid" hidden>
            <span class="deposit__tick">{TICK}</span>
            <p data-t>Deposit received. Your slot is held — open the chat and we will pick it up from here.</p>
          </div>

          <div class="btn-row">
            <a class="btn btn--primary" id="flow-wa" href="{WA}" rel="noopener"><span data-t>Open WhatsApp</span>{ARROW}</a>
            <a class="btn btn--ghost" id="flow-mail" href="mailto:{EMAIL}" data-t>Email instead</a>
          </div>

          <div class="deposit deposit--offer" id="flow-pay-wrap">
            <div>
              <p class="deposit__head" data-t>Want the slot held while we talk?</p>
              <p class="note" data-t>&euro;75, refundable in full until work starts, and credited against your build fee. It is a way to hold your place in the queue, not a commitment.</p>
            </div>
            <a class="btn btn--ghost btn--sm" id="flow-pay" href="#"><span data-t>Hold my slot &mdash; &euro;75</span></a>
          </div>

          <p class="note" style="margin-top:1.5rem" data-t>Your answers are not sent anywhere. They are filled into a message you choose to open. Card details are handled entirely by Stripe and never touch this site.</p>
          <button class="flow__back" type="button" data-go="back" data-t>Back</button>
        </section>
      </div>
    </div>
  </section>

'''))

    # --------------------------------------------------------------- demo
    P.append(dict(
        slug='demo', in_flow=False, no_cta=True, nav='See it work',
        title='See it work — Ownerdeck',
        desc='Watch Ownerdeck handle a real enquiry, try it yourself, then ask '
             'the live assistant anything. Three steps, no sign-up.',
        head='<style>\n' + _frag('_demo_style.css') + '</style>\n',
        scripts=('<script src="/demo.js?v=20260815a"></script>\n'
                 + _frag('_demo_tail.html') + '\n'),
        body='  <div class="wrap section">\n' + _frag('_demo_body.html') + '  </div>\n\n'))

    # -------------------------------------------------------------- legal
    P.extend(_legal.pages(EMAIL, WA))
    return P
