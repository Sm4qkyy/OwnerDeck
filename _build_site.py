# Builds every page of the site from one set of chrome plus the content in
# _content.py, and writes the sitemap to match.
#
# Why a generator and not ten hand-written files: the header, footer, meta
# block and script tags are identical on every page. Hand-maintained, they
# drift — one page keeps a nav item another has lost, one forgets the theme
# bootstrap and flashes white on load. Here there is exactly one copy.
#
# It also assigns the translation keys. Content marked `data-t` gets
# data-i18n="k<md5 of its text>", so editing an English sentence changes its
# key, the lookup misses, and the element falls back to the English in the
# markup. A stale translation cannot outlive the sentence it was made from.
#
# Run:  python _build_site.py
import hashlib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _content as C   # noqa: E402

ORIGIN = 'https://www.ownerdeck.com'
WA = '447520689685'
EMAIL = 'mark@ownerdeck.com'
WA_TEXT = 'Hi%20Mark%20%E2%80%94%20I%20saw%20Ownerdeck%20and%20I%27d%20like%20to%20know%20more.'
WA_LINK = 'https://wa.me/%s?text=%s' % (WA, WA_TEXT)
VER = '20260815a'

ARROW = ('<svg class="btn__arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>')

# The real OD monogram, drawn as a CSS mask rather than an <img>. The file is a
# pure alpha mask, so painting it with currentColor means one asset serves both
# themes and it always matches the wordmark beside it — no light/dark swap, no
# second file to keep in step.
MARK = '<span class="od-mark" aria-hidden="true"></span>'

# Primary navigation. One list, used for the desktop bar and the mobile panel,
# so the two can never disagree.
NAV = [
    ('/what-we-build', 'What we build'),
    ('/how-it-works',  'How it works'),
    ('/pricing',       'Pricing'),
    ('/who-its-for',   "Who it's for"),
    ('/questions',     'Questions'),
]

LEGAL_NAV = [
    ('/terms',   'Terms'),
    ('/privacy', 'Privacy'),
    ('/cookies', 'Cookies'),
    ('/legal',   'Legal notice'),
]

# ---------------------------------------------------------------- i18n keys
# Matches an element carrying a bare `data-t`. Deliberately narrow: the inner
# text must be plain, because i18n.js swaps translations in through
# textContent and that would delete any markup nested inside.
TAG_T = re.compile(
    r'<(?P<tag>[a-z0-9]+)(?P<a>[^>]*?)\sdata-t(?P<b>[^>]*?)>(?P<inner>[^<]*?)</(?P=tag)>')

SOURCE = {}   # key -> English text, written out for the translators


def key_for(text):
    norm = ' '.join(text.split())
    return 'k' + hashlib.md5(norm.encode('utf-8')).hexdigest()[:8], norm


def tag_i18n(html, where):
    """Replace every `data-t` with a content-hashed data-i18n attribute."""
    def sub(m):
        inner = m.group('inner')
        if not inner.strip():
            raise SystemExit('empty data-t element in %s' % where)
        k, norm = key_for(inner)
        SOURCE[k] = norm
        return '<%s%s data-i18n="%s"%s>%s</%s>' % (
            m.group('tag'), m.group('a'), k, m.group('b'), inner, m.group('tag'))

    out = TAG_T.sub(sub, html)
    # Anything left means the element had markup inside it, which this scheme
    # cannot translate. Fail loudly instead of shipping a silent gap.
    leftover = re.search(r'<[a-z0-9]+[^>]*\sdata-t[\s>]', out)
    if leftover:
        raise SystemExit('data-t on an element with nested markup in %s:\n  %s'
                         % (where, out[leftover.start():leftover.start() + 160]))
    return out


# ---------------------------------------------------------------- chrome
def head(page):
    url = ORIGIN + ('/' if page['slug'] == 'index' else '/' + page['slug'])
    title = page['title']
    desc = page['desc']
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="%(url)s">

<meta property="og:type" content="website">
<meta property="og:url" content="%(url)s">
<meta property="og:site_name" content="Ownerdeck">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:image" content="%(origin)s/og-image.jpg">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="%(origin)s/og-image.jpg">

<!-- Both marks are transparent PNGs, so each needs the tab colour it was drawn
     against. Browsers that ignore media on a favicon take the first, which is
     the dark-on-light one — the safe default. -->
<link rel="icon" type="image/png" href="/favicon.png" media="(prefers-color-scheme: light)">
<link rel="icon" type="image/png" href="/favicon-dark.png" media="(prefers-color-scheme: dark)">
<link rel="apple-touch-icon" href="/favicon.png">
<meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0B0B12" media="(prefers-color-scheme: dark)">

