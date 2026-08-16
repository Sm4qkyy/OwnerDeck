# Move the four SEO guides onto od.css.
#
# They were the last pages still asking for brand.css, which .vercelignore
# excludes from the deployment — so in production the stylesheet 404s and the
# guides render as raw unstyled text. They are indexed pages, so that is a live
# bug, not a cosmetic one.
#
# Surgical, not regenerated. Each guide carries hand-written Article, FAQPage
# and BreadcrumbList JSON-LD plus its own OG tags, and rebuilding the page from
# a template would mean re-deriving all of that. Instead the chrome around the
# content is swapped and everything between <main> and </main> is kept.
#
# The header and footer come from _build_site, so the guides cannot drift away
# from the rest of the site.
#
# Idempotent: running it twice is a no-op, because the markers it searches for
# only exist in the old chrome.
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _build_site as B   # noqa: E402

# Every served page that _build_site.py does NOT generate but that still has
# to carry the shared chrome. stats.html belongs here for the same reason the
# guides do: it was converted to od.css separately, so nothing was keeping its
# header in step, and it kept the retired placeholder mark after the real logo
# went in.
GUIDES = [
    'whatsapp-bot-car-rental.html',
    'whatsapp-booking-bot-boat-charter-tours.html',
    'whatsapp-auto-reply-vs-ai-assistant.html',
    'do-i-need-a-new-number-whatsapp-bot.html',
    'stop-losing-bookings-slow-whatsapp-replies.html',
    'stats.html',
]

NEW_ASSETS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap">\n'
    '<link rel="stylesheet" href="/od.css?v=%s">' % B.VER
)

NEW_THEME_COLOR = (
    '<meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)">\n'
    '<meta name="theme-color" content="#0A0A0B" media="(prefers-color-scheme: dark)">'
)

BACK = ('<a class="back" href="/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M19 12H5M11 6l-6 6 6 6"/></svg> Back to ownerdeck.com</a>')


def convert(name):
    path = os.path.join(HERE, name)
    html = io.open(path, encoding='utf-8').read()
    before = len(html)

    first_run = 'brand.css' in html

    # ---- one-time migrations, only meaningful on the first pass -----------
    if first_run:
        # 1. Fonts and stylesheet. The retired Fraunces/Switzer preloads go with
        #    them — those files are still in the repo but nothing asks for them.
        html = re.sub(
            r'<link rel="preload" href="fonts/[^"]+"[^>]*>\s*'
            r'(<link rel="preload" href="fonts/[^"]+"[^>]*>\s*)*'
            r'<link rel="stylesheet" href="brand\.css[^"]*">',
            NEW_ASSETS, html)

        # Theme colour, now that there are two themes.
        html = html.replace('<meta name="theme-color" content="#F7F4EF">', NEW_THEME_COLOR)

        # Favicon paths were relative, which is wrong on a clean URL.
        html = html.replace('href="favicon.png"', 'href="/favicon.png"')

        # The content wrapper. <main id="main"> now carries the id, and the
        # reading measure comes from .measure.
        html = html.replace('<main>\n  <div id="main" class="wrap section longform">',
                            '<main id="main">\n  <div class="wrap measure longform">')

        # Body classes that changed meaning or name.
        html = re.sub(r'<a class="back-link" href="/">[^<]*</a>', BACK, html)
        html = html.replace('<div class="note">', '<div class="callout">')

    # ---- always refresh the chrome ---------------------------------------
    # Not guarded by first_run. These guides have to track _build_site or they
    # drift the moment the header changes — which is exactly what happened when
    # the logo went in and they kept the retired placeholder mark. Both patterns
    # match the old markup and the new, so this is safe to run repeatedly.
    # stats.html is an internal dashboard behind a robots Disallow — a sales
    # chat widget has no business on it. The guides are public landing pages
    # where it earns its place, so they keep it and get its stylesheet below.
    ctx = {'no_widget': name == 'stats.html'}

    html = re.sub(r'<a class="skip-link".*?</header>', B.header().strip(), html, flags=re.S)
    html = re.sub(r'<footer class="(?:footer|foot)">.*?</html>\s*',
                  B.footer(ctx).lstrip(), html, flags=re.S)

    # The shared footer pulls in chat-widget.js, so any page keeping the widget
    # needs its stylesheet too. Without it the launcher rendered as a huge grey
    # unstyled block pinned to the bottom-left of every guide.
    if not ctx['no_widget'] and 'chat-widget.css' not in html:
        html = html.replace('<link rel="stylesheet" href="/od.css?v=%s">' % B.VER,
                            '<link rel="stylesheet" href="/od.css?v=%s">\n'
                            '<link rel="stylesheet" href="/chat-widget.css?v=%s">'
                            % (B.VER, B.VER), 1)

    # Translation keys for the chrome that was just inserted.
    html = B.tag_i18n(html, name)

    io.open(path, 'w', encoding='utf-8', newline='\n').write(html)
    return name, before, len(html), 'converted' if first_run else 'chrome refreshed'


FAVICONS = (
    '<link rel="icon" type="image/png" href="/favicon.png" media="(prefers-color-scheme: light)">\n'
    '<link rel="icon" type="image/png" href="/favicon-dark.png" media="(prefers-color-scheme: dark)">\n'
    '<link rel="apple-touch-icon" href="/favicon.png">'
)


def normalise_favicons():
    """Runs over every page this script owns, not only the ones it just
    converted."""
    done = []
    for name in GUIDES:
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            continue
        html = io.open(path, encoding='utf-8').read()
        # One or more icon links, then apple-touch. The `+` matters: matching a
        # single icon link meant that on a second run the pattern latched onto
        # the dark link and the apple-touch after it, and prepended the whole
        # block again. Four re-runs left four duplicate light-mode links.
        new = re.sub(
            r'(?:<link rel="icon"[^>]*>\s*)+<link rel="apple-touch-icon"[^>]*>',
            FAVICONS, html, count=1)
        if new != html:
            io.open(path, 'w', encoding='utf-8', newline='\n').write(new)
            done.append(name)
    return done


def main():
    print('%-46s %8s %8s  %s' % ('GUIDE', 'BEFORE', 'AFTER', ''))
    for name in GUIDES:
        n, a, b, note = convert(name)
        print('%-46s %8d %8d  %s' % (n, a, b, note))

    touched = normalise_favicons()
    if touched:
        print('\n  light/dark favicon pair added to: %s' % ', '.join(touched))

    # Nothing served should still reference the retired stylesheet.
    stale = []
    for f in sorted(os.listdir(HERE)):
        if not f.endswith('.html') or f.startswith('_'):
            continue
        body = io.open(os.path.join(HERE, f), encoding='utf-8').read()
        if re.search(r'(href|src)="[^"]*(brand\.css|motion\.js)', body):
            stale.append(f)
    print()
    if stale:
        print('  STILL REFERENCING RETIRED ASSETS: %s' % ', '.join(stale))
        sys.exit(1)
    print('  No served page references brand.css or motion.js.')


if __name__ == '__main__':
    main()