<!-- Runs before first paint and does two things.
     .js marks that scripting is available: every rule in od.css that hides
     something is scoped to it, so if this line is never reached the page
     renders complete rather than blank.
     data-theme is read here rather than in od.js because a deferred script
     would repaint the page light-then-dark on every single load. -->
<script>
(function () {
  var r = document.documentElement;
  r.classList.add('js');
  try {
    var t = localStorage.getItem('od_theme');
    if (t === 'light' || t === 'dark') r.setAttribute('data-theme', t);
  } catch (e) {}
})();
</script>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/od.css?v=%(ver)s">
%(widget_css)s%(extra)s</head>
<body>
''' % dict(title=title, desc=desc, url=url, origin=ORIGIN, ver=VER,
           extra=page.get('head', ''),
           widget_css=('' if page.get('no_widget') else
                       '<link rel="stylesheet" href="/chat-widget.css?v=%s">\n' % VER))


def header():
    nav = '\n'.join(
        '      <a href="%s" data-t>%s</a>' % (h, l) for h, l in NAV)
    mob = '\n'.join(
        '        <a href="%s" data-t>%s</a>' % (h, l) for h, l in NAV)
    legal = '\n'.join(
        '        <a href="%s" data-t>%s</a>' % (h, l) for h, l in LEGAL_NAV)
    return '''<a class="skip-link" href="#main" data-t>Skip to content</a>

<header class="masthead">
  <div class="wrap masthead__bar">
    <a class="masthead__mark" href="/" aria-label="Ownerdeck home">%(mark)s Ownerdeck</a>

    <nav class="masthead__nav" aria-label="Primary">
%(nav)s
    </nav>
    <span class="masthead__nav-spacer"></span>

    <div class="masthead__tools">
      <!-- i18n.js inserts the language switcher immediately before this
           button, so the id is load-bearing, not decoration. -->
      <button id="theme-toggle" class="icon-btn" type="button" aria-label="Switch to the dark theme">
        <svg class="ic-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.2v2M12 19.8v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M2.2 12h2M19.8 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>
        <svg class="ic-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>
      </button>

      <a class="btn btn--primary btn--sm masthead__cta" href="/start" data-t>Get started</a>

      <!-- <details> rather than a scripted panel: it opens, closes and takes
           keyboard focus with no JavaScript at all. -->
      <details class="mmenu">
        <summary aria-label="Open the menu"><span class="mmenu__bars" aria-hidden="true"><i></i></span></summary>
        <div class="mmenu__panel">
%(mob)s
          <span class="mmenu__sep"></span>
%(legal)s
          <a class="btn btn--primary" href="%(wa)s" rel="noopener" data-t>Message us on WhatsApp</a>
        </div>
      </details>
    </div>
  </div>
</header>

''' % dict(mark=MARK, nav=nav, mob=mob, legal=legal, wa=WA_LINK)


def cta_band():
    return '''  <section class="section">
    <div class="wrap">
      <div class="cta" data-reveal>
        <h2 data-t>Set it once. Let it run.</h2>
        <p data-t>Tell us about your business and we will show you exactly how Ownerdeck would handle your website, your messages and your bookings.</p>
        <div class="btn-row">
          <a class="btn btn--primary" href="/start"><span data-t>Get started</span>%(arrow)s</a>
          <a class="btn btn--ghost" href="%(wa)s" rel="noopener" data-t>Or message us on WhatsApp</a>
        </div>
        <p class="note" data-t>No VAT. No long contract on the entry plan.</p>
      </div>
    </div>
  </section>

''' % dict(wa=WA_LINK, arrow=ARROW)


def pagenav(prev, nxt):
    if not prev and not nxt:
        return ''
    out = ['  <div class="wrap"><nav class="pagenav" aria-label="Page">']
    if prev:
        out.append('    <a href="%s"><small data-t>Previous</small><b data-t>%s</b></a>'
                   % (prev[0], prev[1]))
    else:
        out.append('    <span></span>')
    if nxt:
        out.append('    <a href="%s"><small data-t>Next</small><b data-t>%s</b></a>'
                   % (nxt[0], nxt[1]))
    out.append('  </nav></div>\n\n')
    return '\n'.join(out)


def footer(page=None):
    build = '\n'.join('<li><a href="/what-we-build#%s" data-t>%s</a></li>' % (s.lower(), s)
                      for s in ['Answer', 'Site', 'Data', 'Book', 'Reach', 'Return'])
    read = '\n'.join('<li><a href="%s" data-t>%s</a></li>' % (h, l) for h, l in NAV)
    legal = '\n'.join('<li><a href="%s" data-t>%s</a></li>' % (h, l) for h, l in LEGAL_NAV)
    return '''<footer class="foot">
  <div class="wrap">
    <div class="foot__grid">
      <div>
        <a class="masthead__mark" href="/" aria-label="Ownerdeck home">%(mark)s Ownerdeck</a>
        <p class="foot__blurb" data-t>We build and run the online side of small owner-operated businesses. One set of facts drives the website, the messages, the bookings and the follow-up.</p>
      </div>
      <div>
        <h2 data-t>The cards</h2>
        <ul>%(build)s</ul>
      </div>
      <div>
        <h2 data-t>Reading</h2>
        <ul>%(read)s</ul>
      </div>
      <div>
        <h2 data-t>Legal</h2>
        <ul>%(legal)s</ul>
        <h2 style="margin-top:1.5rem" data-t>Contact</h2>
        <ul>
          <li><a href="%(wa)s" rel="noopener" data-t>WhatsApp</a></li>
          <li><a href="mailto:%(email)s">%(email)s</a></li>
        </ul>
      </div>
    </div>
    <div class="foot__base">
      <span>&copy; 2026 Ownerdeck</span>
      <span data-t>Built and run by Ownerdeck.</span>
    </div>
  </div>
</footer>

%(widget_js)s%(scripts)s<script src="/i18n.js?v=%(ver)s" defer></script>
<script src="/od.js?v=%(ver)s" defer></script>
<script src="/analytics-events.js?v=%(ver)s" defer></script>
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
''' % dict(mark=MARK, build=build, read=read, legal=legal,
           wa=WA_LINK, email=EMAIL, ver=VER,
           scripts=(page or {}).get('scripts', ''),
           widget_js=('' if (page or {}).get('no_widget') else
                      '<script src="/config.js?v=%s"></script>\n'
                      '<script src="/chat-widget.js?v=%s"></script>\n' % (VER, VER)))


# ---------------------------------------------------------------- driver
def build():
    pages = C.pages(WA_LINK, ARROW, EMAIL)
    order = [p for p in pages if p.get('in_flow')]

    written = []
    for i, page in enumerate(pages):
        prev = nxt = None
        if page.get('in_flow'):
            j = order.index(page)
            if j > 0:
                prev = ('/' + order[j - 1]['slug'], order[j - 1]['nav'])
            if j < len(order) - 1:
                nxt = ('/' + order[j + 1]['slug'], order[j + 1]['nav'])

        html = (head(page) + header() +
                '<main id="main">\n\n' + page['body'] +
                ('' if page.get('no_cta') else cta_band()) +
                '</main>\n\n' + pagenav(prev, nxt) + footer(page))

        html = tag_i18n(html, page['slug'])

        name = 'index.html' if page['slug'] == 'index' else page['slug'] + '.html'
        path = os.path.join(HERE, name)
        with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)
        written.append((name, len(html)))

    # Sitemap, generated from the same list so it cannot fall behind.
    urls = []
    for p in pages:
        loc = ORIGIN + ('/' if p['slug'] == 'index' else '/' + p['slug'])
        pri = '1.0' if p['slug'] == 'index' else ('0.5' if p.get('legal') else '0.8')
        urls.append('  <url><loc>%s</loc><priority>%s</priority></url>' % (loc, pri))
    # /stats is disallowed in robots.txt, so it has no business in the sitemap.
    # The four guides stay out of the navigation but keep their URLs live.
    for extra in ['/demo',
                  '/whatsapp-bot-car-rental',
                  '/whatsapp-booking-bot-boat-charter-tours',
                  '/whatsapp-auto-reply-vs-ai-assistant',
                  '/do-i-need-a-new-number-whatsapp-bot',
                  '/stop-losing-bookings-slow-whatsapp-replies']:
        urls.append('  <url><loc>%s%s</loc><priority>0.6</priority></url>' % (ORIGIN, extra))
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + '\n'.join(urls) + '\n</urlset>\n')
    with io.open(os.path.join(HERE, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(sitemap)

    with io.open(os.path.join(HERE, '_en_source.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(SOURCE, f, ensure_ascii=False, indent=1, sort_keys=True)

    for name, n in written:
        print('  %-22s %6d bytes' % (name, n))
    print('\n  %d pages · %d translatable strings -> _en_source.json'
          % (len(written), len(SOURCE)))


if __name__ == '__main__':
    build()
